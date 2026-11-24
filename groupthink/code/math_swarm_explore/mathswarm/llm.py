"""Model calls. Everything that reaches a model goes through a backend: a function from calls to replies.

    Engine()      the local models, through ../swarm_engine (one model loaded at a time, calls side by side):
                  on this Mac through MLX, on a GPU through a vLLM server. The model's name says which
                  ("9B" is the Mac's build, "9B-bf16" the GPU's: ../swarm_engine/swarm_engine/models.py)
    Scripted()    rule-following stand-ins that need no model: for tests and `lab run --dry-run`

A backend may also carry conversations on (`converse`): each call, then whatever is made of its reply, with
every conversation at its own pace and nothing read twice. That is how agents at desks are run. A conversation
may wait for another: what is made of a reply may be a `Future` of the next call.

A `Call` is one chat (a system and a user message, and the conversation that followed: `more`) with everything
that decides its reply: the model, the seed and the decoding settings. Replies are kept in
data/cache/replies.sqlite under exactly those, so

  - arms whose agents are told the same share their replies: an agent under an arm with looks is the same agent
    as under the arm without, reply for reply, until it is first shown something the other is not;
  - a run that stops is resumed from what it had, and replaying a finished run costs nothing;
  - an arm that differs from another only in the most a reply may be (`max_tokens`) shares every reply that
    ended by itself and fits: the two are the same agents, reply for reply, until the limit first cuts one.

A new `--seed` is a new draw. A fine-tuned model is a different model: a local model is identified by its
folder and by the size and date of its weight files, so retraining in place does not return stale replies.
"""
from __future__ import annotations

import ast
import gc
import hashlib
import json
import os
import re
import sqlite3
import sys
import threading
import time
import zlib
from concurrent.futures import Future
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
from swarm_engine import Sampling

from .paths import CACHE, MODELS, ROOT
from .problems import Problem


@dataclass(frozen=True)
class Call:
    system: str
    user: str
    seed: int
    model: str = "9B"                     # "4B", "9B", a folder under models/, any folder or Hugging Face name
    thinking: int | None = None           # None: think until done. 0: no thinking. N: thought closed at N tokens
    max_tokens: int = 768                 # the most the answer may be
    max_total_tokens: int = 16384         # the most the whole reply may be, thought included
    sampling: Sampling | None = None      # None: the engine's default (Qwen3.5's general thinking preset)
    more: tuple = ()                      # the conversation after the user message: assistant and tool messages
    tools: tuple = ()                     # function schemas offered to the model (mathswarm/harness.py)
    thought_sampling: Sampling | None = None    # None: the thought is drawn as the answer is; else its own policy


@dataclass
class Reply:
    text: str
    thought: str = ""
    reasoning: str = ""                   # the thought as the model had it before it when it answered: with the words that
                                          # closed it, when its budget ran out. What a conversation that carries on passes back
    finish_reason: str = "stop"           # stop, answer_limit, total_limit, end_in_thought
    finished_thinking: bool | None = None  # False if the thought was cut; None if thinking was off
    tokens: int = 0                       # everything written: thought and answer
    thought_tokens: int = 0
    prompt_tokens: int = 0
    cached: bool = False                  # recalled rather than generated now


# ---------------------------------------------------------------- remembered replies

