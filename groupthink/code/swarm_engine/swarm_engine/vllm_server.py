"""A vLLM server for one model on this machine's GPU: installing vLLM, sharing out the GPU's memory, starting and stopping.

    swarm-vllm install                    # vLLM, in an environment of its own at ~/.swarm/vllm
    swarm-vllm serve --model 9B-bf16      # serves until it is told to stop; callers find it at SWARM_VLLM_URL
    swarm-vllm plan --model 9B-bf16       # what it would be started with on this GPU, and why
    swarm-vllm check --model 9B-bf16      # hold the engine against the live server, and time it (vllm_check.py)

`vllm.Engine` starts a server by itself when none is named, and stops it when the process ends. A job that makes
several runs starts one first (`swarm-vllm serve`), so that the model is loaded once.

vLLM is not installed beside this package: it brings its own PyTorch and CUDA, several gigabytes of them, and
lives in an environment of its own. It is looked for at SWARM_VLLM_BIN, at ~/.swarm/vllm/bin/vllm (where `install`
puts the pinned version), and then on the PATH.

A server is started in a session of its own and stopped as a whole (vLLM is several processes): when the engine
that started it ends, when that process is told to stop (SIGTERM, SIGHUP), and by `stop`. One that is found
already answering on the port is never taken for the one that was started: starting refuses, and says so.

The version is pinned (`VERSION`). 0.31.0 is the first in which a conversation's next call finds what the server
kept of it for this model (0.29 and 0.30 lost it every turn: vLLM's pull request 59146), so do not go below it;
and after going above it, `swarm-vllm check` before trusting a run.
"""
from __future__ import annotations

import argparse
import atexit
import json
import os
import shlex
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

VERSION = "0.31.0"        # of vLLM
PORT = 8000
SPARE_GB = 2.0            # of a GPU's memory, what is left alone: the CUDA context and what a step of the model needs
USE = 0.92                # the share of a GPU's memory vLLM is given (its own default)
USE_SMALL = 0.88          # on a GPU of 24 GiB or less: vLLM does not count all it will need when it starts with this
                          # model (its issue 54775: a server on a 24 GB card ran out of memory later)
LIVE_TOKENS = 8000        # a conversation in flight is planned at this length: agents at desks reach 5,000 to 20,000
SNAPSHOTS = 3             # how many copies of its linear-attention state a conversation in flight holds, at most
LONGEST = 65536           # the longest prompt and reply together a server is asked to take, for a model that does not say
SHORTEST = 4096           # and the least a server is worth starting for
HOME = Path("~/.swarm").expanduser()
PLANNED = {"--gpu-memory-utilization": ("gpu_memory_utilization", float), "--max-num-seqs": ("max_num_seqs", int),
           "--max-model-len": ("max_model_len", int), "--max-num-batched-tokens": ("max_num_batched_tokens", int)}


def find() -> str | None:
    """The vLLM program, or None if there is none here."""
    named = os.environ.get("SWARM_VLLM_BIN")
    if named:                                                   # by its whole path: where it lies is where its tools are looked for
        return os.path.abspath(named) if os.access(named, os.X_OK) else None
    pinned = HOME / "vllm/bin/vllm"                             # what `install` put there, before whatever is on the PATH
    return str(pinned) if os.access(pinned, os.X_OK) else shutil.which("vllm")


