"""A swarm working on problems: an `Arm` says what kind of swarm, `play` runs it.

    desk = Arm("desk", agents=12)                                  # the baseline: every agent alone at its desk
    swarm = desk.but("look_at_others", looks=RandomLooks())        # and now and then one reads another's file
    episodes = play(problems, swarm, backend, python)

An agent works in a Python file through a very simple harness (mathswarm/harness.py): one conversation that
carries on from step to step, and tools to write the file, edit it and submit. All the agents of a problem are
at work at once, each at its own pace (`Workshop`). Under an arm with `looks` (mathswarm/looks.py) an agent is
now and then shown another agent's file and writes a few sentences about it, which that agent is shown a step
later. An arm is one row of a results table. A new experiment is usually a few arms that differ in one field,
run on the same problems:

    ARMS = [desk, desk.but("look_at_self", looks=RandomLooks(at="own")), swarm]
"""
from __future__ import annotations

import hashlib
import re
import threading
from concurrent.futures import Future
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from swarm_engine import Sampling, trial_seed

from . import harness, looks, reading
from .grading import recorded
from .llm import Call, Reply
from .metrics import score
from .problems import Problem
from .python import Ran

# What stands in a run's settings for this file and for mathswarm/reading.py, which between them decide what an
# agent is shown and when, and what counts as its answer: a run is not carried on under other code than it began with.
VERSION = hashlib.sha256(Path(__file__).read_bytes() + Path(__file__).with_name("reading.py").read_bytes()).hexdigest()[:12]

NOTE = 500                # how much of what a reply says in words is kept in the log of steps, in characters
LOOK = 10_000             # sets the seed of an agent's look apart from the seeds of its steps
WAIT = object()           # an agent cannot go on yet: what it is to be shown has not happened
LONGEST = 210_000         # tokens. An agent whose conversation has come to more than this after a step takes no further
                          # step and holds what it holds, as one that has used its steps does. The model reads 262,144,
                          # a call that no longer fits stops the whole run (../swarm_engine), and between two steps an
                          # agent may be shown a file, be asked about it twice and hear from several others


@dataclass(frozen=True)
class Arm:
    """One kind of swarm. As it stands it is the baseline: agents at desks, set as `desk_work` found best, and
    nobody reading anybody."""
    name: str
    agents: int = 12                         # agents on each problem
    steps: int = 20                          # the most steps an agent takes: a step is one reply, a thought and then tool calls
                                             # (12 until 2026-10-12, and in every run before that but those that say otherwise)
    model: str | tuple[str, ...] = "9B"      # one model for every agent, or one per agent going round
    thinking: int | None = 1024              # tokens a step may think before its thought is closed; None: no limit; 0: none
    max_tokens: int = 5760                   # the most a step's reply may be: room for a whole file
    lines: int = harness.LINES               # how long a file may be: 300 lines. A file needs the room in a reply
                                             # (`max_tokens`), 19.2 tokens a line. Both were set on 2026-10-12; before
                                             # that they were 80 lines and 1,536 tokens, and `desk_work` measured those
    max_total_tokens: int = 16384            # the most thought and reply together may be (matters when thinking=None)
    sampling: Sampling | None = Sampling.coding()   # how a reply is drawn: tool calls are code, so Qwen's preset for precise
                                             # code. None: the engine's default, Qwen's general preset
    thought_sampling: Sampling | None = Sampling()  # how a thought is drawn: Qwen's general preset. None: as the reply is
    drafts: bool = False                     # a call that was cut off by the reply's length limit, and so not carried out,
                                             # stays in the agent's conversation as it was written. False takes it out: the
                                             # agent keeps its thought and is told it was cut off (the better: `desk_work`)
    system: str | None = None                # replaces what an agent is told (harness.SYSTEM)
    looks: object = None                     # who reads whose file, and when (mathswarm/looks.py). None: nobody reads anybody

    def but(self, name: str, **changes) -> "Arm":
        """This arm with a new name and some fields changed."""
        return replace(self, name=name, **changes)

    def model_of(self, seat: int) -> str:
        return self.model if isinstance(self.model, str) else self.model[seat % len(self.model)]

    def total_tokens(self) -> int:
        """Room for the whole reply: never less than the thought and the reply together, so that a thought
        that is closed at its budget still gets its reply."""
        if not self.thinking:
            return self.max_total_tokens
        return max(self.max_total_tokens, self.thinking + self.max_tokens + 64)

    @property
    def system_message(self) -> str:
        return self.system if self.system is not None else harness.system(self.steps, self.lines)

    def describe(self) -> dict:
        """Every setting, as it is written in a run's config.json. What the tools do and say is a setting too
        (`harness`), and so are the rules and words of a look (`contact`), for an arm that has looks, and the
        code that decides what an agent is shown and when (`workshop`). `own_words`: the arm was given what its
        agents are told (`system`); otherwise they are told the harness's words, which change with its version."""
        return {**asdict(self), "sampling": asdict(self.sampling or Sampling()), "system": self.system_message,
                "own_words": self.system is not None, "looks": looks.describe(self.looks), "harness": harness.VERSION,
                "contact": looks.VERSION if self.looks is not None else None, "workshop": VERSION}


