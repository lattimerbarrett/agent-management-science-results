"""The engine on a GPU: the calls engine.py takes, answered by a vLLM server.

    from swarm_engine import backend
    engine = backend("9B-bf16")          # starts a vLLM server on this machine's GPU, or uses the one at SWARM_VLLM_URL
    engine.converse(openings, seeds, respond, thinking=1024, max_tokens=1536, tools=tools)

On the Mac the engine is the batch: it plans memory, reads shared starts once, and keeps each conversation's
cache. vLLM does all of that itself (it batches whatever is in flight and keeps what it has read in its prefix
cache), so nothing is planned here. What is kept the same is what a call *is*:

    the prompt     the chat template's text, cut into tokens by the same tokenizer, and sent as token ids
    the thought    one request: from the prompt to `</think>`, an end of turn, or the thought's budget
    the answer     a second request: from there (the thought as the model closed it, or closed with the words
                   Qwen is given when its time is up) to an end of turn, or the answer's limit

Two requests are what give a thought a budget and a sampling policy of its own, as `thinking=N` and
`thought_sampling` do on the Mac. The second begins with everything the first read and wrote; how much of that
the server still holds, and so how much the second has to read again, is the server's affair (`answer_read_tokens`
in a run's usage says how much it was, and `swarm-vllm check` reports it). A reply comes back with the same
fields, the same finish reasons and the same token counts as engine.py gives, and ends on the same tokens: the
tokenizer's end of turn, and what the model's own files name at the top of config.json or in
generation_config.json, which is how mlx-lm reads them for the Mac engine. (Qwen3.5 names `<|endoftext|>` only
under `text_config`, where neither looks: on both, a reply ends on `<|im_end|>` and on nothing else.)

What is counted as read and as not read again is the prompt of a call, as on the Mac: what the server held of
it when the call's first request arrived is `carried_tokens`, and the rest was read. That the answer's request
finds the thought's request in the server is not counted as anything carried.

What differs, and cannot be made the same:
  - The model is another build (Qwen's bfloat16 weights, not a 4-bit conversion): models.py.
  - A seed fixes a call's random draws here too, but they are vLLM's draws, not MLX's: the same call does not
    come out the same on the two.
  - A presence penalty counts the tokens its own request wrote. So on the answer it does not count the
    thought's tokens, as it does on the Mac. A repetition penalty is further off: vLLM counts the prompt's
    tokens too, where the Mac counts only what the call wrote. With the answer drawn without penalties
    (`Sampling.coding()`), as the agents of math_swarm_explore are, there is nothing to count and the two agree;
    a repetition penalty other than 1 has not been used on either.

`converse` keeps its word from engine.py: each conversation at its own pace, `respond` on worker threads, a
conversation that waits for another (`respond` returns a Future), replies the caller already has (`known`), and
an error rather than a hang when every conversation left waits for another.

A server that ends a reply for a reason this engine did not ask for (vLLM can cut one that goes round in
circles, when a request asks it to; none here does) is an error, not a reply cut short.

Nothing here has been run against a real server on this Mac: tests/test_vllm.py plays a stand-in for one, and
`swarm-vllm check` holds the engine against a live server on the GPU machine.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import platform
import secrets
import time
from concurrent.futures import CancelledError as Cancelled
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np

from .common import OUT_OF_TIME, Prompt, Reply, stream
from .models import KNOWN
from .settings import Sampling, integer

URL = "SWARM_VLLM_URL"            # a server that is already up: http://127.0.0.1:8000
WIDTH = "SWARM_VLLM_WIDTH"        # the most calls in flight at once, when the caller does not say
STALL = "SWARM_VLLM_STALL"        # seconds without any answer, with calls in flight, after which a run gives up
TOKENIZER_FILES = ["*.json", "*.jinja", "*.txt", "tokenizer.model", "*.tiktoken"]
TRIES = 6                         # how often a request is sent again when the server does not answer it
BACKOFF = 1.0                     # seconds before the first of those, doubled each time (a test sets it to 0)
STALLED = 1200.0                  # the default for STALL: a reply takes a minute or two, and waits its turn for a few more


@dataclass(frozen=True)
class _Policy:
    """How every reply of one `generate` or `converse` is drawn and where it ends."""
    thinking: int | None
    max_tokens: int
    total: int                    # the most tokens one reply may come to, the engine's own words included
    sampling: Sampling
    thought_sampling: Sampling


def ends_named(path: Path) -> set[int]:
    """The tokens a model's own files name as ending a reply, besides the tokenizer's end of turn, read as mlx-lm
    reads them for the Mac engine: `eos_token_id` at the top of config.json, or generation_config.json's in its
    place."""
    named = None
    for name in ("config.json", "generation_config.json"):
        try:
            named = json.loads((Path(path) / name).read_text()).get("eos_token_id") or named
        except (OSError, ValueError, AttributeError):
            continue
    return {named} if isinstance(named, int) else {token for token in named or () if isinstance(token, int)}


class Engine:
    def __init__(self, model: str = "9B-bf16", *, width: int | None = None, url: str | None = None,
                 revision: str | None = None, say=print):
        """`model` is a name models.py gives to vLLM ("4B-bf16", "9B-bf16"), a Hugging Face repository, or a
        folder. `url` is a vLLM server that is already serving it (or SWARM_VLLM_URL); without one, a server is
        started on this machine's GPU and stopped with this engine. `width` is the most calls in flight at
        once: the server runs as many of them side by side as it has room for, and lines the rest up."""
        import httpx                                           # with transformers: all this backend needs, and neither is MLX
        from huggingface_hub import snapshot_download
        from transformers import AutoTokenizer

        if width is not None:
            integer("width", width, 1)
        known = KNOWN.get(model)
        if known is not None and known.backend != "vllm":
            raise ValueError(f"{model} is the build that runs on a Mac ({known.repo}); on a GPU the model is {model}-bf16")
        self.alias, self.say, self.server = model, say, None
        url = (url or os.environ.get(URL) or "").rstrip("/")
        self.machine = gpu()
        if not url:                                            # a server has to be started here: can one be, before
            from .vllm_server import find                      # gigabytes of weights are fetched for it
            if not self.machine:
                raise RuntimeError(f"no GPU here to serve {model} on (nvidia-smi names none), and no server is named ({URL})")
            if find() is None:
                raise RuntimeError("vLLM is not installed here (swarm-vllm install), and no server is named "
                                   f"({URL})")
        folder = Path(model).expanduser()
        if folder.is_dir():
            if revision is not None:
                raise ValueError("revision applies to Hugging Face repositories, not local directories")
            self.name, self.revision, path = str(folder.resolve()), None, folder.resolve()
        else:
            self.name = known.repo if known else model
            wanted = revision or (known.revision if known else None)
            path = Path(snapshot_download(self.name, revision=wanted, allow_patterns=None if not url else TOKENIZER_FILES))
            self.revision = path.name
        self.model_path = path
        self.tokenizer = AutoTokenizer.from_pretrained(str(path))
        self.artifact_hashes = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                               for f in path.iterdir() if f.suffix in (".json", ".jinja", ".model", ".tiktoken")}
        self._source_hash = hashlib.sha256(b"".join(Path(__file__).with_name(name).read_bytes()
                                                    for name in ("vllm.py", "common.py", "settings.py"))).hexdigest()
        self.versions = {}
        for package in ("httpx", "numpy", "transformers", "tokenizers", "huggingface-hub", "swarm-engine"):
            try:
                self.versions[package] = version(package)
            except PackageNotFoundError:
                pass
        self.end_of_turn = self.tokenizer.eos_token_id
        close = self.encode_text("</think>")
        self.close = close[0] if len(close) == 1 else None      # None: the model has no thinking mode we can drive
        self._out_of_time = self.encode_text(OUT_OF_TIME)
        self.end_tokens = {self.end_of_turn} | ends_named(path)   # as engine.py has them, through mlx-lm
        if not url:
            from .vllm_server import Server
            config = json.loads((path / "config.json").read_text()) if (path / "config.json").exists() else {}
            self.server = Server(path, model, config=config, weights_gb=known.weights_gb if known else 0.0,
                                 dtype=known.dtype if known else "", say=say)
            url = self.server.start()
        self.url = url
        self._httpx = httpx
        self.served, self.context_limit, self.vllm_version = self._hello()
        from .vllm_server import VERSION
        if self.vllm_version and self.vllm_version.split("+")[0] != VERSION:
            say(f"the server at {url} is vLLM {self.vllm_version}; this engine is held against {VERSION}: "
                "run `swarm-vllm check` before trusting a run")
        self.width = width or int(os.environ.get(WIDTH) or 0) or 2 * self._side_by_side()
        self.stall, self._heard = float(os.environ.get(STALL) or STALLED), time.monotonic()
        self.calls = self.new_tokens = self.read_tokens = self.spared_tokens = self.answer_read_tokens = 0
        self.sampled_tokens = self.injected_tokens = self.prompt_tokens = 0
        self.last_run: dict = {}
        self.seconds = 0.0
        self.groups: list[int] = []           # the most calls that were in flight at once in the last run

    # ---------------------------------------------------------------- the server
    def _hello(self) -> tuple[str, int | None, str | None]:
        """The name this model has on the server, the longest prompt and reply together it takes, and the
        server's version. An error if the server is not serving this model."""
        httpx = self._httpx
        try:
            listed = httpx.get(f"{self.url}/v1/models", timeout=30.0)
            listed.raise_for_status()
        except httpx.HTTPError as problem:
            raise RuntimeError(f"no vLLM server answers at {self.url} ({problem})") from None
        models = listed.json().get("data", [])
        wanted = {self.alias, self.name, str(self.model_path)}
        mine = next((m for m in models if m.get("id") in wanted), None) or next((m for m in models if m.get("root") in wanted), None)
        if mine is None:
            raise RuntimeError(f"the vLLM server at {self.url} serves {', '.join(str(m.get('id')) for m in models) or 'nothing'}, "
                               f"not {self.alias}")
        try:
            told = httpx.get(f"{self.url}/version", timeout=30.0)
            server_version = told.json().get("version") if told.status_code == 200 else None
        except (httpx.HTTPError, ValueError):
            server_version = None
        return mine["id"], mine.get("max_model_len"), server_version

    def _side_by_side(self) -> int:
        """How many conversations the server writes side by side: as it was started here, as a server on this
        machine's GPU is planned (one that something else started for this model), or a guess for one that is
        somewhere else. Twice that many calls are kept in flight, so that the server always has the next one."""
        if self.server is not None:
            return self.server.planned["max_num_seqs"]
        from .vllm_server import capacity
        return capacity(self.alias) or 128

    def close_server(self):
        """Stop the server, if this engine started it."""
        if self.server is not None:
            self.server.stop()
            self.server = None

    def describe(self) -> dict:
        """The settings a run's log should record."""
        return {"backend": "vllm", "model": self.name, "revision": self.revision, "model_path": str(self.model_path),
                "served_as": self.served, "url": self.url, "vllm": self.vllm_version,
                "server": self.server.planned | {"command": self.server.command()} if self.server else None,
                "artifact_sha256": self.artifact_hashes, "versions": self.versions, "source_sha256": self._source_hash,
                "python": platform.python_version(), "system": f"{platform.system()} {platform.machine()}",
                "machine": self.machine.get("name"), "context_limit": self.context_limit, "width": self.width}

    # ---------------------------------------------------------------- prompts
    def encode(self, prompt: Prompt, thinking: bool = False, tools: list[dict] | None = None) -> list[int]:
        """Token ids of a chat prompt that ends where the model's reply starts. `tools` are function schemas:
        the chat template describes them to the model in the model's own tool-call format."""
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        elif isinstance(prompt, tuple):
            messages = [{"role": "system", "content": prompt[0]}, {"role": "user", "content": prompt[1]}]
        else:
            messages = prompt
        text = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=thinking,
                                                  tokenize=False, **({"tools": tools} if tools else {}))
        return self.encode_text(text)

    def encode_text(self, text: str) -> list[int]:
        return self.tokenizer.encode(text, add_special_tokens=False)

    # ---------------------------------------------------------------- settings
    def _policy(self, thinking, max_tokens, max_total_tokens, sampling, thought_sampling) -> _Policy:
        for name, value in (("max_tokens", max_tokens), ("max_total_tokens", max_total_tokens)):
            integer(name, value, 1)
        if thinking is not None:
            integer("thinking", thinking)
        sampling = sampling if sampling is not None else Sampling()
        thought_sampling = thought_sampling if thought_sampling is not None else sampling
        if not isinstance(sampling, Sampling) or not isinstance(thought_sampling, Sampling):
            raise ValueError("sampling and thought_sampling must be Sampling configurations")
        if thinking != 0 and self.close is None:
            raise ValueError(f"{self.name} has no </think> token; use thinking=0")
        return _Policy(thinking, max_tokens, self._allowance(thinking, max_tokens, max_total_tokens), sampling, thought_sampling)

    def _allowance(self, thinking: int | None, max_tokens: int, max_total_tokens: int) -> int:
        """The most tokens one reply may come to (as engine.py counts it)."""
        if thinking is None:
            return max_total_tokens
        return min(max_total_tokens, (thinking + len(self._out_of_time) if thinking else 0) + max_tokens + 1)

    def _fits(self, context: list[int], total: int, who: str) -> list[int]:
        if self.context_limit is not None and len(context) + total > self.context_limit:
            raise ValueError(f"{who}: prompt + output allowance exceeds context limit {self.context_limit}")
        return context

    def _sent(self, flying: int):
        """A call goes to the server, `flying` with it. When it is the only one, the time since the server was
        last heard starts now: nothing was asked of it before, so its silence till now was not silence."""
        if flying == 1:
            self._heard = time.monotonic()

    async def _watch(self, flying):
        """Give up on a server that has stopped answering: with calls in flight and nothing heard for `stall`
        seconds, the run ends with an error instead of waiting for ever (vLLM has hung under load with this
        model: its issue 37729). Replies are kept by the caller, so the same run carries on from where it was.
        The time counts while calls are in flight, not while tools run or known replies are replayed."""
        while True:
            await asyncio.sleep(min(5.0, max(self.stall / 4, 0.01)))
            if flying() and time.monotonic() - self._heard > self.stall:
                raise RuntimeError(f"the vLLM server at {self.url} has answered nothing for {self.stall:.0f} seconds, "
                                   f"with {flying()} calls in flight")

    def _client(self):
        httpx = self._httpx
        return httpx.AsyncClient(timeout=httpx.Timeout(None, connect=30.0),      # a call waits its turn on the server: no limit
                                 limits=httpx.Limits(max_connections=self.width + 8, max_keepalive_connections=self.width + 8))

    # ---------------------------------------------------------------- one call
    async def _complete(self, client, prompt: list[int], limit: int, stops: set[int], sampling: Sampling,
                        seed: int) -> tuple[list[int], int | None, int, int]:
        """One request to the server: what it wrote after `prompt` (without the token that stopped it), the
        token that stopped it (None if `limit` did), how many tokens of the prompt it read, and how many it
        still held from before."""
        httpx = self._httpx
        body = {"model": self.served, "prompt": prompt, "max_tokens": limit, "stop_token_ids": sorted(stops), "seed": seed,
                "temperature": sampling.temperature, "top_p": sampling.top_p, "top_k": sampling.top_k,
                "min_p": sampling.min_p, "presence_penalty": sampling.presence_penalty,
                "repetition_penalty": sampling.repetition_penalty, "skip_special_tokens": False,
                "spaces_between_special_tokens": False, "add_special_tokens": False, "return_token_ids": True,
                "stream": False, "n": 1}
        problem = None
        for attempt in range(TRIES):
            if attempt:
                await asyncio.sleep(min(2.0 ** attempt, 30.0) * BACKOFF)
            try:
                answered = await client.post(f"{self.url}/v1/completions", json=body)
            except httpx.TransportError as error:                # the server was not there, or hung up
                problem = f"{type(error).__name__}: {error}"
                continue
            if answered.status_code in (429, 500, 502, 503, 504):
                problem = f"HTTP {answered.status_code}: {answered.text[:300]}"
                continue
            if answered.status_code != 200:
                raise ValueError(f"the vLLM server refused a call (HTTP {answered.status_code}): {answered.text[:500]}")
            self._heard = time.monotonic()
            said = answered.json()
            choice, usage = said["choices"][0], said.get("usage") or {}
            tokens = choice.get("token_ids")
            if tokens is None:
                raise RuntimeError("the vLLM server did not say which tokens it wrote (`return_token_ids`): it is too old for this engine")
            tokens, why, stop = list(tokens), choice.get("finish_reason"), None
            if why == "stop":
                if tokens and tokens[-1] in stops:               # some versions leave the token that stopped it at the end
                    stop = tokens.pop()
                else:
                    named = choice.get("stop_reason")
                    stop = named if isinstance(named, int) and named in stops else self.end_of_turn
            elif why != "length":                                # nothing else is asked for, so nothing else is known how to read
                raise RuntimeError(f"the vLLM server ended a call with {why!r}")
            held = ((usage.get("prompt_tokens_details") or {}).get("cached_tokens")) or 0
            return tokens, stop, len(prompt) - held, held
        raise RuntimeError(f"the vLLM server at {self.url} did not answer a call in {TRIES} tries ({problem})")

    async def _one(self, client, context: list[int], seed: int, policy: _Policy) -> tuple[Reply, int, int]:
        """One call: the thought, then the answer. Returns the reply, the tokens of its prompt the server read
        and the tokens of it the server still held. What ends each part, and what is counted, is as engine.py
        has it: read and held are of the prompt, as its first request found it. What the answer's request had
        to read again of the prompt and the thought is counted by itself (`answer_read_tokens`)."""
        thinking, total = policy.thinking, policy.total
        thought: list[int] = []
        leaving: list[int] = []
        answer: list[int] = []
        emitted: list[int] = []
        injected_positions: list[int] = []
        closed_itself, ended_turn, stopped, finish, read, spared, again = None, False, False, None, None, 0, 0
        if thinking != 0:
            budget = total if thinking is None else min(thinking, total)
            written, stop, read, spared = await self._complete(client, context, budget, {self.close, *self.end_tokens},
                                                               policy.thought_sampling, stream(seed, context))
            thought = written + ([stop] if stop is not None else [])
            emitted += thought
            if stop == self.close:
                closed_itself = True
            elif stop is not None:                               # the model ended its turn inside the thought
                closed_itself, ended_turn, stopped, finish = False, True, True, "end_in_thought"
            elif thinking is None or len(emitted) >= total:
                closed_itself, finish = False, "total_limit"
            else:                                                # its budget is used up: the engine closes the thought
                closed_itself, leaving = False, self._out_of_time[:total - len(emitted)]
                injected_positions += range(len(emitted), len(emitted) + len(leaving))
                emitted += leaving
                if len(leaving) < len(self._out_of_time):
                    finish = "total_limit"
        if finish is None:
            room = min(policy.max_tokens, total - len(emitted))
            if room <= 0:
                finish = "total_limit"
            else:
                prefix = context + thought + leaving
                written, stop, new, held = await self._complete(client, prefix, room, set(self.end_tokens), policy.sampling,
                                                                stream(seed, prefix))
                if read is None:                                 # no thought: this is the call's first request
                    read, spared = new, held
                else:
                    again = new
                answer = written + ([stop] if stop is not None else [])
                emitted += answer
                if stop is not None:
                    stopped, finish = True, "stop"
                elif len(written) >= policy.max_tokens:
                    finish = "answer_limit"
                    if len(emitted) < total:                     # as engine.py: one end of turn of the engine's own closes the reply
                        injected_positions.append(len(emitted))
                        emitted.append(self.end_of_turn)
                else:
                    finish = "total_limit"
        said = answer[:-1] if answer and answer[-1] in self.end_tokens else answer
        thought_text, thought_tokens, reasoning = "", None, ""
        if thinking != 0:
            body = thought[:-1] if closed_itself or ended_turn else thought
            thought_text, thought_tokens = self.tokenizer.decode(body).strip(), thought + leaving
            reasoning = self.tokenizer.decode(thought + leaving).split("</think>")[0]
        injected = len(injected_positions)
        read, spared = (len(context), 0) if read is None else (read, min(spared, len(context)))      # None: nothing was sent
        self.new_tokens += len(emitted)
        self.sampled_tokens += len(emitted) - injected
        self.injected_tokens += injected
        self.read_tokens += read
        self.spared_tokens += spared
        self.answer_read_tokens += again
        reply = Reply(self.tokenizer.decode(said).strip(), answer, thought=thought_text, reasoning=reasoning,
                      thought_tokens=thought_tokens, finished_thinking=closed_itself, stopped=stopped, finish_reason=finish,
                      seed=seed, prompt_tokens=len(context), sampled_tokens=len(emitted) - injected, injected_tokens=injected,
                      injected_positions=injected_positions, output_tokens=emitted)
        return reply, read, spared

    # ---------------------------------------------------------------- generation
    def generate(self, prompts: list[Prompt], seeds: list[int] | None = None, *, thinking: int | None = None,
                 max_tokens: int = 4096, max_total_tokens: int = 32768, sampling: Sampling | None = None,
                 temperature: float | None = None, thinking_temperature: float | None = None,
                 thinking_top_k: int | None = None, share: bool = True, tools: list[dict] | None = None,
                 thought_sampling: Sampling | None = None) -> list[Reply]:
        """Generate in input order, using fresh recorded seeds when none are supplied. The settings mean what
        they mean in engine.py. `share` is taken and not used: the server reads a shared start once by itself."""
        if sampling is not None and not isinstance(sampling, Sampling):
            raise ValueError("sampling must be a Sampling configuration")
        if thought_sampling is not None and not isinstance(thought_sampling, Sampling):
            raise ValueError("thought_sampling must be a Sampling configuration")
        sampling = sampling if sampling is not None else Sampling()
        if temperature is not None:
            sampling = replace(sampling, temperature=temperature)
            thought_sampling = thought_sampling and replace(thought_sampling, temperature=temperature)
        thought_sampling = replace(thought_sampling or sampling,
            **({"temperature": thinking_temperature} if thinking_temperature is not None else {}),
            **({"top_k": thinking_top_k} if thinking_top_k is not None else {}))
        policy = self._policy(thinking, max_tokens, max_total_tokens, sampling, thought_sampling)
        seeds = list(seeds) if seeds is not None else [secrets.randbits(64) for _ in prompts]
        if len(seeds) != len(prompts):
            raise ValueError("seeds must have exactly one entry per prompt")
        for seed in seeds:
            integer("seed", seed)
        self.groups, self.last_run = [], {}
        if not prompts:
            return []
        started = time.perf_counter()
        contexts = [self._fits(self.encode(p, thinking=thinking != 0, tools=tools), policy.total, f"Request {i}")
                    for i, p in enumerate(prompts)]
        self.last_run = {"engine": self.describe(), "seeds": seeds, "prompt_sha256": [digest(c) for c in contexts],
                         "prompt_tokens": [len(c) for c in contexts], "thinking": thinking, "max_tokens": max_tokens,
                         "max_total_tokens": max_total_tokens, "sampling": asdict(policy.sampling),
                         "thought_sampling": asdict(policy.thought_sampling), "share": share,
                         "tools": [tool.get("function", tool).get("name") for tool in tools] if tools else None,
                         "groups": [list(range(len(prompts)))], "status": "running"}
        before = self._counted()
        flying = {"now": 0, "most": 0}

        async def everything() -> list[Reply]:
            gate = asyncio.Semaphore(self.width)

            async def one(i: int) -> Reply:
                async with gate:
                    flying["now"] += 1
                    flying["most"] = max(flying["most"], flying["now"])
                    self._sent(flying["now"])
                    try:
                        reply, _, _ = await self._one(client, contexts[i], seeds[i], policy)
                    finally:
                        flying["now"] -= 1
                reply.metadata = {"prompt_sha256": self.last_run["prompt_sha256"][i], "request_index": i}
                return reply

            self._heard = time.monotonic()
            async with self._client() as client:
                async with asyncio.TaskGroup() as group:
                    watch = group.create_task(self._watch(lambda: flying["now"]))
                    replies = await asyncio.gather(*(group.create_task(one(i)) for i in range(len(prompts))))
                    watch.cancel()
                return list(replies)

        try:
            replies = asyncio.run(everything())
        except BaseExceptionGroup as several:                    # the first thing that went wrong, as it was raised
            self.last_run["status"] = "failed"
            raise first_of(several) from None
        except BaseException:
            self.last_run["status"] = "failed"
            raise
        else:
            self.last_run["status"] = "complete"
            self.calls += len(prompts)
            self.prompt_tokens += sum(len(c) for c in contexts)
        finally:
            self._ended(started, before, flying["most"])
        return replies

    def _counted(self) -> tuple[int, ...]:
        return (self.read_tokens, self.spared_tokens, self.new_tokens, self.sampled_tokens, self.injected_tokens,
                self.answer_read_tokens)

    def _ended(self, started: float, before: tuple[int, ...], widest: int, **more):
        elapsed = time.perf_counter() - started
        self.seconds += elapsed
        self.groups = [widest]
        self.last_run.update(seconds=elapsed, widest=widest, **more, usage=dict(zip(
            ("read_tokens", "spared_tokens", "output_tokens", "sampled_tokens", "injected_tokens", "answer_read_tokens"),
            (now - then for now, then in zip(self._counted(), before)))))

    # ---------------------------------------------------------------- conversations
    def converse(self, prompts: list[Prompt], seeds: list[int], respond, *, thinking: int | None = None,
                 max_tokens: int = 4096, max_total_tokens: int = 32768, sampling: Sampling | None = None,
                 thought_sampling: Sampling | None = None, tools: list[dict] | None = None, workers: int = 4,
                 at_once: int | None = None, known=None) -> None:
        """Carry on many conversations side by side, each at its own pace: engine.py's `converse`, with the
        server keeping what each has read.

        `prompts[i]` opens conversation i and `seeds[i]` is its seed. When its reply is written,
        `respond(i, reply)` says how it goes on: `(prompt, seed)`, its next call, or None when it is over. It
        runs on one of `workers` other threads and must not touch the engine. It may return a
        `concurrent.futures.Future` of its answer: the conversation then waits, holding nothing, until another
        `respond` sets it. If every conversation left is waiting and none is at work, the run stops with an
        error. `known(i)`, if given, is asked once before each call of conversation i is sent: a reply it
        returns goes to `respond` as it is, and nothing is sent. `at_once` is the most conversations open at a
        time; with it, a conversation that waits for one that is not opened yet waits for ever: open them all.

        A next prompt that begins with what its conversation has read and written is read from where it left
        off, as far as the server still holds it (`carried_tokens` in `last_run`). Nothing has to be done for
        that here, and nothing is lost when it does not: the server reads what it no longer holds.

        Every opening is cut into tokens and held against the server's limit before anything is sent, as
        engine.py does. A later prompt is, unlike there, only when its reply is not known already."""
        for name, value in (("workers", workers), *((("at_once", at_once),) if at_once is not None else ())):
            integer(name, value, 1)
        policy = self._policy(thinking, max_tokens, max_total_tokens, sampling, thought_sampling)
        seeds = list(seeds)
        if len(seeds) != len(prompts):
            raise ValueError("seeds must have exactly one entry per prompt")
        for seed in seeds:
            integer("seed", seed)
        self.groups, self.last_run = [], {}
        if not prompts:
            return
        started = time.perf_counter()
        log: list[dict] = []
        self.last_run = {"engine": self.describe(), "conversations": len(prompts), "calls": log, "thinking": thinking,
                         "max_tokens": max_tokens, "max_total_tokens": max_total_tokens, "sampling": asdict(policy.sampling),
                         "thought_sampling": asdict(policy.thought_sampling), "share": True,
                         "tools": [tool.get("function", tool).get("name") for tool in tools] if tools else None,
                         "at_once": at_once, "status": "running"}
        before = self._counted()
        count = {"flying": 0, "widest": 0, "recalled": 0, "at_work": 0, "unopened": len(prompts), "open": 0}
        promised: set[Future] = set()                # the answers `respond` said would come later
        pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="respond")
        desk = ThreadPoolExecutor(max_workers=1, thread_name_prefix="prompt")     # prompts are cut into tokens, and `known` asked, off the loop

        def encode(prompt: Prompt, who: int) -> list[int]:
            return self._fits(self.encode(prompt, thinking=thinking != 0, tools=tools), policy.total, f"Conversation {who}")

        try:
            openings = [encode(prompt, i) for i, prompt in enumerate(prompts)]
        except BaseException:
            self.last_run["status"] = "failed"
            pool.shutdown(wait=False)
            desk.shutdown(wait=False)
            raise

        async def everything():
            loop = asyncio.get_running_loop()
            gate = asyncio.Semaphore(self.width)
            door = asyncio.Semaphore(at_once) if at_once is not None else None

            def stuck() -> str | None:
                """Why nothing can go on, if nothing can: some conversations wait for an answer, nobody is at work
                to give one, and nobody else can begin."""
                can_open = count["unopened"] and (at_once is None or count["open"] < at_once)
                if not promised or count["at_work"] or can_open or any(f.done() for f in promised):
                    return None
                return (f"{len(promised)} conversations wait for each other and none is at work"
                        + (f"; {count['unopened']} are not opened yet (at_once={at_once})" if count["unopened"] else ""))

            def answer_of(waited: Future) -> asyncio.Future:
                """What a promise comes to, for the loop to wait on. Nothing done here reaches back into the promise
                (a run that ends leaves those it waited on as they are, as engine.py does), and one that its
                maker cancels ends the run with the error it is there: an Exception, not this loop's own
                cancellation."""
                mine = loop.create_future()

                def tell(done: Future):
                    def pass_on():
                        if mine.done():
                            return
                        if done.cancelled():
                            mine.set_exception(Cancelled())
                        elif done.exception() is not None:
                            mine.set_exception(done.exception())
                        else:
                            mine.set_result(done.result())
                    try:
                        loop.call_soon_threadsafe(pass_on)
                    except RuntimeError:                           # the loop has gone: the run is over
                        pass

                waited.add_done_callback(tell)
                return mine

            async def talk(i: int):
                if door is not None:
                    await door.acquire()
                count["unopened"] -= 1
                count["open"] += 1
                count["at_work"] += 1
                try:
                    prompt, seed, context = prompts[i], seeds[i], openings[i]
                    while True:
                        reply = await loop.run_in_executor(desk, known, i) if known is not None else None
                        if reply is not None:
                            count["recalled"] += 1
                        else:
                            if context is None:
                                context = await loop.run_in_executor(desk, encode, prompt, i)
                            async with gate:
                                count["flying"] += 1
                                count["widest"] = max(count["widest"], count["flying"])
                                self._sent(count["flying"])
                                entry = {"conversation": i, "seed": seed, "prompt_tokens": len(context), "carried_tokens": 0,
                                         "started": round(time.perf_counter() - started, 2), "prompt_sha256": digest(context)}
                                log.append(entry)
                                try:
                                    reply, read, spared = await self._one(client, context, seed, policy)
                                finally:
                                    count["flying"] -= 1
                            reply.metadata = {"prompt_sha256": entry["prompt_sha256"], "conversation": i}
                            entry.update(carried_tokens=min(spared, len(context)), output_tokens=len(reply.output_tokens),
                                         finish_reason=reply.finish_reason, finished=round(time.perf_counter() - started, 2))
                        went_on = await loop.run_in_executor(pool, respond, i, reply)
                        while isinstance(went_on, Future):         # how it goes on is not known yet: it waits (and what it
                            waited = went_on                       # waited for may be another wait)
                            promised.add(waited)
                            count["at_work"] -= 1
                            try:
                                if (why := stuck()) is not None:
                                    raise RuntimeError(why)
                                went_on = await answer_of(waited)
                            finally:
                                promised.discard(waited)
                                count["at_work"] += 1
                        if went_on is None:
                            break
                        (prompt, seed), context = went_on, None
                        integer("seed", seed)
                finally:
                    count["at_work"] -= 1
                    count["open"] -= 1
                    if door is not None:
                        door.release()
                if (why := stuck()) is not None:                   # it was the last at work, and others still wait
                    raise RuntimeError(why)

            self._heard = time.monotonic()
            async with self._client() as client:
                async with asyncio.TaskGroup() as group:
                    watch = group.create_task(self._watch(lambda: count["flying"]))
                    await asyncio.gather(*(group.create_task(talk(i)) for i in range(len(prompts))))
                    watch.cancel()

        try:
            asyncio.run(everything())
        except BaseExceptionGroup as several:                    # the first thing that went wrong, as it was raised
            self.last_run["status"] = "failed"
            raise first_of(several) from None
        except BaseException:
            self.last_run["status"] = "failed"
            raise
        else:
            self.last_run["status"] = "complete"
            self.calls += len(log)
            self.prompt_tokens += sum(entry["prompt_tokens"] for entry in log)
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
            desk.shutdown(wait=True, cancel_futures=True)
            self._ended(started, before, count["widest"], read_again=0, let_go=0, known=count["recalled"], peak_memory_gb=None)


def digest(context: list[int]) -> str:
    """What stands for a prompt in a log (as engine.py: a hash of its token ids)."""
    return hashlib.sha256(np.asarray(context, dtype="<i4").tobytes()).hexdigest()


def first_of(several: BaseExceptionGroup) -> BaseException:
    """Of the errors a group of conversations ended with, the one to raise: a real one before a cancellation."""
    flat, left = [], [several]
    while left:
        error = left.pop(0)
        if isinstance(error, BaseExceptionGroup):
            left = list(error.exceptions) + left
        else:
            flat.append(error)
    return next((e for e in flat if not isinstance(e, asyncio.CancelledError)), flat[0])


def gpu() -> dict:
    """This machine's first GPU, as nvidia-smi names it: {"name", "memory_gb"}. Empty if it has none."""
    import subprocess
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=20).stdout.strip().splitlines()
        name, memory = (part.strip() for part in out[0].split(","))
        return {"name": name, "memory_gb": round(int(memory) / 1024, 1), "count": len(out)}
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return {}