def footprint(config: dict) -> tuple[int, int]:
    """What one conversation in flight holds on the GPU, from the model's config.json: bytes per token (the keys
    and values of the layers that keep an attention cache, two bytes a number) and bytes for one copy of the
    state of the linear-attention layers of Qwen3.5 (four bytes a number). For the 9B that is 32 KB a token and
    48 MB, which is what the Mac engine reads off a loaded model. vLLM keeps two or three such copies for a
    conversation in flight, and one for each place in a conversation it can take up again."""
    text = config.get("text_config", config)
    layers = text.get("num_hidden_layers", 0)
    kinds = text.get("layer_types") or ["full_attention"] * layers
    heads = text.get("num_key_value_heads") or text.get("num_attention_heads") or 0
    width = text.get("head_dim") or (text.get("hidden_size", 0) // max(text.get("num_attention_heads") or 1, 1))
    per_token = kinds.count("full_attention") * 2 * heads * width * 2
    fixed = (kinds.count("linear_attention") * text.get("linear_num_value_heads", 0) * text.get("linear_key_head_dim", 0)
             * text.get("linear_value_head_dim", 0) * 4)
    return per_token, fixed


def plan(gpu_gb: float, weights_gb: float, config: dict, use: float | None = None) -> dict:
    """What a server is started with on a GPU of `gpu_gb` GiB: the share of its memory, the most conversations
    it writes side by side, and the longest it takes. What is left after the weights is room for conversations;
    each in flight is counted at `LIVE_TOKENS`. More may be sent than are written side by side: the rest wait
    their turn in the server. The longest prompt and reply together is the model's own limit, as on the Mac,
    or half the room where that is less. `use` is the share of the GPU's memory, if the caller says (then
    SWARM_VLLM_GPU_USE, then vLLM's own). These are starting values, not measurements: `swarm-vllm check`
    reports what a server did with them."""
    use = float(use or os.environ.get("SWARM_VLLM_GPU_USE") or (USE if gpu_gb > 24 else USE_SMALL))
    per_token, fixed = footprint(config)
    room = gpu_gb * use - weights_gb - SPARE_GB
    tokens = int(room * 2**30 / per_token) if per_token else 0
    text = config.get("text_config", config)
    longest = min(text.get("max_position_embeddings") or LONGEST, tokens // 2 // 1024 * 1024)
    if not per_token:
        raise ValueError("the model's config.json does not say what a conversation holds (no layers in it)")
    if room <= 0 or longest < SHORTEST:
        raise ValueError(f"{weights_gb:g} GiB of weights leave no room for conversations on {use:.0%} of a GPU of {gpu_gb:g} GiB"
                         + (f" ({tokens:,} tokens of it)" if room > 0 else ""))
    side_by_side = int(os.environ.get("SWARM_VLLM_SEQS") or 0) or int(room * 2**30 / (SNAPSHOTS * fixed + per_token * LIVE_TOKENS))
    return {"gpu_gb": gpu_gb, "gpu_memory_utilization": use, "room_gb": round(room, 1), "room_tokens": tokens,
            "max_num_seqs": max(2, min(side_by_side, 512)), "max_model_len": longest,
            # tokens the server takes in one step, read and written together: vLLM's own are 8,192 on a GPU of
            # 70 GiB and more and 2,048 below, which is slow where long conversations are read again
            "max_num_batched_tokens": 16384 if gpu_gb >= 70 else 8192 if gpu_gb >= 30 else 4096}


def overrides(arguments: list[str]) -> tuple[dict, list[str]]:
    """Of extra vLLM arguments (SWARM_VLLM_ARGS): those that change what `plan` plans, as its settings, and the
    rest. They are taken into the plan, so that what a run records of its server is what the server ran with."""
    given, rest, at = {}, [], 0
    while at < len(arguments):
        flag, _, value = arguments[at].partition("=")
        if flag in PLANNED:
            if not value and at + 1 < len(arguments):
                at, value = at + 1, arguments[at + 1]
            name, kind = PLANNED[flag]
            given[name] = kind(value)
        else:
            rest.append(arguments[at])
        at += 1
    return given, rest


class Server:
    """One model served by vLLM on this machine, on 127.0.0.1. Started here, and stopped when this process ends."""

    def __init__(self, path: Path, name: str, *, config: dict | None = None, weights_gb: float = 0.0, dtype: str = "",
                 port: int | None = None, say=print, **settings):
        """`settings` are `plan`'s own, given by the caller: gpu_memory_utilization, max_num_seqs, max_model_len.
        They come before what SWARM_VLLM_ARGS says of the same, and that before what `plan` works out. The share
        of the GPU's memory is settled first: everything else is counted from the room it leaves."""
        from .vllm import gpu
        self.path, self.name, self.dtype, self.say = Path(path), name, dtype, say
        self.port = port or int(os.environ.get("SWARM_VLLM_PORT") or PORT)
        self.gpu = gpu()
        if not self.gpu:
            raise RuntimeError("no GPU here to serve a model on (nvidia-smi names none)")
        weights = weights_gb or sum(f.stat().st_size for f in self.path.glob("*.safetensors")) / 2**30
        self.text_only = "vision_config" in (config or {})      # a model with a vision tower is served without it
        given, self.extra = overrides(shlex.split(os.environ.get("SWARM_VLLM_ARGS", "")))
        given |= {k: v for k, v in settings.items() if v is not None}
        self.planned = plan(self.gpu["memory_gb"], weights, config or {}, use=given.get("gpu_memory_utilization")) | given
        self.process: subprocess.Popen | None = None
        self.log = Path(os.environ.get("SWARM_LOGS") or HOME / "logs").expanduser() / f"vllm-{self.port}.log"

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def command(self) -> list[str]:
        """The vLLM command line. What a request says of how a reply is drawn is all that draws it: a model
        repository's own defaults are switched off (`--generation-config vllm`). The vision tower of Qwen3.5 is
        not loaded (`--language-model-only`): agents send text. The server says how much of a prompt it still
        held (`--enable-prompt-tokens-details`), which is what a run's log counts as not read again. What
        SWARM_VLLM_ARGS says beyond the plan is added at the end."""
        planned = self.planned
        return [find() or "vllm", "serve", str(self.path), "--served-model-name", self.name, "--host", "127.0.0.1",
                "--port", str(self.port), "--gpu-memory-utilization", f"{planned['gpu_memory_utilization']:g}",
                "--max-num-seqs", str(planned["max_num_seqs"]), "--max-model-len", str(planned["max_model_len"]),
                "--max-num-batched-tokens", str(planned["max_num_batched_tokens"]),
                "--generation-config", "vllm", "--enable-prompt-tokens-details",
                *(["--language-model-only"] if self.text_only else []),
                *(["--dtype", self.dtype] if self.dtype else []), *self.extra]

    @staticmethod
    def environment(program: str) -> dict:
        """What the server is started with around it: its own environment, as one that is activated has it, and
        not the caller's. The folder its program lies in comes first on the PATH, because what vLLM is installed
        with calls its tools by name: FlashInfer, which draws the tokens, builds its sampler with `ninja` the
        first time a server starts, and a server that cannot find it stops there (seen on the first rented A10,
        2026-10-11)."""
        env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "PYTHONPATH")}
        program = os.path.abspath(program) if os.sep in program else shutil.which(program) or program
        if os.path.isabs(program):
            # where the program really lies first (a link to it on the PATH, as `uv tool` leaves one, has its tools
            # there and not beside the link), then where it was found
            folders = list(dict.fromkeys([os.path.dirname(os.path.realpath(program)), os.path.dirname(program)]))
            env["PATH"] = os.pathsep.join([*folders, env.get("PATH") or os.defpath])
            for folder in folders:
                if os.path.exists(os.path.join(os.path.dirname(folder), "pyvenv.cfg")):
                    env["VIRTUAL_ENV"] = os.path.dirname(folder)
                    break
        return env | {"VLLM_NO_USAGE_STATS": "1", "DO_NOT_TRACK": "1", "HF_HUB_OFFLINE": "1"}

    def taken(self) -> bool:
        """Whether something listens on the port already."""
        try:
            socket.create_connection(("127.0.0.1", self.port), timeout=2.0).close()
            return True
        except OSError:
            return False

    def start(self, timeout: float = 1800.0) -> str:
        """Start the server and wait until it answers. Returns its address. It is the server this started that
        has to answer: if something is on the port already (a server a run that was killed left behind, or one
        started by hand), nothing is started, since its settings would not be these and stopping would not
        stop it."""
        import httpx
        if find() is None:
            raise RuntimeError("vLLM is not installed here: it is looked for at SWARM_VLLM_BIN, at "
                               f"{HOME / 'vllm/bin/vllm'} and on the PATH (swarm-vllm install)")
        if self.taken():
            raise RuntimeError(f"something answers at {self.url} already. If it is a vLLM server for this model, name it "
                               f"(SWARM_VLLM_URL={self.url}); if a run left it behind, stop it (pkill -INT -f 'vllm serve'); "
                               "or take another port (SWARM_VLLM_PORT)")
        command = self.command()
        self.log.parent.mkdir(parents=True, exist_ok=True)
        env = self.environment(command[0])
        self.say(f"starting vLLM on {self.gpu['name']} ({self.gpu['memory_gb']:g} GiB): room for {self.planned['room_tokens']:,} "
                 f"tokens of conversation, {self.planned['max_num_seqs']} side by side, {self.planned['max_model_len']:,} the "
                 f"longest. Its log: {self.log}")
        started = time.time()
        with open(self.log, "ab") as log:
            log.write(f"\n==== {time.strftime('%Y-%m-%d %H:%M:%S')} {shlex.join(command)}\n".encode())
            log.flush()
            self.process = subprocess.Popen(command, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                            start_new_session=True)      # a group of its own: it is stopped as a whole
        atexit.register(self.stop)
        self.stop_when_told()
        while time.time() - started < timeout:
            if self.process.poll() is not None:
                raise RuntimeError(f"vLLM stopped while starting (code {self.process.returncode}). The end of {self.log}:\n{self.tail()}")
            try:
                if httpx.get(f"{self.url}/health", timeout=5.0).status_code == 200:
                    self.say(f"vLLM is up at {self.url} after {time.time() - started:.0f}s")
                    return self.url
            except httpx.HTTPError:
                pass
            time.sleep(2.0)
        self.stop()
        raise RuntimeError(f"vLLM did not answer within {timeout:.0f}s. The end of {self.log}:\n{self.tail()}")

    def tail(self, lines: int = 30) -> str:
        try:
            return "\n".join(self.log.read_text(errors="replace").splitlines()[-lines:])
        except OSError:
            return "(no log)"

    def stop_when_told(self):
        """A process that is told to stop (SIGTERM, SIGHUP) ends without running what `atexit` holds: stop the
        server first, then end as it would have. Only where nothing else has taken the signal already."""
        if threading.current_thread() is not threading.main_thread():
            return

        def told(number, _frame):
            self.stop()
            signal.signal(number, signal.SIG_DFL)
            os.kill(os.getpid(), number)

        for number in (signal.SIGTERM, signal.SIGHUP):
            if signal.getsignal(number) is signal.SIG_DFL:
                signal.signal(number, told)

    def stop(self, grace: float = 30.0):
        """Stop the server and everything it started: asked first, as ctrl-c would, then made to. It takes no
        longer than `grace` and a few seconds (a server that has hung does not answer the asking)."""
        process, self.process = self.process, None
        if process is None:
            return
        for number, wait in ((signal.SIGINT, grace), (signal.SIGKILL, 10.0)):
            try:
                os.killpg(process.pid, number)                  # it leads a group of its own (`start`)
            except OSError:                                     # nothing of it is left
                break
            try:
                process.wait(timeout=wait)
            except subprocess.TimeoutExpired:
                continue
            if number == signal.SIGINT:                         # it has gone: see that what it started has too
                time.sleep(0.5)
        process.poll()


