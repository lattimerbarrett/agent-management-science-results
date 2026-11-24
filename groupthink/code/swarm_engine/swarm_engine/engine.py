"""Batched local inference with explicit decoding policy and per-request audit metadata.

Natural thinking is the default. ``thinking=N`` explicitly opts into forced closure;
``thinking=0`` disables thinking. Seeds reproduce random draws, not bitwise results
across different batch shapes, prefix sharing settings or software versions.
"""
from __future__ import annotations

import inspect
import hashlib
import platform
import secrets
from collections import deque
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from importlib.metadata import version
from pathlib import Path
import time
import zlib
from dataclasses import asdict, dataclass, field, replace

import mlx.core as mx
import numpy as np
from mlx.utils import tree_flatten
from mlx_lm import load
from mlx_lm.generate import BatchGenerator, StopSequences
from mlx_lm.models.cache import ArraysCache, KVCache, make_prompt_cache
from huggingface_hub import snapshot_download

from .machine import budget_gb, cache_gb, limit_memory, require_lock
from .settings import Sampling, integer

# The models this was measured on. Both are 4-bit and in this machine's Hugging Face cache.
MODELS = {"4B": "mlx-community/Qwen3.5-4B-4bit", "9B": "mlx-community/Qwen3.5-9B-4bit"}

REVISIONS = {"4B": "0e7ffd5c629ef7719d4cbc04069232580bfa9d9c",
             "9B": "8b2b98c00a6b4d291155e4890773ca8f769aee53"}

# What Qwen is given when a thought is still open at its budget (from the Qwen3 model card).
OUT_OF_TIME = ("\n\nConsidering the limited time by the user, I have to give the solution based on the thinking "
               "directly now.\n</think>\n\n")

# Memory is planned from what a call's cache holds, doubled: the recurrent state is rewritten every step and
# the attention cache is copied each time it grows, so for a moment both the old and the new are held. On top of
# that, reading prompts holds a lot per token while it lasts (measured when the model is loaded), so prompts
# are read `READ_STEP` tokens at a time. README.md has planned against measured.
FIXED_SPARE, TOKEN_SPARE = 2.0, 2.0
READ_STEP = 512
TALK_PREFILL = 2      # prompts read together while conversations are carried on: most of them are a few new lines
SETTLE_STEPS = 256    # how often a batch's caches are worked out to the end while it is written (see `settle`)

Prompt = str | tuple[str, str] | list[dict]   # a user message, (system, user), or chat messages


@dataclass
class Reply:
    text: str                                 # the answer, without any thinking
    tokens: list[int]                         # the answer's token ids, as written (with its end-of-turn token)
    thought: str = ""                         # what the model thought first, as a person would want to read it
    reasoning: str = ""                       # the thought as the model had it before it when it answered: with the words
                                              # that closed it, when its budget ran out. What a chat passes back as its
                                              # `reasoning_content` if the conversation is to carry on from here
    thought_tokens: list[int] | None = None   # everything between the prompt and the answer, as the model saw it
    finished_thinking: bool | None = None     # False if the thought was closed for it; None if thinking was off
    stopped: bool = True                      # completion ended with a model-sampled EOS
    finish_reason: str = "stop"               # stop, answer_limit, total_limit, end_in_thought
    seed: int | None = None
    prompt_tokens: int = 0
    sampled_tokens: int = 0
    injected_tokens: int = 0                   # forced bridge and any synthetic termination EOS
    injected_positions: list[int] = field(default_factory=list)
    output_tokens: list[int] = field(default_factory=list)  # exact emitted sequence, including forced tokens
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------- planning (no model needed)

def common(a: list[int], b: list[int]) -> int:
    """How many tokens two contexts start with in common."""
    n = min(len(a), len(b))
    if a[:n] == b[:n]:
        return n
    low, high = 0, n                          # a[:low] == b[:low] and a[:high] != b[:high]
    while high - low > 1:
        mid = (low + high) // 2
        if a[:mid] == b[:mid]:
            low = mid
        else:
            high = mid
    return low


def clusters(contexts: list[list[int]], min_saved: int = 64) -> list[tuple[int, list[int]]]:
    """Sets of calls whose shared start is worth reading once: (tokens they all start with, which calls).

    Sorting puts calls with a common start next to each other. The set that saves the most reading (shared
    tokens times the calls that no longer read them) is taken first, then the same again to its left and right,
    so that the calls about one problem are grouped on the whole problem, not on the system message every call
    happens to begin with. A call belongs to at most one set."""
    order = sorted(range(len(contexts)), key=contexts.__getitem__)
    shared = [common(contexts[order[k]], contexts[order[k + 1]]) for k in range(len(order) - 1)]
    found: list[tuple[int, list[int]]] = []
    todo = [(0, len(order) - 1)]                  # stretches of calls order[first..last] still to look at
    while todo:
        first, last = todo.pop()
        if last <= first:
            continue
        # The widest-times-lowest block of `shared[first:last]` (the largest rectangle under a histogram).
        best, stack = (0, 0, 0, 0), []            # tokens saved, from, to, shared by all of them
        for at in range(first, last + 1):
            low = shared[at] if at < last else -1
            begin = at
            while stack and stack[-1][1] >= low:
                begin, height = stack.pop()
                if (at - begin) * height > best[0]:
                    best = ((at - begin) * height, begin, at, height)
            stack.append((begin, low))
        saved, i, j, low = best
        if saved < min_saved:
            continue
        found.append((low, [order[k] for k in range(i, j + 1)]))
        todo += [(first, i - 1), (j + 1, last)]
    return found