class Memo:
    def __init__(self, path: Path | None = CACHE / "replies.sqlite"):
        self.db, self.lock = None, threading.Lock()          # conversations that are carried on ask from several threads
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            # a job on a rented machine has its caches copied whole every few minutes, and a write waits for that
            self.db = sqlite3.connect(path, check_same_thread=False, timeout=120)
            self.db.execute("create table if not exists replies (key text primary key, reply text, at text)")

    @staticmethod
    def key(call: Call, identity: str) -> str:
        settings = asdict(call) | {"model": identity, "sampling": asdict(call.sampling or Sampling())}
        for late in ("more", "tools", "thought_sampling"):      # left out when empty, so that a plain call keeps the
            if not settings[late]:                              # key it had before these existed
                del settings[late]
        return hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def any_length(call: Call, identity: str) -> str:
        """Where a reply that ended by itself is noted as well: under its call with the limit on the answer left out."""
        return "any length " + Memo.key(replace(call, max_tokens=0), identity)

    def recall(self, call: Call, identity: str) -> Reply | None:
        """The reply kept for a call. If there is none: the reply kept for the same call under another limit on
        its answer, when that reply ended by itself and fits this call's limit. What a model writes does not
        depend on a limit it did not reach, so an arm that gives its agents more room for a reply is paired with
        the arm that gives less, reply for reply, until the limit first cuts one."""
        key = self.key(call, identity)
        if (kept := self.get(key)) is not None:
            self.share(call, identity, key, kept)          # a reply kept before replies were shared this way
            return kept
        if self.db is None:
            return None
        with self.lock:
            row = self.db.execute("select reply from replies where key = ?", (self.any_length(call, identity),)).fetchone()
        kept = self.get(json.loads(row[0])["same as"]) if row else None
        fits = kept is not None and kept.finish_reason == "stop" and kept.tokens - kept.thought_tokens < call.max_tokens
        return kept if fits else None

    def keep(self, call: Call, identity: str, reply: Reply):
        key = self.key(call, identity)
        self.put(key, reply)
        self.share(call, identity, key, reply)

    def share(self, call: Call, identity: str, key: str, reply: Reply):
        """Note, under the call without its limit, where a reply that ended by itself is kept. The first such
        reply stays the one that is shared, so that what was recalled once is recalled again."""
        if self.db is None or reply.finish_reason != "stop":
            return
        with self.lock:
            free = self.any_length(call, identity)
            if self.db.execute("select 1 from replies where key = ?", (free,)).fetchone() is None:
                self.db.execute("insert or ignore into replies values (?, ?, ?)",
                                (free, json.dumps({"same as": key}), time.strftime("%Y-%m-%d %H:%M:%S")))
                self.db.commit()

    def get(self, key: str) -> Reply | None:
        with self.lock:
            row = self.db.execute("select reply from replies where key = ?", (key,)).fetchone() if self.db else None
        if row is None:
            return None
        kept = {key: value for key, value in json.loads(row[0]).items() if key in Reply.__dataclass_fields__}      # of the fields there are now
        return Reply(**(kept | {"cached": True}))

    def put(self, key: str, reply: Reply):
        if self.db is not None:
            with self.lock:
                self.db.execute("insert or replace into replies values (?, ?, ?)",
                                (key, json.dumps(asdict(reply) | {"cached": False}), time.strftime("%Y-%m-%d %H:%M:%S")))
                self.db.commit()


# ---------------------------------------------------------------- the local models

def resolve(model: str) -> str:
    """A model as the engine wants it named: an alias, or the full path of a local folder."""
    for folder in (MODELS / model, ROOT / model, Path(model).expanduser()):
        if folder.is_dir() and (folder / "config.json").exists():
            return str(folder.resolve())
    return model


def identity(model: str) -> str:
    """What makes two models the same for the purpose of reusing a reply."""
    name = resolve(model)
    folder = Path(name)
    if folder.is_dir():
        weights = sorted((f.name, f.stat().st_size, int(f.stat().st_mtime))
                         for f in folder.iterdir() if f.suffix in (".safetensors", ".json", ".jinja"))
        return f"{name}#{hashlib.sha256(json.dumps(weights).encode()).hexdigest()[:16]}"
    from swarm_engine.models import MODELS as ALIASES, REVISIONS
    return f"{ALIASES.get(name, name)}@{REVISIONS.get(name, 'unpinned')}"