@dataclass
class Step:
    """One step of one agent, as it is logged (a line of posts.jsonl)."""
    round: int                       # counted from 0: its step `round + 1`
    agent: int                       # counted from 0; agents are named from 1
    answer: str | None               # the answer it held after the step, as its file printed it
    note: str = ""                   # what its reply said in words, before its tool calls
    did: str = ""                    # the tools it called
    python: str | None = None        # its file as the step left it, if the step ran it
    check: Ran | None = None         # and what Python made of it
    recorded: str | None = None      # the answer as it is scored (grading.recorded); never shown to an agent


@dataclass(frozen=True)
class Stood:
    """How an agent's desk stood after one of its steps: what a reader is shown of it."""
    step: int
    file: str | None
    ran: Ran | None
    answer: str | None               # the answer its agent held: the last one a run without errors printed
    printed: str | None = None       # the answer the file as it stands printed, which is what a reader sees: None if
                                     # its last run stopped, or printed none


@dataclass
class Look:
    """One agent reading a file: who, when, what it was shown and what it wrote."""
    step: int                        # the reader had taken this many steps
    reader: int
    of: int                          # whose file: another agent's, or the reader's own (the control)
    seen: int | None = None          # the step of that agent after which its file stood as shown; None: it had none yet
    stopped: bool = False            # that agent had stopped work by then
    unread: bool = False             # what is said cannot reach that agent: it had stopped, or had one step left
    own: str | None = None           # the answer the reader held
    theirs: str | None = None        # the answer the agent whose file it is held, after that step
    printed: str | None = None       # the answer the file that was shown printed, when Python ran it
    said: str | None = None          # what the reader said, as it is passed on
    asks: int = 0                    # how often it was asked: twice, if it said nothing the first time
    called: bool = False             # a reply of its held a call to one of its own tools, which was not carried out
    heard: int | None = None         # the step of the other agent after which it was shown those words
    done: bool = False               # the reader has written, or there was nothing to read


