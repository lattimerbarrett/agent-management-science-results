"""An OpenAI-compatible endpoint, for when the code that calls the model is not yours to change.

    swarm-serve                          # Qwen3.5-4B on http://127.0.0.1:8091/v1, 50 calls side by side
    swarm-serve --model 9B --width 100

Prefer `Engine` when you can: it is about 10% faster and it is the only way a context shared by 50 agents is
read once (through this server the 49 others each reuse 512 tokens of it). This starts vllm-mlx (the same MLX
underneath, so the next fastest thing on this machine) under the machine lock, with the settings its defaults
get wrong for an experiment:

  --pflash off                   by default it compresses long prompts for Qwen3.5, dropping what an agent reads
  --no-spec-decode               by default it downloads and runs a speculative-decoding helper; no faster at 50
  --text-only                    the Qwen3.5 builds carry a vision tower that players do not need
  --gpu-memory-utilization 0.45  at its own 0.6 it took this laptop to 1.5 GB free and failed 28 of 50 requests

and with a guard that stops the server if the machine gets under 7 GB free, which a round of long prompts can do.

One thing cannot be fixed from here: the server switches thinking OFF unless each request asks for it. Send
`"chat_template_kwargs": {"enable_thinking": true}` in the request body, or call `chat` below.
"""
import argparse
import os
import shutil
import signal
import subprocess
import sys
import time

from .machine import guard, under_lock
from .settings import Sampling, integer
from dataclasses import asdict
import secrets

MODELS = {"4B": "mlx-community/Qwen3.5-4B-4bit", "9B": "mlx-community/Qwen3.5-9B-4bit"}


def command(model: str, port: int, width: int, memory: float = 0.45) -> list[str]:
    """The vllm-mlx command line, with its experiment-changing defaults turned off."""
    binary = shutil.which("vllm-mlx") or os.path.expanduser("~/.local/bin/vllm-mlx")
    return [binary, "--no-telemetry", "--no-banner", "serve", MODELS.get(model, model), "--host", "127.0.0.1",
            "--port", str(port), "--text-only", "--pflash", "off", "--no-spec-decode", "--hybrid-cache-entries", "64",
            "--max-num-seqs", str(width), "--completion-batch-size", str(width), "--prefill-batch-size", str(width),
            "--gpu-memory-utilization", str(memory), "--cache-memory-mb", "2048", "--watchdog-ppid", str(os.getpid())]


def chat(base: str, messages: list[dict], *, thinking: bool = True, max_total_tokens: int = 32768,
         sampling: Sampling | None = None, timeout: float = 900.0, **body) -> dict:
    """Return the FULL completion, including choices[*].finish_reason and usage.

    The server's max_tokens counts thinking AND answers. max_total_tokens names
    that explicitly here; legacy max_tokens in body is accepted as the same total
    allowance. This endpoint does not implement Engine's forced-thinking budget
    or separate answer limit. It is a different backend, not an equivalent replay.
    """
    import httpx

    if not isinstance(thinking, bool):
        raise ValueError("thinking must be a boolean")
    if body.get("stream"):
        raise ValueError("chat() returns a complete response; streaming is not supported")
    if "max_tokens" in body:
        if max_total_tokens != 32768:
            raise ValueError("Pass max_total_tokens or legacy max_tokens, not both")
        max_total_tokens = body.pop("max_tokens")
    integer("max_total_tokens", max_total_tokens, 1)
    template = dict(body.pop("chat_template_kwargs", {}))
    if "enable_thinking" in template and template["enable_thinking"] != thinking:
        raise ValueError("Conflicting thinking and chat_template_kwargs.enable_thinking")
    template["enable_thinking"] = thinking
    payload = {**asdict(sampling or Sampling()), "seed": secrets.randbits(31), **body,
               "messages": messages, "max_tokens": max_total_tokens, "chat_template_kwargs": template}
    if "model" not in payload:
        models = httpx.get(f"{base}/v1/models", timeout=10.0)
        models.raise_for_status()
        payload["model"] = models.json()["data"][0]["id"]
    reply = httpx.post(f"{base}/v1/chat/completions", json=payload, timeout=timeout)
    reply.raise_for_status()
    result = reply.json()
    result["swarm_settings"] = {k: v for k, v in payload.items() if k != "messages"}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="4B", help='"4B", "9B" or any model vllm-mlx can serve')
    parser.add_argument("--port", type=int, default=8091)
    parser.add_argument("--width", type=int, default=50, help="calls generated side by side")
    parser.add_argument("--mem-gb", type=float, default=20, help="what the lock wrapper is told this job may use")
    parser.add_argument("--floor-gb", type=float, default=7.0, help="stop the server if available memory falls under this")
    args = parser.parse_args()
    under_lock(mem_gb=args.mem_gb)

    run = command(args.model, args.port, args.width)
    if not os.path.exists(run[0]):
        sys.exit("vllm-mlx is not installed (uv tool install rapid-mlx)")
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}      # it runs in its own environment
    server = subprocess.Popen(run, env=env)
    guard(server, args.floor_gb, on_kill=lambda why: print(f"[swarm-serve] {why}; server stopped", file=sys.stderr, flush=True))
    signal.signal(signal.SIGINT, signal.default_int_handler)     # even if started with interrupts switched off
    signal.signal(signal.SIGTERM, lambda *_: server.send_signal(signal.SIGINT))
    print(f"[swarm-serve] {MODELS.get(args.model, args.model)} at http://127.0.0.1:{args.port}/v1 once it says Ready "
          f"(ctrl-c to stop). Requests must ask for thinking: see `swarm_engine.serve.chat`.", file=sys.stderr, flush=True)
    try:
        while server.poll() is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        server.send_signal(signal.SIGINT)
        try:
            server.wait(timeout=30)
        except subprocess.TimeoutExpired:
            server.kill()
    sys.exit(server.returncode or 0)


if __name__ == "__main__":
    main()