def room(model: str) -> dict | None:
    """What a server for `model` is started with on this machine's GPU, as `plan` has it: "room_tokens", the
    tokens of conversation it holds, and "max_num_seqs", the conversations it writes side by side, among the
    rest. None where there is no GPU, or the model's files are not on this machine yet: a caller then keeps
    its own defaults. A server that somebody started with settings of their own has those, not these."""
    from huggingface_hub import snapshot_download

    from .models import KNOWN
    from .vllm import gpu
    card, known, folder = gpu(), KNOWN.get(model), Path(model).expanduser()
    if not card or (known is not None and known.backend != "vllm"):
        return None
    try:
        path = folder if folder.is_dir() else Path(snapshot_download(known.repo if known else model, allow_patterns=["config.json"],
                                                                     revision=known.revision if known else None, local_files_only=True))
        config = json.loads((path / "config.json").read_text())
        weights = (known.weights_gb if known else 0.0) or sum(f.stat().st_size for f in path.glob("*.safetensors")) / 2**30
        return plan(card["memory_gb"], weights, config)
    except Exception:                                          # no files here, or a model whose config says nothing of its layers
        return None


def capacity(model: str) -> int | None:
    """How many conversations a server for `model` writes side by side on this machine's GPU, as `plan` has it
    (SWARM_VLLM_SEQS overrides, for the server and for whoever asks here). None where there is no GPU, or the
    model's files are not on this machine yet: a caller then keeps its own defaults.

    It is what a run should have open at once when its conversations are as long as the plan counts them
    (`LIVE_TOKENS`). Fewer leaves the GPU with less to do than it could; more than its room holds (`room`), and
    the server drops what it kept of the conversations that are not being written, and reads them again."""
    planned = room(model)
    return planned["max_num_seqs"] if planned else None