class Workshop:
    """One problem on which every agent works at its own desk (mathswarm/harness.py): a Python file, three tools,
    and a conversation that carries on. Nobody waits for the others: an agent's next step is asked for as soon
    as its last has been carried out. In the logs, round r is every agent's step r + 1; an agent that submits
    holds its answer from then on.

    Under an arm with looks (mathswarm/looks.py) an agent's steps are sometimes followed by a turn in which it
    reads a file and writes about it, and by what another agent wrote about its own. The clock is the step
    count: a reader, after its step s, is shown the other's file as it stood after that agent's step s, and
    what it writes is read by that agent after its step s + 1. `step` therefore sometimes answers with a
    `Future` of an agent's next call: the agent waits, and only for the one agent it reads or is read by."""

    def __init__(self, problem: Problem, arm: Arm, seed: int = 0, python=None):
        if isinstance(arm.thinking, tuple):
            raise ValueError("an agent's steps are one conversation, which has one thought budget")
        if arm.looks is not None and not isinstance(arm.model, str):
            raise ValueError("agents who read each other's files run on one model: an agent waits for another only "
                             "while both are carried by the same engine")
        self.problem, self.arm, self.seed = problem, arm, seed
        python = python or NoPython()
        asked = replace(problem, answer=None)             # all that a desk is given of the problem: not its known answer

        def read(text: str) -> str | None:
            """What a file printed after `ANSWER:`, as an answer: `m + n = 371` is 371. Where the problem asks
            for a whole number, `204.0` and `1,024` are 204 and 1024, and `123.3` and `Done` are not answers."""
            value = text.rsplit("=", 1)[-1] if asked.answer_type != "text" else text
            answer = reading.answer(value, asked)
            if asked.answer_type != "integer":
                return answer
            whole = re.fullmatch(r"\+?(-?(?:\d{1,3}(?:,\d{3})+|\d+))(?:\.0*)?", (answer or "").strip("$ "))
            return whole.group(1).replace(",", "") if whole else None

        seats = range(arm.agents)
        self.desks = [harness.Desk(lambda code: python.check_many([code])[0], read, lines=arm.lines) for _ in seats]
        self.talk: list[list[dict]] = [[] for _ in seats]       # each agent's conversation after the problem
        self.news: list[list[str]] = [[] for _ in seats]        # what the call an agent is answering read that was new
        self.asked: list[Call | None] = [None for _ in seats]   # the call each agent is answering
        self.steps: list[Step] = []                             # every step taken, as it is logged
        self.calls: list[dict] = []                             # every model call, as it is logged
        self.answers: list[list[str | None]] = []               # where every agent stood after each step (`close`)
        self.invalid = 0
        # What follows is the same for every arm; without looks nothing in it ever makes an agent wait.
        self.lock = threading.Lock()                            # agents' steps are carried out on several threads at once
        self.plan = arm.looks.plan(problem.seed, seed, arm.agents, arm.steps) if arm.looks is not None else {}
        self.readers: dict[tuple[int, int], list[int]] = {}     # (an agent, a step): who reads its file as it stood then
        for (reader, step), of in sorted(self.plan.items()):
            if of != reader:
                self.readers.setdefault((of, step), []).append(reader)
        self.stood: list[list[Stood]] = [[] for _ in seats]     # how each agent's desk stood after each of its steps
        self.taken = [0 for _ in seats]                         # the steps each agent has taken
        self.over: list[int | None] = [None for _ in seats]     # the step with which an agent stopped
        self.outgrown: set[int] = set()                         # the agents that stopped because their conversation was too long
        self.looks: dict[tuple[int, int], Look] = {}            # (reader, step): every look that came due
        self.phase = ["step" for _ in seats]                    # what an agent's next reply is: a "step", or its "words" about
                                                                # a file. Between replies: to "look", then to "hear"; or "over"
        self.unsaid: list[list[str]] = [[] for _ in seats]      # what an agent is yet to be told before its next call
        self.waiting: dict[int, Future] = {}                    # the agents who cannot go on yet, and the call each is owed

    # ---- an agent's calls
    def call(self, seat: int) -> Call:
        """An agent's next call: the problem, and its conversation so far."""
        arm, look = self.arm, self.looks.get((seat, self.taken[seat]))
        attempt = self.taken[seat] + (LOOK * look.asks if self.phase[seat] == "words" else 0)
        self.asked[seat] = Call(arm.system_message, f"Problem:\n{self.problem.statement}",
                                trial_seed(self.seed * 2**32 + self.problem.seed, seat, attempt), arm.model_of(seat),
                                arm.thinking, arm.max_tokens, arm.total_tokens(), arm.sampling,
                                more=tuple(self.talk[seat]), tools=harness.tools(arm.lines), thought_sampling=arm.thought_sampling)
        return self.asked[seat]

    def step(self, seat: int, reply: Reply) -> Call | Future | None:
        """Take one reply of an agent: carry it out at its desk, or, if it was shown a file, keep its words about
        it. Returns the agent's next call; None once it has submitted or used its steps; or a `Future` of one
        of those, when what it is to be shown next has not happened yet (the file of an agent that has not got
        as far, or the words of one that has not written them). The future is set by the step of another agent.
        The reply goes back into the conversation as it was written, so that the model reads on from its own
        words (but for a call that was cut off, in an arm that keeps no such drafts).
        Agents' steps are carried out on several threads at once, and the answer checker cannot be used from
        them, so nothing is marked right or wrong here: `close` does that."""
        with self.lock:
            words = self.phase[seat] == "words"
        desk = self.desks[seat]
        runs = desk.did["runs"]
        results = None if words else desk.step(reply.text, cut=reply.finish_reason != "stop")     # its Python runs here
        with self.lock:
            mine = again = None
            if words:
                again = self._wrote(seat, reply)                # its next call, if it said nothing and is asked once more
            else:
                self._worked(seat, reply, results, ran=desk.did["runs"] > runs)
            if again is None and self.phase[seat] != "over":
                mine = self.waiting[seat] = Future()            # as if it had to wait: let go at once if it need not
            freed = self._let_go()
        went_on: Call | Future | None = again or mine
        for who, future, call in freed:                         # outside the lock: whoever hears of it may take a step
            if who == seat:
                went_on = call
            else:
                future.set_result(call)
        return went_on

    def _worked(self, seat: int, reply: Reply, results: list[list], ran: bool):
        """A step has been carried out at an agent's desk: put it in its conversation and in the logs, and note
        how its desk now stands for those who read it. `ran`: the step ran the file."""
        desk, asked, step = self.desks[seat], self.asked[seat], self.desks[seat].did["steps"]
        told = [reading.clean(text) for _, text in results]
        self.talk[seat].append(self._said(reply))
        self.steps.append(Step(step - 1, seat, desk.answer, reading.cut(" ".join(harness.said(reply.text).split()), NOTE),
                               did=", ".join(name or "no tool call" for name, _ in results),
                               python=desk.file if ran else None, check=desk.ran if ran else None))
        self.calls.append(self._logged(seat, step - 1, asked, reply, did=[[name or "", text] for (name, _), text in zip(results, told)]))
        self.taken[seat] = step
        printed = desk.read(desk.ran.answer) if desk.ran is not None and desk.ran.ok and desk.ran.answer is not None else None
        self.stood[seat].append(Stood(step, desk.file, desk.ran, desk.answer, printed))
        if not desk.done and step < self.arm.steps and reply.prompt_tokens + reply.tokens > LONGEST:
            self.outgrown.add(seat)                             # what it was shown and what it then wrote, in tokens
        if desk.done or step >= self.arm.steps or seat in self.outgrown:
            self.over[seat], self.phase[seat] = step, "over"
            self.talk[seat] += [{"role": "tool", "content": text} for text in told]      # nothing follows its last step
        else:
            self.unsaid[seat], self.phase[seat] = told, "look"

    def _wrote(self, seat: int, reply: Reply) -> Call | None:
        """An agent has replied to the file it was shown. If it said nothing of it, it is asked once more: this
        returns that call. Otherwise what it said is kept, to be passed on, and it goes on to its next step."""
        look = self.looks[seat, self.taken[seat]]
        words, others = looks.said(reply.text)
        words = reading.cut(reading.clean(words).strip(), looks.SAID)
        self.talk[seat].append({**self._said(reply), "content": looks.kept(reply.text)})     # without the calls not carried out
        look.called = look.called or bool(others)
        self.calls.append(self._logged(seat, look.step - 1, self.asked[seat], reply, did=[],
                                       look={"of": look.of, "seen": look.seen, "ask": look.asks}))
        if not words and look.asks < looks.ASKS:
            look.asks += 1
            return self._tell(seat, [" ".join([looks.NOT_KEPT.format(tools=", ".join(others))] * bool(others)
                                              + [looks.again(own=look.of == seat)])])
        look.said, look.done = words, True
        self.unsaid[seat] = [looks.after(others)]
        self.phase[seat] = "hear"
        return None

    def _said(self, reply: Reply) -> dict:
        cut = reply.finish_reason != "stop"
        kept = harness.finished(reply.text) if cut and not self.arm.drafts else reply.text
        return {"role": "assistant", "content": kept, "reasoning_content": reply.reasoning or reply.thought or ""}

    def _logged(self, seat: int, round_: int, asked: Call, reply: Reply, **more) -> dict:
        shown = self.news[seat]
        return {"round": round_, "agent": seat, "model": asked.model, "seed": asked.seed, "answer": self.desks[seat].answer,
                "right": None, "prompt": "\n\n".join(shown) if shown else asked.user, "thought": reply.thought,
                "reply": reply.text, **more, "finish_reason": reply.finish_reason,
                "finished_thinking": reply.finished_thinking, "tokens": reply.tokens, "thought_tokens": reply.thought_tokens,
                "prompt_tokens": reply.prompt_tokens, "cached": reply.cached}

    def _tell(self, seat: int, told: list[str]) -> Call:
        """Put what an agent is told at the end of its conversation, and make its next call."""
        self.talk[seat] += [{"role": "tool", "content": text} for text in told]
        self.news[seat], self.unsaid[seat] = told, []
        return self.call(seat)

    # ---- between two steps of an agent
    def _let_go(self) -> list[tuple[int, Future, Call]]:
        """Every agent that waited and can now go on: (agent, the future it was given, its next call). One
        agent going on may be what another waited for, so this is gone through until nobody moves."""
        freed, moved = [], True
        while moved:
            moved = False
            for who in list(self.waiting):
                if (call := self._move(who)) is not WAIT:
                    freed.append((who, self.waiting.pop(who), call))
                    moved = True
        return freed

    def _stood(self, of: int, step: int) -> Stood | object:
        """An agent's desk after its step `step`, or as it left it if it stopped before; WAIT if it has not got
        that far."""
        if len(self.stood[of]) >= step:
            return self.stood[of][step - 1]
        return self.stood[of][-1] if self.over[of] is not None else WAIT

    def _move(self, seat: int) -> Call | object:
        """The next call of an agent that is between two steps, or WAIT. First it reads a file, if it was picked
        to (`looks`); then it is told what its last step came to, and what others wrote about its own file a
        step ago. Nothing is changed while it has to wait, so this may be asked again and again."""
        step, desk = self.taken[seat], self.desks[seat]
        if self.phase[seat] == "look":
            of = self.plan.get((seat, step))
            stood = None if of is None else self._stood(of, step)
            if stood is WAIT:
                return WAIT
            self.phase[seat] = "hear"
            if stood is not None:
                stopped = self.over[of] is not None and self.over[of] <= step
                look = self.looks[seat, step] = Look(step, seat, of, own=desk.answer, theirs=stood.answer, printed=stood.printed,
                                                     stopped=stopped, unread=stopped or step >= self.arm.steps - 1)
                if stood.file is None:
                    look.done = True                            # it has no file yet: there is nothing to read
                else:
                    look.seen, look.asks, self.phase[seat] = stood.step, 1, "words"
                    shown = looks.shows(reading.clean(stood.file), stood.ran, self.arm.steps, own=of == seat, unread=look.unread)
                    return self._tell(seat, [*self.unsaid[seat], reading.clean(shown)])
        written = []
        for reader in self.readers.get((seat, step - 1), ()):
            look = self.looks.get((reader, step - 1))
            if look is None and self.over[reader] is not None and self.over[reader] < step:
                continue                                        # it stopped before it would have read this agent's file
            if look is None or not look.done:
                return WAIT                                     # it has not got that far, or has not written yet
            if look.said:
                written.append(look)
        for look in written:
            look.heard = step
        told = list(self.unsaid[seat])
        if (left := harness.steps_left(step, self.arm.steps, desk.answer)):
            told[-1] += "\n\n" + left                          # as at a desk alone; and not under another agent's words,
        told += [looks.heard(look.said) for look in written]    # where "submit it" would read as an answer to them
        self.phase[seat] = "step"
        return self._tell(seat, told)

    # ---- once every agent is done
    def close(self):
        """Put the steps in order, mark the answers agents held right or wrong, and note where everyone stood
        after each step."""
        if self.waiting or any(phase != "over" for phase in self.phase):
            raise RuntimeError(f"{self.problem.id}: {len(self.waiting)} agents were left waiting for each other")
        self.steps.sort(key=lambda step: (step.round, step.agent))
        self.calls.sort(key=lambda call: (call["round"], call["agent"], "look" in call))
        work = [call for call in self.calls if "look" not in call]
        for step, call in zip(self.steps, work, strict=True):
            step.recorded = recorded(self.problem, step.answer)
            call["right"] = step.recorded == self.problem.truth
        held: list[str | None] = [None] * self.arm.agents
        for round_ in range(self.arm.steps):
            for step in (s for s in self.steps if s.round == round_):
                held[step.agent] = step.recorded
            self.answers.append(list(held))
        for call in self.calls:
            if "look" in call:                                  # what it held when it read
                call["right"] = self.answers[call["round"]][call["agent"]] == self.problem.truth
        self.invalid = sum(call["answer"] is None for call in work)

    def told(self, seat: int) -> str:
        """One line for the log when an agent stops: what it holds and what it took."""
        desk, mine = self.desks[seat], [call for call in list(self.calls) if call["agent"] == seat]
        how = f"submitted in step {desk.did['steps']}" if desk.done else f"out of steps after {desk.did['steps']}"
        read = len({call["round"] for call in mine if "look" in call})
        return (f"{self.problem.id} agent {seat + 1}: {desk.answer or 'no answer'} (known answer {self.problem.truth}), {how}; "
                f"{desk.did['runs']} runs ({desk.did['runs_clean']} with no errors)" + (f", read {read} files" if read else "")
                + f", {sum(call['tokens'] for call in mine):,} tokens written")

    # ---- what is logged
    def row(self) -> dict:
        """One line of episodes.jsonl: where every agent stood after every step, the scores, what each agent did
        at its desk, and every look."""
        tags = {"arm": self.arm.name, "benchmark": self.problem.benchmark, "split": self.problem.split,
                "problem": self.problem.id, "seed": self.seed, "truth": self.problem.truth}
        work = [{"agent": seat, "steps": desk.did["steps"], "writes": desk.did["write_file"], "edits": desk.did["edit_file"],
                 "edits_near": desk.did["edit_near"], "edits_failed": desk.did["edit_failed"], "runs": desk.did["runs"],
                 "runs_clean": desk.did["runs_clean"], "no_call": desk.did["no_call"], "unknown_tool": desk.did["unknown_tool"],
                 "cut_off": desk.did["cut_off"], "too_long": desk.did["too_long"], "submitted": desk.did["steps"] if desk.done else None,
                 "lines": len(desk.file.splitlines()) if desk.file else 0}
                for seat, desk in enumerate(self.desks)]
        steps = [call for call in self.calls if "look" not in call]
        return {**tags, "agents": self.arm.agents, "steps": self.arm.steps, "answers": self.answers,
                **score(self.answers, self.problem.truth), "calls": len(self.calls), "invalid": self.invalid,
                "outgrown": sorted(self.outgrown),
                "cut_thoughts": sum(c["finished_thinking"] is False for c in self.calls),
                "tokens": sum(c["tokens"] for c in self.calls), "posts": len(self.steps),
                # one entry per step: round, agent, tokens of thought, whether the thought ended by itself, right
                "thoughts": [[c["round"], c["agent"], c["thought_tokens"], c["finished_thinking"], c["right"]] for c in steps],
                "work": work, "looks": [self._look(look) for _, look in sorted(self.looks.items(), key=lambda item: (item[0][1], item[0][0]))]}

    def _look(self, look: Look, words: bool = False) -> dict:
        """A look as it is logged: answers in the form they are scored in. `words`: with what was written."""
        own, theirs = recorded(self.problem, look.own), recorded(self.problem, look.theirs)
        return {"step": look.step, "reader": look.reader, "of": look.of, "seen": look.seen, "stopped": look.stopped,
                "unread": look.unread, "own": own, "theirs": theirs, "printed": recorded(self.problem, look.printed),
                "heard": look.heard, "words": len(look.said or ""), "asks": look.asks, "called": look.called,
                **({"said": look.said} if words else {})}

    def post_rows(self) -> list[dict]:
        tags = {"arm": self.arm.name, "benchmark": self.problem.benchmark, "problem": self.problem.id}
        return [{**tags, "round": s.round, "agent": s.agent, "answer": s.answer, "recorded": s.recorded,
                 "right": s.recorded == self.problem.truth, "note": s.note, "check": asdict(s.check) if s.check else None,
                 "did": s.did, **({"python": s.python} if s.python else {})} for s in self.steps]

    def call_rows(self) -> list[dict]:
        tags = {"arm": self.arm.name, "benchmark": self.problem.benchmark, "problem": self.problem.id}
        return [{**tags, **call} for call in self.calls]

    def look_rows(self) -> list[dict]:
        """One line of looks.jsonl for every look, with the words that were written."""
        tags = {"arm": self.arm.name, "benchmark": self.problem.benchmark, "problem": self.problem.id, "truth": self.problem.truth}
        return [{**tags, **self._look(look, words=True)} for _, look in sorted(self.looks.items(), key=lambda item: (item[0][1], item[0][0]))]