class Engine:
    """The local models. Call it with a list of `Call`s; it answers in the same order.

    Calls are grouped by model and settings and each group goes to the engine as one batch, which the engine
    cuts to fit in memory. One model is loaded at a time: a swarm that mixes models pays a reload each time the
    model changes, so calls are sorted to change it as rarely as possible. `width` is the most calls side by
    side; left out, each kind of engine has its own (100 on the Mac, what the server has room for on a GPU).
    """

    def __init__(self, memo: Memo | None = None, record=None, say=print, width: int | None = None):
        self.memo = memo if memo is not None else Memo()
        self.record = record or (lambda row: None)     # called with one row per engine batch (seeds, tokens, time)
        self.say, self.width = say, width
        self.loaded: tuple[str, object] | None = None
        self.calls = self.generated = self.tokens = self.read = self.spared = 0
        self.seconds = 0.0
        self._identity: dict[str, str] = {}

    def _engine(self, model: str):
        import swarm_engine
        name = resolve(model)
        if self.loaded is None or self.loaded[0] != name:
            self.unload()
            started = time.time()
            self.loaded = (name, swarm_engine.backend(name, **({"width": self.width} if self.width else {})))
            self.say(f"loaded {name} in {time.time() - started:.0f}s")
        return self.loaded[1]

    def unload(self):
        """Let the model go: its memory on a Mac, and on a GPU the server this started for it (one that was
        already up is left up)."""
        if self.loaded is None:
            return
        engine, self.loaded = self.loaded[1], None
        if hasattr(engine, "close_server"):
            engine.close_server()
        else:
            import mlx.core as mx
            del engine
            gc.collect()
            mx.clear_cache()

    def __call__(self, calls: list[Call]) -> list[Reply]:
        replies: list[Reply | None] = [None] * len(calls)
        groups: dict[tuple, list[int]] = {}
        for at, call in enumerate(calls):
            if call.model not in self._identity:
                self._identity[call.model] = identity(call.model)
            if (kept := self.memo.recall(call, self._identity[call.model])) is not None:
                replies[at] = kept
            else:
                groups.setdefault(settings(call), []).append(at)
        self.calls += len(calls)
        for (model, thinking, max_tokens, max_total_tokens, sampling, thought_sampling, tools), where in sorted(groups.items(), key=lambda g: g[0][0]):
            engine = self._engine(model)
            written = engine.generate([chat(calls[at]) for at in where],
                                      seeds=[calls[at].seed for at in where], thinking=thinking, max_tokens=max_tokens,
                                      max_total_tokens=max_total_tokens, sampling=sampling, thought_sampling=thought_sampling,
                                      tools=json.loads(tools) or None)
            run = engine.last_run
            self.record({"model": self._identity[model], "calls": len(where), "batches": engine.groups,
                         "seconds": round(run["seconds"], 1), **run["usage"], "thinking": thinking,
                         "max_tokens": max_tokens, "max_total_tokens": max_total_tokens, "sampling": run["sampling"],
                         "seeds": run["seeds"], "prompt_tokens": run["prompt_tokens"],
                         "prompt_sha256": run["prompt_sha256"], "engine": run["engine"]})
            self.generated += len(where)
            self.tokens += run["usage"]["output_tokens"]
            self.seconds += run["seconds"]
            self.read += run["usage"]["read_tokens"]
            self.spared += run["usage"]["spared_tokens"]
            for at, r in zip(where, written, strict=True):       # a reply for every call, or stop here
                replies[at] = self._keep(calls[at], r)
        return replies

    def _keep(self, call: Call, r) -> Reply:
        """An engine's reply as it is handed on, and remembered."""
        reply = Reply(r.text, r.thought, r.reasoning, r.finish_reason, r.finished_thinking, r.sampled_tokens + r.injected_tokens,
                      len(r.thought_tokens or ()), r.prompt_tokens)
        self.memo.keep(call, self._identity[call.model], reply)
        return reply

    def converse(self, calls: list[Call], then, at_once: int | None = None):
        """Answer each call, then the call that `then(index, reply)` makes of the reply, and so on until it makes
        none: every conversation at its own pace, and nothing it has read or written read again (the engine's
        `converse`). `then` is called from other threads, a conversation at a time. It may answer with a
        `Future` of the next call: the conversation then waits, for as long as it takes another one to set it.
        A reply that is remembered is not written again, and goes to `then` in the same loop as the replies
        that are written: a conversation is replayed as far as the cache goes and carried on from there, and
        one that waits for another waits whether that one is replayed or written.
        A conversation keeps the settings it started with. `at_once` is the most conversations carried at a
        time; the rest begin as these end."""
        lock, groups = threading.Lock(), {}
        for i, call in enumerate(calls):
            if call.model not in self._identity:
                self._identity[call.model] = identity(call.model)
            groups.setdefault(settings(call), {})[i] = call
        for kind, live in sorted(groups.items(), key=lambda group: group[0][0]):
            model, thinking, max_tokens, max_total_tokens, sampling, thought_sampling, tools = kind
            engine, who = self._engine(model), list(live)

            def known(k: int) -> Reply | None:
                return self.memo.recall(live[who[k]], self._identity[model])

            def goes_on(k: int, call: Call | None):
                """A conversation's next call as the engine takes it."""
                if call is None:
                    return None
                if settings(call) != kind:
                    raise ValueError("a conversation that is carried on keeps its model and settings from call to call")
                live[who[k]] = call
                return chat(call), call.seed

            def respond(k: int, r):
                i = who[k]
                if isinstance(r, Reply):                    # remembered: `known` handed it over
                    with lock:
                        self.calls += 1
                    went_on = then(i, r)
                else:
                    went_on = then(i, self._keep(live[i], r))
                return after(went_on, lambda call: goes_on(k, call)) if isinstance(went_on, Future) else goes_on(k, went_on)

            engine.converse([chat(live[i]) for i in who], [live[i].seed for i in who], respond, thinking=thinking,
                            max_tokens=max_tokens, max_total_tokens=max_total_tokens, sampling=sampling,
                            thought_sampling=thought_sampling, tools=json.loads(tools) or None, at_once=at_once,
                            known=known, workers=WORKERS)
            run = engine.last_run
            self.record({"model": self._identity[model], "conversations": len(who), "calls": len(run["calls"]), "at_once": at_once,
                         "batches": engine.groups, "seconds": round(run["seconds"], 1), **run["usage"],
                         "read_again": run["read_again"], "let_go": run["let_go"], "known": run.get("known"), "widest": run.get("widest"),
                         "peak_memory_gb": run.get("peak_memory_gb"), "thinking": thinking,
                         "max_tokens": max_tokens, "max_total_tokens": max_total_tokens, "sampling": run["sampling"],
                         "seeds": [c["seed"] for c in run["calls"]], "prompt_tokens": [c["prompt_tokens"] for c in run["calls"]],
                         "carried_tokens": [c["carried_tokens"] for c in run["calls"]],
                         "output_tokens_each": [c.get("output_tokens") for c in run["calls"]],
                         "conversation": [who[c["conversation"]] for c in run["calls"]],          # as the caller numbered them
                         "started": [c.get("started") for c in run["calls"]], "finished": [c.get("finished") for c in run["calls"]],
                         "prompt_sha256": [c["prompt_sha256"] for c in run["calls"]], "engine": run["engine"]})
            self.calls += len(run["calls"])
            self.generated += len(run["calls"])
            self.tokens += run["usage"]["output_tokens"]
            self.read += run["usage"]["read_tokens"]
            self.spared += run["usage"]["spared_tokens"]
            self.seconds += run["seconds"]