def plan(lengths: list[int], extra: int, width: int, room: float, fixed: float, per_token: float) -> list[list[int]]:
    """Cut calls into groups that can run side by side: at most `width` of them, and no more memory than `room`
    if every call in the group ran to its full length. A batch holds every row at its longest row's length, so
    calls are taken shortest first and a group is costed at its longest. Oversized calls fail before generation."""
    integer("width", width, 1)
    integer("extra", extra)
    if room <= 0:
        raise ValueError("No memory remains for requests; increase the memory budget or reduce prefill")
    if not lengths:
        return []
    groups: list[list[int]] = [[]]
    for i in sorted(range(len(lengths)), key=lengths.__getitem__):
        size = len(groups[-1]) + 1
        each = FIXED_SPARE * fixed + TOKEN_SPARE * per_token * (lengths[i] + extra)
        if each > room:
            raise ValueError(f"Request {i} needs an estimated {each / 2**30:.2f} GiB of cache but only "
                             f"{room / 2**30:.2f} GiB remains; reduce context/output limits or increase memory")
        if groups[-1] and (size > width or size * each > room):
            groups.append([])
        groups[-1].append(i)
    return groups


def stream(seed: int, context: list[int]) -> int:
    """Which random stream a call draws from: fixed by who is asking (`seed`) and by exactly what they were
    asked. The same question from the same asker always draws the same numbers, while a different question gets
    fresh randomness (so an agent's successive answers are independent draws)."""
    asked = zlib.crc32(np.asarray(context, dtype=np.int32).tobytes())
    return int(np.random.SeedSequence([seed, asked]).generate_state(1)[0])


# ---------------------------------------------------------------- one call's way through its reply

THINKING, LEAVING, ANSWERING, ENDING, OVER = range(5)


@dataclass
class _Call:
    """Where one call is in its reply, and what it has written so far."""
    key: mx.array                                      # its own random stream: split once for every draw
    stage: int
    forced: list[int] = field(default_factory=list)    # tokens it writes next whatever the model would say
    thought: list[int] = field(default_factory=list)   # the thought as the model wrote it
    leaving: list[int] = field(default_factory=list)   # what took it from the thought to the answer
    answer: list[int] = field(default_factory=list)
    closed_itself: bool | None = None                  # the thought ended with the model's own </think>
    ended_turn: bool = False                           # the model ended its turn inside the thought
    stopped: bool = False
    finish_reason: str | None = None
    emitted: list[int] = field(default_factory=list)
    sampled: int = 0
    injected: int = 0
    injected_positions: list[int] = field(default_factory=list)
    seen: set[int] = field(default_factory=set)


@dataclass
class _Talk:
    """One conversation that is being carried on: its call in flight, and what is kept of it between calls."""
    index: int
    context: list[int]                                 # the prompt of its call: the one in flight, or the next
    seed: int
    start: int | None = None                           # the shared start its first prompt begins with, if any
    held: list[int] = field(default_factory=list)      # the tokens `cache` holds: all it has read and written
    cache: list | None = None                          # None while its call is in flight, and when nothing is kept
    call: _Call | None = None
    seen: list[int] = field(default_factory=list)      # what the generator says this call wrote
    entry: dict = field(default_factory=dict)          # this call's line in `last_run`


def nbytes(cache: list | None) -> int:
    return sum(c.nbytes for c in cache) if cache else 0


def settle(gen) -> None:
    """Have the caches of the rows being written worked out to the end. mlx-lm counts positions in them with
    arrays that nothing reads while a row is written, so every step leaves one more sum for later in each layer's
    cache, and each holds a Metal buffer: about 25 a step on Qwen3.5 (measured, results/2026-10-08-converse),
    whatever the number of rows, against the 499,000 MLX may hold at once. Twenty thousand steps of one batch
    reach that, and the next allocation fails. Working the caches out lets all of it go."""
    batch = getattr(gen, "_generation_batch", None)
    if batch is not None and batch.prompt_cache:
        mx.eval([c.state for c in batch.prompt_cache])


def own(cache: list) -> list:
    """A finished call's cache, holding its own memory. mlx-lm hands the recurrent state back as a slice of the
    batch's arrays, and a slice keeps the whole batch's arrays alive for as long as it is kept."""
    for c in cache:
        if isinstance(c, ArraysCache):
            c.cache = [None if state is None else mx.contiguous(state) for state in c.cache]
    mx.eval([c.state for c in cache])
    return cache