def driver() -> str | None:
    """The NVIDIA driver's version here ("570.133.20"), or None if there is none."""
    try:
        return subprocess.run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"], capture_output=True,
                              text=True, timeout=20).stdout.strip().splitlines()[0].strip() or None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def install_commands(driver_version: str | None, machine: str, home: Path = HOME) -> list[list[str]]:
    """What installs vLLM into an environment of its own. The wheel on PyPI is built for CUDA 13, which needs
    driver 580 or newer; for an older driver (a rented machine may have 570) vLLM publishes the same version
    built for CUDA 12.9. `--torch-backend` has uv take PyTorch and what goes with it from PyTorch's own index
    for that CUDA, and everything else from PyPI."""
    env = str(home / "vllm")
    try:
        series = int((driver_version or "").split(".")[0])
    except ValueError:
        raise RuntimeError("no NVIDIA driver here to install vLLM for (nvidia-smi names none)") from None
    if series >= 580:
        package = [f"vllm=={VERSION}", "--torch-backend=auto"]
    else:
        machine = {"amd64": "x86_64", "arm64": "aarch64"}.get(machine, machine)
        package = [f"https://github.com/vllm-project/vllm/releases/download/v{VERSION}/vllm-{VERSION}+cu129-cp38-abi3-"
                   f"manylinux_2_28_{machine}.whl", "--torch-backend=cu129"]
    # `--allow-existing`: an install that was cut short, or an older version, is carried on over, not refused
    return [["uv", "venv", env, "--python", "3.12", "--seed", "--managed-python", "--allow-existing"],
            ["uv", "pip", "install", "--python", f"{env}/bin/python", *package]]