# How many replies are taken at once: each runs an agent's file, which may take its 30 seconds. On the Mac the
# model writes a few replies a second at most and eight keep up. A GPU writes many times that, so there it is
# most of the machine's processors (a rented one has about thirty).
WORKERS = 8 if sys.platform == "darwin" else max(8, min(64, (os.cpu_count() or 8) - 4))


def after(first: Future, then) -> Future:
    """A future of what `then` makes of `first`'s result, set as soon as `first` is."""
    later: Future = Future()

    def done(first: Future):
        try:
            later.set_result(then(first.result()))
        except BaseException as error:                      # whoever waits for it is told, instead of waiting for ever
            later.set_exception(error)
    first.add_done_callback(done)
    return later


def settings(call: Call) -> tuple:
    """What calls must share to go to the engine together: the model and how its reply is drawn."""
    return (call.model, call.thinking, call.max_tokens, call.max_total_tokens, call.sampling, call.thought_sampling,
            json.dumps(call.tools))


def chat(call: Call) -> tuple[str, str] | list[dict]:
    """A call as the engine takes it: (system, user), or the whole conversation when it has gone on."""
    if not call.more:
        return call.system, call.user
    return [{"role": "system", "content": call.system}, {"role": "user", "content": call.user}, *call.more]


# ---------------------------------------------------------------- stand-ins that need no model