class _Conductor:
    """Chooses every row's next token: one call from the batch generator per step, for all rows at once.

    Each call's draw comes from that call's own random stream, and the chosen tokens are read back once per
    step for the whole batch. Knowing every token as it is chosen is what lets a call go
    from thought to answer without leaving the batch. Only an explicitly requested
    thought budget injects a transition; natural closure keeps sampling normally.

    The generator calls a sampler with the rows' log-probabilities but not their names. Each call therefore
    also has a logits processor that says "here" (`present`), promotes logits to
    float32 and applies penalties. Row-by-row invocation identifies the sampling order."""

    def __init__(self, calls: list[_Call], *, thinking: int | None, max_tokens: int,
                 total_limit: int, sampling: Sampling, thought_sampling: Sampling,
                 close: int | None, end_of_turn: int, out_of_time: list[int],
                 end_tokens: set[int] | None = None):
        self.calls, self.thinking, self.max_tokens = calls, thinking, max_tokens
        self.total_limit = total_limit
        self.sampling, self.thought_sampling = sampling, thought_sampling
        self.close, self.end_of_turn = close, end_of_turn
        self.end_tokens = end_tokens or {end_of_turn}
        self.out_of_time = out_of_time
        self.present: list[int] = []

    def here(self, k: int):
        def processor(_tokens, logits):
            self.present.append(k)
            # Normalize in float32, before information is lost to bf16 logsumexp.
            logits = logits.astype(mx.float32)
            call = self.calls[k]
            settings = self.thought_sampling if call.stage == THINKING else self.sampling
            if call.seen and (settings.presence_penalty or settings.repetition_penalty != 1):
                indices = mx.array(sorted(call.seen))
                values = logits[:, indices]
                values = mx.where(values < 0, values * settings.repetition_penalty,
                                  values / settings.repetition_penalty) - settings.presence_penalty
                logits = mx.put_along_axis(logits, indices[None], values, axis=-1)
            return logits
        return processor

    def __call__(self, logprobs: mx.array) -> mx.array:
        rows, self.present = [self.calls[k] for k in self.present], []
        if len(rows) != logprobs.shape[0]:
            raise RuntimeError("the batch generator sampled rows that were not announced (mlx-lm changed?)")
        drawing = [c.stage in (THINKING, ANSWERING) and len(c.emitted) < self.total_limit for c in rows]
        would = self._draw(logprobs, rows, drawing) if any(drawing) else [0] * len(rows)
        return mx.array([self._next(c, token) for c, token in zip(rows, would)])

    def _draw(self, logprobs: mx.array, rows: list[_Call], drawing: list[bool]) -> list[int]:
        chosen = []
        # Filter together for each policy, while retaining an independent full-vocabulary
        # Gumbel draw per row. Regrouping rows cannot change their random streams.
        policies = [self.thought_sampling if c.stage == THINKING else self.sampling for c in rows]
        filtered = {}
        for settings in set(policies):
            indices = [i for i, (p, draws) in enumerate(zip(policies, drawing)) if draws and p == settings]
            if indices:
                values = filter_logits(logprobs[mx.array(indices)], settings)
                filtered.update((i, values[j:j + 1]) for j, i in enumerate(indices))
        for i, c in enumerate(rows):
            if not drawing[i]:
                chosen.append(mx.array([0]))
            elif policies[i].temperature == 0:
                chosen.append(mx.argmax(filtered[i], axis=-1))
            else:
                c.key, use = mx.random.split(c.key)
                chosen.append(mx.random.categorical(filtered[i], key=use))
        return mx.concatenate(chosen).tolist()

    def _next(self, c: _Call, token: int) -> int:
        # BatchGenerator samples one step ahead. Do not record its discarded lookahead
        # after a terminal token or total cap as output (or advance the random stream).
        if c.stage == OVER:
            return self.end_of_turn
        if len(c.emitted) >= self.total_limit:
            c.finish_reason = c.finish_reason or "total_limit"
            if c.closed_itself is None and self.thinking != 0:
                c.closed_itself = False
            c.stage = OVER
            return self.end_of_turn
        injected = c.stage in (LEAVING, ENDING)
        if c.stage == LEAVING:
            token = c.forced.pop(0)
            c.leaving.append(token)
            if not c.forced:
                c.stage = ANSWERING
        elif c.stage == THINKING:
            c.thought.append(token)
            if token in self.end_tokens:
                c.closed_itself, c.ended_turn, c.stopped = False, True, True
                c.finish_reason, c.stage = "end_in_thought", OVER
            elif token == self.close:
                c.closed_itself, c.stage = True, ANSWERING
            elif self.thinking is not None and len(c.thought) >= self.thinking:
                c.closed_itself, c.forced, c.stage = False, list(self.out_of_time), LEAVING
        elif c.stage == ANSWERING:
            c.answer.append(token)
            if token in self.end_tokens:
                c.stopped, c.stage, c.finish_reason = True, OVER, "stop"
            elif len(c.answer) >= self.max_tokens:
                c.stage, c.finish_reason = ENDING, "answer_limit"
        elif c.stage == ENDING:
            c.stage, token = OVER, self.end_of_turn
        if injected:
            c.injected_positions.append(len(c.emitted))
        c.emitted.append(token)
        c.seen.add(token)
        c.injected += int(injected)
        c.sampled += int(not injected)
        return token


def filter_logits(logprobs: mx.array, settings: Sampling) -> mx.array:
    """Temperature -> exact top-k -> top-p -> min-p, retaining the highest token.

    Work on the top-k shortlist for nucleus filtering, then scatter back so keyed
    categorical noise remains attached to vocabulary IDs, not sorted positions.
    """
    if settings.temperature == 0:
        return logprobs
    scaled = logprobs.astype(mx.float32) / settings.temperature
    vocab = scaled.shape[-1]
    k = min(settings.top_k, vocab) if settings.top_k else vocab
    if k < vocab:
        indices = mx.argpartition(-scaled, kth=k - 1, axis=-1)[:, :k]
        values = mx.take_along_axis(scaled, indices, axis=-1)
    else:
        indices = mx.broadcast_to(mx.arange(vocab)[None], scaled.shape)
        values = scaled
    if settings.top_p < 1 or settings.min_p > 0:
        order = mx.argsort(-values, axis=-1)
        indices = mx.take_along_axis(indices, order, axis=-1)
        values = mx.take_along_axis(values, order, axis=-1)
        probabilities = mx.softmax(values, axis=-1)
        preceding = mx.cumsum(probabilities, axis=-1) - probabilities
        keep = (preceding < settings.top_p) & (probabilities >= settings.min_p * probabilities[:, :1])
        keep = keep | (mx.arange(k)[None] == 0)
        values = mx.where(keep, values, -mx.inf)
    return mx.put_along_axis(mx.full_like(scaled, -mx.inf), indices, values, axis=-1)


# ---------------------------------------------------------------- the engine