def install(say=print) -> str:
    """Install vLLM, unless the pinned version is there already. Returns the program's path."""
    import platform
    program = HOME / "vllm/bin/vllm"
    if program.exists():
        there = subprocess.run([str(HOME / "vllm/bin/python"), "-c", "import vllm; print(vllm.__version__)"],
                               capture_output=True, text=True).stdout.strip()
        if there.split("+")[0] == VERSION:
            say(f"vLLM {there} is installed at {program}")
            return str(program)
    for command in install_commands(driver(), platform.machine().lower()):
        say(shlex.join(command))
        subprocess.run(command, check=True)
    return str(program)


def resolve(model: str) -> tuple[Path, dict, float, str]:
    """A model's folder (downloaded if need be), its config, the size of its weights and the precision it is served in."""
    from huggingface_hub import snapshot_download

    from .models import KNOWN
    known = KNOWN.get(model)
    if known is not None and known.backend != "vllm":
        raise SystemExit(f"{model} is the build that runs on a Mac; on a GPU the model is {model}-bf16")
    folder = Path(model).expanduser()
    path = folder.resolve() if folder.is_dir() else Path(snapshot_download(known.repo if known else model,
                                                                             revision=known.revision if known else None))
    config = json.loads((path / "config.json").read_text()) if (path / "config.json").exists() else {}
    return path, config, known.weights_gb if known else 0.0, known.dtype if known else ""


def main():
    parser = argparse.ArgumentParser(prog="swarm-vllm", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, about in (("serve", "serve a model until told to stop"), ("plan", "what a server would be started with here")):
        sub = commands.add_parser(name, help=about)
        sub.add_argument("--model", default="9B-bf16", help='"4B-bf16", "9B-bf16", a Hugging Face repository or a folder')
        sub.add_argument("--port", type=int)
        sub.add_argument("--max-num-seqs", type=int, help="conversations written side by side (default: from the GPU's memory)")
        sub.add_argument("--max-model-len", type=int, help="the longest prompt and reply together (default: from the GPU's memory)")
        sub.add_argument("--gpu-memory-utilization", type=float, help=f"the share of the GPU's memory (default {USE})")
    commands.add_parser("install", help=f"install vLLM {VERSION} into an environment of its own ({HOME / 'vllm'})")
    check = commands.add_parser("check", help="hold the engine against a live server, and time it")
    check.add_argument("--model", default="9B-bf16")
    check.add_argument("--out", help="write what was found to this file")
    check.add_argument("--widths", type=int, nargs="*", default=[8, 32, 128], help="calls in flight at once, for the timing")
    args = parser.parse_args()
    if args.command == "install":
        install(say=lambda line: print(f"[swarm-vllm] {line}", file=sys.stderr, flush=True))
        return
    if args.command == "check":
        from .vllm_check import main as check_main
        sys.exit(check_main(args))
    from .vllm import gpu
    if not gpu():                                             # before the model's files are fetched for nothing
        sys.exit("no GPU here to serve a model on (nvidia-smi names none)")
    path, config, weights, dtype = resolve(args.model)
    server = Server(path, args.model, config=config, weights_gb=weights, dtype=dtype, port=args.port,
                    max_num_seqs=args.max_num_seqs, max_model_len=args.max_model_len,
                    gpu_memory_utilization=args.gpu_memory_utilization, say=lambda line: print(f"[swarm-vllm] {line}", file=sys.stderr, flush=True))
    if args.command == "plan":
        print(json.dumps(server.planned | {"gpu": server.gpu, "command": server.command()}, indent=2))
        return
    def told_to_stop(_signal, _frame):
        raise KeyboardInterrupt

    for number in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(number, told_to_stop)
    code = 0
    try:
        url = server.start()
        print(f"[swarm-vllm] {args.model} at {url}: export SWARM_VLLM_URL={url} (ctrl-c to stop)", file=sys.stderr, flush=True)
        while server.process is not None and server.process.poll() is None:
            time.sleep(1.0)
        code = server.process.returncode if server.process is not None else 0
    except KeyboardInterrupt:
        pass
    finally:
        for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):      # told again while it stops: it is stopping
            signal.signal(number, signal.SIG_IGN)
        server.stop()
    sys.exit(code or 0)


if __name__ == "__main__":
    main()