class NoPython:
    """Stands in when there is no sandbox to run agents' Python in: every file comes back not run."""

    def check_many(self, codes: list[str]) -> list[Ran]:
        return [Ran("unavailable", error="there is no sandbox here to run it in") for _ in codes]


def carry_on(backend, calls: list[Call], then, at_once: int | None = None):
    """Answer each call, then the call that `then(index, reply)` makes of the reply, and so on until it makes
    none. `then` may answer with a `Future` of the next call: that conversation waits for another's reply. A
    backend that carries conversations on (`backend.converse`: the local models, through ../swarm_engine) lets
    each go at its own pace and reads nothing twice, `at_once` of them at a time; any other is asked a round at
    a time."""
    if hasattr(backend, "converse"):
        return backend.converse(calls, then, at_once)
    live, waiting = dict(enumerate(calls)), {}
    while live or waiting:
        if not live:
            raise RuntimeError(f"{len(waiting)} conversations wait for each other and none can go on")
        replies = backend(list(live.values()))
        asked, live = live, {}
        for i, reply in zip(asked, replies, strict=True):
            went_on = then(i, reply)
            (waiting if isinstance(went_on, Future) else live)[i] = went_on
        for i in [i for i, future in waiting.items() if future.done()]:
            live[i] = waiting.pop(i).result()
        live = {i: call for i, call in live.items() if call is not None}


def play(problems: list[Problem], arm: Arm, backend, python=None, seed: int = 0, progress=None,
         desks: int | None = None) -> list[Workshop]:
    """Run `arm` on every problem, side by side, and return the finished episodes in the problems' order.
    `backend` answers model calls (mathswarm/llm.py). `python` runs the agents' files (mathswarm/python.py).
    `progress` is told of each reply as it is taken (episode, agent, whether the agent has stopped).
    `desks` is how many agents work at once: the rest begin as these stop, which keeps the model's memory for
    conversations that are going on. It is for agents who work alone. Under an arm with looks every agent is
    open from the start, whatever `desks` says: an agent may read the file of any other, and reads it as it
    stood after as many steps as it has taken itself."""
    episodes = [Workshop(problem, arm, seed, python) for problem in problems]
    seats = [(episode, seat) for episode in episodes for seat in range(arm.agents)]

    def then(i: int, reply: Reply) -> Call | Future | None:
        episode, seat = seats[i]
        went_on = episode.step(seat, reply)
        if progress:
            progress(episode, seat, went_on is None)
        return went_on

    carry_on(backend, [episode.call(seat) for episode, seat in seats], then, None if arm.looks is not None else desks)
    for episode in episodes:
        episode.close()
    return episodes