class Engine:
    def __init__(self, model: str = "4B", *, width: int = 100, prefill: int = 16, min_shared: int = 64,
                 revision: str | None = None):
        """`model` is "4B", "9B" or any mlx-lm model. `width` is the most calls generated side by side;
        `prefill` the most prompts read together (reading is where memory briefly peaks); a shared start is
        read once when that saves at least `min_shared` tokens of reading."""
        for name, value in (("width", width), ("prefill", prefill), ("min_shared", min_shared)):
            integer(name, value, 1)
        require_lock()
        limit_memory()
        if "logits_processors" not in inspect.signature(BatchGenerator.insert).parameters:
            raise RuntimeError("swarm_engine needs mlx-lm 0.32 (per-call caches and processors in BatchGenerator)")
        self.name = MODELS.get(model, model)
        self.width, self.prefill, self.min_shared = width, prefill, min_shared
        path = Path(self.name).expanduser()
        if not path.is_dir():
            path = Path(snapshot_download(self.name, revision=revision or REVISIONS.get(model),
                        allow_patterns=["*.json", "model*.safetensors", "tokenizer.model", "*.tiktoken",
                                        "tiktoken.model", "*.txt", "*.jinja"]))
            self.revision = path.name
        else:
            if revision is not None:
                raise ValueError("revision applies to Hugging Face repositories, not local directories")
            self.revision = None
        self.model_path = path.resolve()
        self.model, self.tokenizer, config = load(str(path), return_config=True)
        text_config = config.get("text_config", config)
        self.context_limit = text_config.get("max_position_embeddings")
        self.artifact_hashes = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                               for f in path.iterdir() if f.suffix in (".json", ".jinja", ".model", ".tiktoken")}
        self.versions = {p: version(p) for p in ("mlx", "mlx-lm", "numpy", "transformers", "tokenizers",
                                               "huggingface-hub", "swarm-engine")}
        self._source_hash = hashlib.sha256(Path(__file__).read_bytes() +
                                           Path(__file__).with_name("settings.py").read_bytes()).hexdigest()
        self.model.eval()
        self.end_of_turn = self.tokenizer.eos_token_id
        close = self.encode_text("</think>")
        self.close = close[0] if len(close) == 1 else None      # None: the model has no thinking mode we can drive
        self._out_of_time = self.encode_text(OUT_OF_TIME)
        self.end_tokens = set(self.tokenizer.eos_token_ids) | {self.end_of_turn}
        self._end = StopSequences([[t] for t in sorted(self.end_tokens)])
        self.weights = sum(v.nbytes for _, v in tree_flatten(self.model.parameters()))
        self.fixed, self.per_token = self._footprint()
        self.read_fixed, self.read_per_token = self._reading()
        self.room = (budget_gb() - cache_gb()) * 2**30 - self.weights
        if self.room <= 0:
            raise ValueError("Model weights and buffer cache exhaust the memory budget")
        self.calls = self.new_tokens = self.read_tokens = self.spared_tokens = 0
        self.sampled_tokens = self.injected_tokens = self.prompt_tokens = 0
        self.last_run: dict = {}
        self.seconds = 0.0
        self.groups: list[int] = []           # how the last `generate` was cut up: calls side by side in each batch

    def _footprint(self) -> tuple[int, int]:
        """What one live call holds: bytes whatever its length (the recurrent state of Qwen3.5's linear-attention
        layers) and bytes per token (the attention cache of the layers that keep one). Read off a real cache, so
        it is right for whichever model was loaded."""
        cache = make_prompt_cache(self.model)
        self.model(mx.array([[self.end_of_turn, self.end_of_turn]]), cache=cache)
        mx.eval([c.state for c in cache])
        fixed = per_token = 0
        for c in cache:
            if isinstance(c, KVCache):
                per_token += (c.keys.shape[1] * c.keys.shape[3] + c.values.shape[1] * c.values.shape[3]) * c.keys.dtype.size
            else:
                fixed += c.nbytes
        return fixed, per_token

    def _reading(self) -> tuple[float, float]:
        """What reading a prompt briefly holds on top of the cache it leaves: bytes whatever is read, and bytes
        per token read at once. Measured on two reads of different lengths (after one to warm up)."""
        def held(tokens: int) -> int:
            mx.clear_cache()
            mx.reset_peak_memory()
            cache = make_prompt_cache(self.model)
            self.model(mx.array([[self.end_of_turn] * tokens]), cache=cache)
            mx.eval([c.state for c in cache])
            return max(mx.get_peak_memory() - mx.get_active_memory(), 0)

        held(64)
        short, long = held(256), held(1024)
        per_token = max((long - short) / (1024 - 256), 0.0)
        return max(short - 256 * per_token, 0.0), per_token

    def describe(self) -> dict:
        """The settings a run's log should record."""
        return {"model": self.name, "revision": self.revision, "model_path": str(self.model_path),
                "artifact_sha256": self.artifact_hashes, "versions": self.versions, "source_sha256": self._source_hash,
                "python": platform.python_version(), "macos": platform.mac_ver()[0],
                "machine": mx.device_info().get("device_name"),
                "context_limit": self.context_limit, "min_shared": self.min_shared,
                "width": self.width, "prefill": self.prefill, "budget_gb": budget_gb(), "cache_gb": cache_gb(),
                "weights_gb": round(self.weights / 2**30, 1), "per_call_mb": round(self.fixed / 2**20, 1),
                "per_token_kb": round(self.per_token / 2**10, 1), "reading_mb": round(self.read_fixed / 2**20),
                "reading_kb_per_token": round(self.read_per_token / 2**10)}

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

    # ---------------------------------------------------------------- generation
    def generate(self, prompts: list[Prompt], seeds: list[int] | None = None, *, thinking: int | None = None,
                 max_tokens: int = 4096, max_total_tokens: int = 32768, sampling: Sampling | None = None,
                 temperature: float | None = None, thinking_temperature: float | None = None,
                 thinking_top_k: int | None = None, share: bool = True, tools: list[dict] | None = None,
                 thought_sampling: Sampling | None = None) -> list[Reply]:
        """Generate in input order, using fresh recorded seeds when none are supplied.

        tools: function schemas offered to every prompt of this call. The chat
        template writes them into the prompt; a tool call comes back as text in
        the reply. The engine neither parses nor runs it: the caller does, and
        passes the call and its result back as chat messages on the next call.

        thinking=None: natural thinking until </think> or the total safety cap.
        thinking=0: direct answers. thinking=N>0: opt into forced closure after N
        thought tokens. max_tokens always caps ANSWER tokens; max_total_tokens
        caps the entire emitted reply, including injected tokens. No answer is
        manufactured when the total cap expires or the model ends in its thought.

        Sampling applies to both phases, unless thought_sampling gives the
        thought a policy of its own (to think with the general preset and write
        code with the precise one, say). The legacy temperature overrides are
        explicit opt-ins; thinking_top_k only overrides the thought's top-k.
        Save last_run and Reply metadata for replay. Fixed seeds reproduce random
        streams, not exact trajectories across different batching configurations.
        """
        for name, value in (("max_tokens", max_tokens), ("max_total_tokens", max_total_tokens),
                            ("width", self.width), ("prefill", self.prefill), ("min_shared", self.min_shared)):
            integer(name, value, 1)
        if thinking is not None:
            integer("thinking", thinking)
        if not isinstance(share, bool):
            raise ValueError("share must be a boolean")
        sampling = sampling if sampling is not None else Sampling()
        if not isinstance(sampling, Sampling):
            raise ValueError("sampling must be a Sampling configuration")
        if thought_sampling is not None and not isinstance(thought_sampling, Sampling):
            raise ValueError("thought_sampling must be a Sampling configuration")
        if temperature is not None:
            sampling = replace(sampling, temperature=temperature)
            thought_sampling = thought_sampling and replace(thought_sampling, temperature=temperature)
        thought_sampling = replace(thought_sampling or sampling,
            **({"temperature": thinking_temperature} if thinking_temperature is not None else {}),
            **({"top_k": thinking_top_k} if thinking_top_k is not None else {}))
        seeds = list(seeds) if seeds is not None else [secrets.randbits(64) for _ in prompts]
        if len(seeds) != len(prompts):
            raise ValueError("seeds must have exactly one entry per prompt")
        for seed in seeds:
            integer("seed", seed)
        self.groups, self.last_run = [], {}
        if not prompts:
            return []
        if thinking != 0 and self.close is None:
            raise ValueError(f"{self.name} has no </think> token; use thinking=0")
        started = time.perf_counter()
        contexts = [self.encode(p, thinking=thinking != 0, tools=tools) for p in prompts]
        extra = self._allowance(thinking, max_tokens, max_total_tokens)
        lengths = [len(c) for c in contexts]
        if self.context_limit is not None:
            for i, length in enumerate(lengths):
                if length + extra > self.context_limit:
                    raise ValueError(f"Request {i}: prompt + output allowance exceeds context limit {self.context_limit}")
        replies: list[Reply | None] = [None] * len(prompts)
        read_from, start_of = [0] * len(contexts), [None] * len(contexts)
        for which, (shared, members) in enumerate(clusters(contexts, self.min_shared) if share else []):
            shared = min(shared, min(len(contexts[m]) for m in members) - 1)
            if shared * (len(members) - 1) >= self.min_shared:
                for m in members:
                    read_from[m], start_of[m] = shared, which
        unread = max(n - at for n, at in zip(lengths, read_from))
        reading = self.read_fixed + min(self.prefill, self.width, len(prompts)) * min(unread, READ_STEP) * self.read_per_token
        # Shared prefixes use the same bounded read step, including identical prompts
        # whose remaining suffix is only one token.
        if any(read_from):
            reading = max(reading, self.read_fixed + min(max(read_from), READ_STEP) * self.read_per_token)
        groups = plan(lengths, extra, self.width, self.room - reading, self.fixed, self.per_token)
        self.groups = [len(g) for g in groups]
        self.last_run = {"engine": self.describe(), "seeds": seeds,
                         "prompt_sha256": [hashlib.sha256(np.asarray(c, dtype="<i4").tobytes()).hexdigest() for c in contexts],
                         "prompt_tokens": lengths, "thinking": thinking, "max_tokens": max_tokens,
                         "max_total_tokens": max_total_tokens, "sampling": asdict(sampling),
                         "thought_sampling": asdict(thought_sampling), "share": share,
                         "tools": [tool.get("function", tool).get("name") for tool in tools] if tools else None,
                         "groups": groups, "status": "running"}
        before = (self.read_tokens, self.spared_tokens, self.new_tokens, self.sampled_tokens, self.injected_tokens)
        try:
            for group in groups:
                batch = self._side_by_side([contexts[i] for i in group], [seeds[i] for i in group],
                    [read_from[i] for i in group], [start_of[i] for i in group],
                    extra, thinking, max_tokens, sampling, thought_sampling)
                if len(batch) != len(group):
                    raise RuntimeError("Batch generator did not return all requested replies")
                for i, reply in zip(group, batch):
                    reply.metadata = {"prompt_sha256": self.last_run["prompt_sha256"][i], "request_index": i}
                    replies[i] = reply
                mx.clear_cache()
        except Exception:
            self.last_run["status"] = "failed"
            raise
        else:
            self.last_run["status"] = "complete"
            self.calls += len(prompts)
            self.prompt_tokens += sum(lengths)
        finally:
            elapsed = time.perf_counter() - started
            self.seconds += elapsed
            self.last_run["seconds"] = elapsed
            now = (self.read_tokens, self.spared_tokens, self.new_tokens, self.sampled_tokens, self.injected_tokens)
            self.last_run["usage"] = dict(zip(("read_tokens", "spared_tokens", "output_tokens", "sampled_tokens", "injected_tokens"),
                                             (a - b for a, b in zip(now, before))))
        return replies

    def _allowance(self, thinking: int | None, max_tokens: int, max_total_tokens: int) -> int:
        """The most tokens one reply may come to: what a call's cache must have room to grow by."""
        if thinking is None:
            return max_total_tokens
        return min(max_total_tokens, (thinking + len(self._out_of_time) if thinking else 0) + max_tokens + 1)

    def _read(self, tokens: list[int]) -> list:
        """A cache that holds `tokens`, to be handed (as a copy each) to the calls that start with them."""
        cache = make_prompt_cache(self.model)
        for at in range(0, len(tokens), READ_STEP):
            self.model(mx.array(tokens[at:at + READ_STEP])[None], cache=cache)
            mx.eval([c.state for c in cache])
        self.read_tokens += len(tokens)
        return cache

    def _side_by_side(self, contexts: list[list[int]], seeds: list[int], read_from: list[int], start_of: list,
                      extra: int, thinking: int | None, max_tokens: int, sampling: Sampling,
                      thought_sampling: Sampling) -> list[Reply]:
        calls = [_Call(mx.random.key(stream(s, c)), THINKING if thinking != 0 else ANSWERING)
                 for s, c in zip(seeds, contexts)]
        conductor = _Conductor(calls, thinking=thinking, max_tokens=max_tokens, total_limit=extra,
                               sampling=sampling, thought_sampling=thought_sampling, close=self.close,
                               end_of_turn=self.end_of_turn, end_tokens=self.end_tokens, out_of_time=self._out_of_time)
        gen = BatchGenerator(self.model, max_tokens=extra, stop_tokens=[[t] for t in sorted(self.end_tokens)],
                             sampler=conductor, completion_batch_size=self.width,
                             prefill_batch_size=min(self.prefill, self.width), prefill_step_size=READ_STEP)
        try:
            starts: dict = {}
            for k, which in enumerate(start_of):
                if which is not None and which not in starts:
                    starts[which] = self._read(contexts[k][:read_from[k]])
                elif which is not None:
                    self.spared_tokens += read_from[k]
            caches = [starts.get(which) for which in start_of]
            del starts
            self.read_tokens += sum(len(c) - at for c, at in zip(contexts, read_from))
            uids = gen.insert([c[at:] for c, at in zip(contexts, read_from)], caches=caches,
                              samplers=[conductor] * len(calls),
                              logits_processors=[[conductor.here(k)] for k in range(len(calls))],
                              stop_sequences=[self._end] * len(calls))
            del caches
            left = set(uids)
            observed = {uid: [] for uid in uids}
            steps = 0
            while left and (responses := gen.next_generated()):
                for response in responses:
                    observed[response.uid].append(response.token)
                    if response.finish_reason is not None:
                        left.remove(response.uid)
                steps += 1
                if steps % SETTLE_STEPS == 0:
                    settle(gen)
            if left:
                raise RuntimeError(f"Batch generator exited with {len(left)} unfinished requests")
            for uid, call in zip(uids, calls):
                if observed[uid] != call.emitted:
                    raise RuntimeError("Sampler trace differs from emitted tokens (mlx-lm changed?)")
        finally:
            gen.close()

        return [self._reply(context, seed, c, thinking) for context, seed, c in zip(contexts, seeds, calls)]

    def _reply(self, context: list[int], seed: int, c: _Call, thinking: int | None) -> Reply:
        """What a finished call wrote, as it is handed back."""
        self.new_tokens += len(c.emitted)
        self.sampled_tokens += c.sampled
        self.injected_tokens += c.injected
        said = c.answer[:-1] if c.answer and c.answer[-1] in self.end_tokens else c.answer
        thought_text, thought_tokens = "", None
        if thinking != 0:
            body = c.thought[:-1] if c.closed_itself or c.ended_turn else c.thought
            thought_text = self.tokenizer.decode(body).strip()
            thought_tokens = c.thought + c.leaving
            if c.closed_itself is None:
                c.closed_itself = False
        reasoning = self.tokenizer.decode(c.thought + c.leaving).split("</think>")[0] if thinking != 0 else ""
        return Reply(self.tokenizer.decode(said).strip(), c.answer, thought=thought_text, reasoning=reasoning,
            thought_tokens=thought_tokens, finished_thinking=c.closed_itself, stopped=c.stopped,
            finish_reason=c.finish_reason or "total_limit", seed=seed, prompt_tokens=len(context),
            sampled_tokens=c.sampled, injected_tokens=c.injected, injected_positions=c.injected_positions,
            output_tokens=c.emitted)

    # ---------------------------------------------------------------- conversations
    def converse(self, prompts: list[Prompt], seeds: list[int], respond, *, thinking: int | None = None,
                 max_tokens: int = 4096, max_total_tokens: int = 32768, sampling: Sampling | None = None,
                 thought_sampling: Sampling | None = None, tools: list[dict] | None = None, workers: int = 4,
                 at_once: int | None = None, known=None) -> None:
        """Carry on many conversations side by side, each at its own pace, reading nothing twice.

        `prompts[i]` opens conversation i and `seeds[i]` is its seed. When its reply is written,
        `respond(i, reply)` says how it goes on: `(prompt, seed)`, its next call, or None when it is over.
        The next call starts as soon as `respond` returns, whatever the other conversations are doing, so
        nobody waits for the slowest. `respond` runs on one of `workers` other threads (it is where a tool
        is run, and may take a while) and must not touch the engine.

        A call whose prompt begins with exactly the tokens its conversation has read and written so far
        carries on from there: only what is new is read. A chat's next prompt does, when the reply is passed
        back as it was written (`text` as the content, `reasoning` as the thought). When it does not (the
        reply was rewritten, or its tokens come back from the tokenizer cut differently), the whole prompt is
        read again. Either way the call is the one `generate` would make of that prompt and seed: carrying
        on changes what is read, never what is asked. Opening prompts with a shared start have it read once,
        as in `generate`.

        Memory is planned call by call. One starts when the calls in flight (at their full allowance, each
        as long as the longest, as a batch holds them) and the caches kept for the others fit the budget.
        When even a call by itself does not fit beside what is kept, kept caches are let go, largest first,
        and those conversations read their prompts again. `at_once` is the most conversations carried at a
        time: the rest are opened as these end. Give it when conversations grow long: opened all together
        they start side by side while they are short, and later most of them wait, their caches kept, for
        room to go on. Settings mean what they mean in `generate`, and `last_run` records every call.

        A conversation may wait for another. When how it goes on depends on something that has not happened
        yet (another conversation's reply, say), `respond` returns a `concurrent.futures.Future` of its
        answer in place of the answer. The conversation then holds no call and no worker, and keeps its
        cache, until the future is done. Whoever sets the future's result does so from another `respond`.
        If every conversation left is waiting and none is at work, nothing can let them go on, and the run
        stops with an error. With `at_once`, a conversation that waits for one that is not opened yet waits
        for ever: open them all.

        `known(i)`, if given, is asked once before each call of conversation i is written. A reply it
        returns (anything but None) goes to `respond` as it is, and nothing is written for that call: this
        is how a caller who keeps replies replays a conversation as far as it is remembered, in the same
        loop and on the same workers as the calls that are new. Such a call is not in `last_run["calls"]`;
        `last_run["known"]` counts them.
        """
        for name, value in (("max_tokens", max_tokens), ("max_total_tokens", max_total_tokens), ("workers", workers),
                            ("width", self.width), ("prefill", self.prefill), ("min_shared", self.min_shared),
                            *((("at_once", at_once),) if at_once is not None else ())):
            integer(name, value, 1)
        if thinking is not None:
            integer("thinking", thinking)
        sampling = sampling if sampling is not None else Sampling()
        thought_sampling = thought_sampling if thought_sampling is not None else sampling
        if not isinstance(sampling, Sampling) or not isinstance(thought_sampling, Sampling):
            raise ValueError("sampling and thought_sampling must be Sampling configurations")
        seeds = list(seeds)
        if len(seeds) != len(prompts):
            raise ValueError("seeds must have exactly one entry per prompt")
        for seed in seeds:
            integer("seed", seed)
        self.groups, self.last_run = [], {}
        if not prompts:
            return
        if thinking != 0 and self.close is None:
            raise ValueError(f"{self.name} has no </think> token; use thinking=0")
        started = time.perf_counter()
        mx.reset_peak_memory()
        extra = self._allowance(thinking, max_tokens, max_total_tokens)
        prefill = min(self.prefill, self.width, TALK_PREFILL)
        reading = self.read_fixed + prefill * READ_STEP * self.read_per_token

        def encode(prompt: Prompt, who: int) -> list[int]:
            context = self.encode(prompt, thinking=thinking != 0, tools=tools)
            if self.context_limit is not None and len(context) + extra > self.context_limit:
                raise ValueError(f"Conversation {who}: prompt + output allowance exceeds context limit {self.context_limit}")
            return context

        talks = [_Talk(i, encode(prompt, i), seed) for i, (prompt, seed) in enumerate(zip(prompts, seeds))]
        starts: dict[int, list] = {}          # shared starts: [the tokens shared, their cache once read, calls yet to take it]
        for which, (shared, members) in enumerate(clusters([t.context for t in talks], self.min_shared)):
            shared = min(shared, min(len(talks[m].context) for m in members) - 1)
            if shared * (len(members) - 1) >= self.min_shared:
                starts[which] = [talks[members[0]].context[:shared], None, len(members)]
                for m in members:
                    talks[m].start = which
        conductor = _Conductor([], thinking=thinking, max_tokens=max_tokens, total_limit=extra, sampling=sampling,
                               thought_sampling=thought_sampling, close=self.close, end_of_turn=self.end_of_turn,
                               end_tokens=self.end_tokens, out_of_time=self._out_of_time)
        gen = BatchGenerator(self.model, max_tokens=extra, stop_tokens=[[t] for t in sorted(self.end_tokens)],
                             sampler=conductor, completion_batch_size=self.width, prefill_batch_size=prefill,
                             prefill_step_size=READ_STEP)
        log: list[dict] = []
        self.last_run = {"engine": self.describe(), "conversations": len(prompts), "calls": log, "thinking": thinking,
                         "max_tokens": max_tokens, "max_total_tokens": max_total_tokens, "sampling": asdict(sampling),
                         "thought_sampling": asdict(thought_sampling), "share": True,
                         "tools": [tool.get("function", tool).get("name") for tool in tools] if tools else None,
                         "at_once": at_once, "status": "running"}
        before = (self.read_tokens, self.spared_tokens, self.new_tokens, self.sampled_tokens, self.injected_tokens)
        unopened: deque[_Talk] = deque(talks)      # conversations not begun yet
        waiting: deque[_Talk] = deque()            # begun, with a prompt, for room
        writing: dict[int, _Talk] = {}             # in the generator, by its uid
        deciding: dict[Future, _Talk] = {}         # reply written: `respond` at work, or its answer waited for
        promised: set[Future] = set()              # of those, the answers `respond` said would come later
        widest = reread = let_go = steps = open_ = recalled = 0
        pool = ThreadPoolExecutor(max_workers=workers)

        def queue(talk: _Talk) -> None:
            """A conversation's call goes in line to be written, or, if its reply is known, straight to `respond`."""
            nonlocal recalled
            reply = known(talk.index) if known is not None else None
            if reply is None:
                waiting.append(talk)
            else:
                recalled += 1
                deciding[pool.submit(respond, talk.index, reply)] = talk

        try:
            while unopened or waiting or writing or deciding:
                for future in [f for f in deciding if f.done()]:
                    talk = deciding.pop(future)
                    promised.discard(future)
                    went_on = future.result()
                    if isinstance(went_on, Future):            # how it goes on is not known yet: it waits
                        deciding[went_on] = talk
                        promised.add(went_on)
                        continue
                    if went_on is None:
                        talk.held, talk.cache = [], None
                        if (start := starts.get(talk.start)) is not None:      # it ended without taking the start it shares
                            start[2] -= 1
                            if not start[2]:
                                starts = {which: s for which, s in starts.items() if s is not start}
                        open_ -= 1
                        continue
                    prompt, talk.seed = went_on
                    integer("seed", talk.seed)
                    talk.context = encode(prompt, talk.index)
                    carries_on = len(talk.held) < len(talk.context) and talk.context[:len(talk.held)] == talk.held
                    if talk.cache is not None and not carries_on:
                        talk.held, talk.cache = [], None
                        reread += 1
                    queue(talk)
                while len(writing) < self.width:
                    while not waiting and unopened and (at_once is None or open_ < at_once):
                        open_ += 1
                        queue(unopened.popleft())                      # one more conversation is begun
                    if not waiting:
                        break
                    talk = waiting[0]
                    longest = max(len(t.context) for t in (talk, *writing.values())) + extra
                    kept = [t for t in talks if t.cache is not None and t is not talk]
                    held = sum(nbytes(t.cache) for t in kept) + sum(nbytes(start[1]) for start in starts.values())
                    each = FIXED_SPARE * self.fixed + TOKEN_SPARE * self.per_token * longest      # as `plan` counts a call
                    if (len(writing) + 1) * each + held + reading > self.room:
                        if writing:
                            break                              # when a call in flight is done
                        if not kept:
                            raise ValueError(f"Conversation {talk.index} needs an estimated {each / 2**30:.2f} GiB of cache "
                                             f"but only {(self.room - reading) / 2**30:.2f} GiB remains; reduce "
                                             "context/output limits or increase memory")
                        largest = max(kept, key=lambda t: nbytes(t.cache))
                        largest.held, largest.cache = [], None
                        let_go += 1
                        continue
                    waiting.popleft()
                    at, cache, start = len(talk.held), talk.cache, starts.get(talk.start)
                    talk.held, talk.cache, talk.start = [], None, None
                    if cache is None and start is not None:    # its first call to be written: the start it shares with
                        if talk.context[:len(start[0])] == start[0]:       # others, if its prompt still begins with it (it
                            if start[1] is None:                           # is a later prompt when its first replies were known)
                                start[1] = self._read(start[0])
                            else:
                                self.spared_tokens += len(start[0])
                            at, cache = len(start[0]), start[1]
                        start[2] -= 1
                        if not start[2]:
                            starts = {which: s for which, s in starts.items() if s is not start}
                    elif cache is not None:
                        self.spared_tokens += at
                    self.read_tokens += len(talk.context) - at
                    talk.call, talk.seen = _Call(mx.random.key(stream(talk.seed, talk.context)),
                                                 THINKING if thinking != 0 else ANSWERING), []
                    conductor.calls.append(talk.call)
                    (uid,) = gen.insert([talk.context[at:]], caches=[cache], samplers=[conductor],
                                        logits_processors=[[conductor.here(len(conductor.calls) - 1)]],
                                        stop_sequences=[self._end])
                    writing[uid] = talk
                    log.append({"conversation": talk.index, "seed": talk.seed, "prompt_tokens": len(talk.context),
                                "carried_tokens": at, "started": round(time.perf_counter() - started, 2),
                                "prompt_sha256": hashlib.sha256(np.asarray(talk.context, dtype="<i4").tobytes()).hexdigest()})
                    talk.entry = log[-1]
                    del cache
                widest = max(widest, len(writing))
                if writing:
                    responses = gen.next_generated()
                    if not responses:
                        raise RuntimeError(f"Batch generator exited with {len(writing)} unfinished requests")
                    steps += 1
                    if steps % SETTLE_STEPS == 0:
                        settle(gen)
                    for response in responses:
                        talk = writing[response.uid]
                        talk.seen.append(response.token)
                        if response.finish_reason is None:
                            continue
                        del writing[response.uid]
                        if talk.seen != talk.call.emitted:
                            raise RuntimeError("Sampler trace differs from emitted tokens (mlx-lm changed?)")
                        reply = self._reply(talk.context, talk.seed, talk.call, thinking)
                        reply.metadata = {"prompt_sha256": talk.entry["prompt_sha256"], "conversation": talk.index}
                        talk.entry.update(output_tokens=len(talk.call.emitted), finish_reason=reply.finish_reason,
                                          finished=round(time.perf_counter() - started, 2))
                        talk.held, talk.cache = talk.context + talk.call.emitted, own(response.prompt_cache)
                        deciding[pool.submit(respond, talk.index, reply)] = talk
                elif deciding:
                    if promised.issuperset(deciding) and not any(f.done() for f in deciding):
                        raise RuntimeError(f"{len(deciding)} conversations wait for each other and none is at work"
                                           + (f"; {len(unopened)} are not opened yet (at_once={at_once})" if unopened else ""))
                    wait(list(deciding), return_when=FIRST_COMPLETED)
        except BaseException:
            self.last_run["status"] = "failed"
            raise
        else:
            self.last_run["status"] = "complete"
            self.calls += len(log)
            self.prompt_tokens += sum(entry["prompt_tokens"] for entry in log)
        finally:
            gen.close()
            pool.shutdown(wait=True, cancel_futures=True)
            for talk in talks:
                talk.cache = None
            mx.clear_cache()
            elapsed = time.perf_counter() - started
            self.seconds += elapsed
            self.groups = [widest]
            now = (self.read_tokens, self.spared_tokens, self.new_tokens, self.sampled_tokens, self.injected_tokens)
            self.last_run.update(seconds=elapsed, widest=widest, read_again=reread, let_go=let_go, known=recalled,
                                 peak_memory_gb=round(mx.get_peak_memory() / 2**30, 2), usage=dict(zip(
                ("read_tokens", "spared_tokens", "output_tokens", "sampled_tokens", "injected_tokens"),
                (a - b for a, b in zip(now, before)))))