def wrong(problem: Problem, which: int) -> str:
    """A wrong answer of the right kind. `which` picks among a few, so that scripted agents can agree on one."""
    kind = problem.answer_type
    if kind == "choice":
        others = [letter for letter in problem.letters if letter != problem.answer]
        return others[which % len(others)]
    if kind == "integer":
        return str(int(problem.answer) + 1 + which % 3)
    if kind == "float":
        return f"{float(problem.answer) * (2 + which % 3) + 1:.4g}"
    if kind.startswith("list"):
        return "[" + ", ".join(f"{float(x) * (2 + which % 3) + 1:.4g}" for x in problem.answer) + "]"
    return [text for text in ("0", "1", "unknown", "none of these") if text != problem.truth][which % 3]


class Scripted:
    """Agents that follow a few rules instead of thinking. An agent writes a Python file, edits it so that it
    prints an answer, and submits, a step at a time: the right answer with probability `skill`, and otherwise
    one of three wrong ones. `stay` is how many steps it lets pass before it submits (it writes its file out
    again and nothing changes). Shown a file to read, it says what its own file prints. Told of another answer
    than its own, by a file it read or by words about its own file, it takes that answer with probability
    `conform`.

    They are for checking that the machinery runs and counts correctly, not for results: `conform` is a dial,
    not a finding."""

    def __init__(self, problems: list[Problem], skill: float = 0.35, conform: float = 0.6, stay: int = 0):
        self.problems = {p.statement: p for p in problems}
        self.skill, self.conform, self.stay = skill, conform, stay
        self.calls = 0

    def __call__(self, calls: list[Call]) -> list[Reply]:
        self.calls += len(calls)
        return [self.one(call) for call in calls]

    def one(self, call: Call) -> Reply:
        from . import looks
        from .harness import written
        rest = call.user.split("Problem:\n", 1)[1]
        problem = next(p for statement, p in self.problems.items() if rest.startswith(statement))
        rng = np.random.default_rng([call.seed % 2**32, zlib.crc32(call.user.encode())])
        worked = re.compile(r"<function=(?!say>)")                         # a step, and not what it said of a file it was shown
        said = [m["content"] for m in call.more if m["role"] == "assistant"]
        step = sum(bool(worked.search(text)) for text in said)             # the steps it has taken
        prints = [ast.literal_eval(inside) for inside in re.findall(r"""print\(((?:'|")ANSWER: .*)\)""", "\n".join(said))]
        holds = prints[-1].removeprefix("ANSWER: ") if prints else None     # what its file prints, as it last wrote it
        since = len(call.more) - next((back for back, m in enumerate(reversed(call.more)) if m["role"] == "assistant" and worked.search(m["content"])),
                                      len(call.more))
        told = [m["content"] for m in call.more[since:] if m["role"] == "tool"]     # what it was told since its last step
        answer = problem.truth if rng.random() < self.skill else wrong(problem, int(rng.integers(3)))
        file = "two = 1 + 1\nprint({!r})".format
        if told and looks.asks(told[-1]):                                  # it is shown a file, and writes about it
            text = written("say", words=f"My file prints ANSWER: {holds}" if holds else "I have no answer yet.")
        elif step == 0:
            text = written("write_file", content="two = 1 + 1\nprint(two)")
        elif step == 1:
            text = "Now the answer.\n\n" + written("edit_file", old="print(two)", new=f"print({'ANSWER: ' + answer!r})")
        else:
            others = [found for text in told if looks.asks(text) or looks.tells(text)
                      for found in re.findall(r"ANSWER: ([^'\n]+?)'?$", text, re.M) if found != holds]
            if others and rng.random() < self.conform:
                text = "I take that answer.\n\n" + written("write_file", content=file("ANSWER: " + others[-1]))
            elif step < 2 + self.stay:
                text = written("write_file", content=file("ANSWER: " + holds))      # the same file again: nothing changes
            else:
                text = written("submit")
        return Reply(text, thought=f"(scripted step {step + 1})", finished_thinking=True, tokens=60, thought_tokens=10,
                     prompt_tokens=(len(call.user) + sum(len(str(m)) for m in call.more)) // 4)
