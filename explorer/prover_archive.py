"""The prover archive: exploring and proving in one loop, with no oracle. It joins exploring by counterfactual
verbalized sampling (CFVS: evs.py) and prover swarms (swarm_play.py), in the manner of quality-diversity
optimization (MAP-Elites): an archive of agents, a parent drawn uniformly, a variation of it rolled out.

1. Seed. A fresh agent works on the problem (the scratchpad, no submit tool) until it stops, or SEED_TURNS turns;
   asked (BELIEF) what it would submit, that is its first answer. It goes to the judge (5) as a rollout does.
2. Experiment. An answer the judge passes is handed to a prover swarm: swarm_play.Swarm as the swarm playground runs it (SYSTEM,
   PROMPT, Slack, the shared workspace, the nudge, compaction), told the answer and what proving it takes (its
   "halves": the claims that show it is the answer and that no other is, two or not). The halves are
   written for the answer by the model (HALVES_ASK, from other problems' halves as examples, never this one's), since
   the answer can be anything. The swarm ends as a swarm does, at its budget (`exp_budget`), or as soon as every
   agent is idle and no nudge will come (Swarm `settle`: both nudges used, or the judge found the proof complete). Then REPORT reads its
   channel and each agent's last reply and writes what it established, with a status (proved, partial, contradicted,
   none), which is what agents are told of it. Whether the archive stops (`stop_rule` "verify", the default since
   2026-11-06; verifier.py): the told answer must have the form a complete answer takes (the answer contract, once
   per problem), and then a verifier, an agent with the swarm's whole record (workspace, channel, every agent's
   transcript) that reruns its code in the sandbox, must find the proof sound, with no gap the team itself
   acknowledged. If so, the archive ends there. (`stop_rule` "manager": MANAGER decides whether it is a new result
   beyond the literature and the earlier experiments, as before 2026-11-06.) The agent
   whose answer it was is told the result (EXPERIMENT, a user message), and its runs may read the swarm's workspace
   (experiments/<e>/ next to its scratchpad, read-only).
3. Options. CFVS (evs.md without its turn count: 3 counterfactuals x 3 approaches, one call) is asked of the agent,
   and with the continuation (its own next step, no approach) gives its options: up to 10. They are kept with the
   agent, which only now joins the archive. An agent whose answer starts an experiment gets them at once, so the
   tree can explore from it while the swarm proves, and when the experiment has been read, up to 10 more, asked
   with the result known (branches e<i>/...).
4. Rollout. A member is drawn uniformly (among those with an option left), and one of its options left uniformly
   (or the page's pick, first): the agent's conversation (each step's counterfactual relabelled as an assumption,
   evs.RELABEL) and a copy of its scratchpad, told the counterfactual as verified and the approach (evs.VERIFIED, as
   the explore runs' default), takes a step of up to `step_turns` turns, ending early only at a turn that calls no
   tool. (Not at a run with exit code 0, swarm.ends, as the explore runs' steps: gpt-6.1-sol makes one call a turn,
   so 72 of the 82 rollouts of 20261104-221825-p43 ended at their first run, often one that only listed files.)
   It is asked BELIEF.
5. Judge. JUDGE decides whether the agent's answer claims anything (a value, bounds, a range ...: not "I don't have
   an answer" or a bare "unknown") and compares it with every answer an experiment has had (or is having): a claim
   different from them all starts an experiment (2, for the new agent); either way the agent gets its options (3)
   and joins the archive. So no experiment runs until some agent's answer claims something. With `gate` "definite"
   (the default since 2026-11-20), a new claim starts one only if it also has the answer contract's form (the stop
   rule's gate, verifier.definite, asked once per answer): proved, bounds or "not known" could never end the archive,
   so they aren't sent to a swarm. `gate` "claim" sends every new claim, as before.
   `workers` rollouts go on at once, and `max_experiments` experiments. While an experiment runs, the tree waits:
   only `wait_rollouts` drawn rollouts may start after one starts (the page's picks always may).
6. News. A rollout's agent is first told (NEWS, a user message) every experiment that has been read since it, or its
   lineage, last heard: what each established, and its workspace (read-only, experiments/<e>/). So the agents that
   explore after an experiment ends start from its result, wherever they are in the tree.

It ends when an experiment proves a definite answer (the verifier; or a new result, the manager), at Stop, at the budget (everything: agents, CFVS, judges, swarms), or
when no member has an option left.

Explore only (`experiments` "list", 2026-11-23; archive_explore.py): the exploration alone. An answer that would start
an experiment is listed as one (status "queued", in order: the queue a swarm would be started from) and no swarm
runs, so no result ever comes back: no news, no options asked with a result known, and the tree never waits. The
judge compares each answer with the listed ones, as it does with running experiments. `max_rollouts` ends it after
that many rollouts. Each run is kept in runs/archive/<time>-p<problem>/: settings.json, prompts.json,
state.json (every agent, without its conversation, and every experiment), events.jsonl, calls.jsonl (judge, report,
manager, halves, contract, definite and verify calls), contract.json, nodes/<id>/ (conversation.json, node.json,
scratch/) and <e>/ (a swarm's folder, as swarm_play keeps one, and verify/: the verifier's conversation.json and box/,
its folder with the record rendered).
"""

import copy
import json
import random
import shutil
import threading
import time
import traceback
from dataclasses import replace
from functools import partial
from pathlib import Path

import benchmark
import evs
import swarm_play
import verifier
from evs import NO_ANSWER_STEP
from llm import cost, usage_dict
from replies import parse
from scratchpad import Scratchpad
from streamed import CUT_OFF, NO_CALLS, longer_runs, respond
from toolkit import Toolbox

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "archive"
# The problems the page offers: the nine and the October list (an archive needs only a problem's statement; the
# answer a swarm is told and its halves are the archive's own).
PROBLEMS = swarm_play.PROBLEMS + benchmark.OCTOBER
DEFAULTS = {
    "budget": 100.0,  # dollars, the whole archive
    "exp_budget": 18.0,  # dollars, one experiment's swarm (the right p12 proof cost $5.80, p41's $11.04)
    "agents": 4,  # a swarm's
    "workers": 2,  # rollouts at once
    "max_experiments": 2,  # swarms at once
    "wait_rollouts": 6,  # rollouts that may start after an experiment starts, while one runs; then the tree waits
    "seed_turns": 20,  # the seed agent's most turns (a free agent's 20)
    "step_turns": 5,  # a rollout's most turns
    "n": 3,  # counterfactuals
    "k": 3,  # approaches given each
    "run_minutes": 10,  # an archive agent's longest scratchpad run
    "seed": 0,  # draws parents and options
    "stop_rule": "verify",  # verify (the contract gate + the verifier, verifier.py) or manager (MANAGER, before 2026-11-06)
    "gate": "definite",  # an experiment only for an answer the contract's gate passes; "claim": any new claim (before 2026-11-20)
    "experiments": "run",  # "list": explore only: an answer that would start an experiment is only listed, no swarm runs
    "max_rollouts": 0,  # the archive ends after this many rollouts (0: no limit)
}
MIN_EXP_BUDGET = 2.0  # no experiment starts with less than this left
OPTION_TOKENS = evs.MAX_TOKENS
SIDE_TOKENS = 16000  # BELIEF
CALL_TOKENS = 32000  # JUDGE, REPORT, MANAGER, HALVES_ASK
CHANNEL_CHARS = 240_000  # of a swarm's channel REPORT reads (the end of it)
FINAL_CHARS = 12_000  # of each swarm agent's last reply
STEP_CHARS = 16_000  # of a rollout's text the judge reads

# The archive's agents: the alone arm's system prompt (runner.system_prompt) without a turn limit or submit_answer,
# with the run's limits.
SYSTEM = r"""You are given the task of solving a math problem.

## How you work
You work in turns. In each turn you can call several tools; they run in the order you call them, and you see their results at the start of your next turn. You stop by ending a turn without calling a tool.

## Execution environment
You have one Python scratchpad file, scratchpad.py, that persists across turns: you can read, write, edit and run it. Each run is a fresh Python process, and may take up to {run_time} and use {memory} of memory; it may use multiprocessing with up to {workers} worker processes.
The Python environment includes NumPy, SciPy, SymPy, NetworkX, pandas, scikit-learn, gmpy2, Z3, mpmath and SageMath. Sage is imported in the same interpreter (`from sage.all import *`), and GAP and PARI work through it; Sage's Singular-based multivariate ideal methods (such as groebner_basis) crash here, so use SymPy's groebner for those.
There is no public internet access or web search. Do not try to access websites, remote APIs, or install packages. A run cannot start other programs, except more Python processes for multiprocessing.
The main challenge is mathematical reasoning, therefore the tools might not even be necessary.
Use them only if you think they will help you solve the problem.

## Scoring
You are scored on whether or not you get the final answer correct. When you have it, state it in \boxed{...}."""

OPTIONS_ASK = evs.TEMPLATE.replace(" (turn {turn} of {max_turns})", "")  # evs.md, with no turn count
assert OPTIONS_ASK != evs.TEMPLATE
TAKE = evs.VERIFIED  # the counterfactual as a verified result, then the approach
RELABEL = evs.RELABEL  # what it becomes once the agent is a parent

BELIEF = """A side question, outside your turns: if you had to submit your final answer to the problem now, what would it be? Call no tools. Reply with one JSON object, in a ```json block, and nothing else: {"answer": "<your final answer alone, as you would submit it: no explanation or reasons>", "confidence": <your probability, from 0 to 1, that it is correct>}."""

EXPERIMENT = """Your answer, {answer}, was handed to a team of {n} agents. They were told that it is the answer and asked to prove it completely, as a team, with a Slack channel and a shared workspace. Their run ended ({reason}) after ${cost:.2f}.

What they established:

{report}

Their workspace is in experiments/{e}/, next to your scratchpad: your runs can read it, not write it."""

NEWS = """Meanwhile, other solvers on this problem proposed answers, and each answer was handed to a team of agents that was told it is the answer and asked to prove it completely, as a team, with a Slack channel and a shared workspace. What came of them:

{items}

Each team's workspace is in experiments/<its id>/, next to your scratchpad: your runs can read it, not write it."""
NEWS_ITEM = """{e}: told that the answer is {answer}. Their run ended ({reason}) after ${cost:.2f}. What they established:

{report}"""

HALVES_ASK = """Below is a math problem and an answer to it. A team will be told the answer and asked to prove it. Write the sentence that tells them what proving it takes: the claims that together show this is the answer and that no other is, each stated in the problem's own terms, without any method. Use as many claims as the answer needs, and don't add one that would hold of any answer. These examples are from other problems, each of which happens to need two:

{examples}

<problem>
{problem}
</problem>

<answer>
{answer}
</answer>

Reply with the sentence only."""
HALVES_FROM = [43, 25, 37, 30]  # the problems whose halves (swarm_play.HALVES) are the examples, but the archive's own

JUDGE = """You oversee a search for the answer to the math problem below. Solvers explore it, and when one proposes an answer that claims something, the answer is handed to a team that is told it and asked to prove it. The answers handed to teams so far, with what their teams established:

{answers}

A solver has just taken a step. It was told: {told}

What it wrote in the step (its last part):

<step>
{step}
</step>

Asked what it would submit now, it answered: {answer} (its confidence: {confidence}).

Decide two things. First, whether its answer makes a claim about the problem's answer that a team could set out to prove: a value, an object, a formula, yes or no, bounds or a range, a set of possibilities, or "not determined by what is known" together with what is known (such as bounds). An answer that claims nothing is not one: "I don't have an answer", "unknown" or "it can't be determined" with nothing more, a refusal. Judge the answer as it stands, as it would be submitted: what the step says around it doesn't make it a claim, since the team is told the answer alone.

Second, whether it is a different claim from every answer above. Answers that make different claims are different even when they are close: a value and a range or set containing it, a value and "unknown", two different ranges, a general formula and a special case of it. Mathematically equal expressions, or the same claim worded differently, are the same answer.

<problem>
{problem}
</problem>

Reply with one JSON object, in a ```json block, and nothing else: {{"claim": true or false, "same_as": "<the id of the answer above that it is the same as, or null>", "answer": "<its final answer alone, as it would be submitted: no explanation or reasons>", "reason": "<briefly, why>"}}."""

REPORT = """Below is a math problem, and the record of a team of {n} agents who were told that its answer is {answer} and asked to prove it, with Python that checks every step: their Slack channel (#proof), then each agent's last reply. Their run ended: {reason}.

Write what they established, for a solver who will work on the problem next and has seen none of it: what is proved and how (the key ideas, constructions and computations, and where in their workspace the code and results are), what they could not prove and why, and whether anything they found contradicts the answer they were told. Be specific and complete, in up to about 1,200 words. Then, on a last line of its own, one of:
STATUS: PROVED (the whole proof of the answer is complete)
STATUS: PARTIAL (part of it is proved)
STATUS: CONTRADICTED (they found that the answer is false)
STATUS: NONE

<problem>
{problem}
</problem>

<channel>
{channel}
</channel>

{finals}"""

MANAGER = """You are the manager of a search for the answer to the math problem below, with its proof. Each answer that comes up is handed to a team that is told it and asked to prove it. The earlier experiments:

{earlier}

The experiment that has just ended: its team was told that the answer is {answer}. Its run ended ({reason}). What it established:

<report>
{report}
</report>

The end of its channel:

<channel>
{channel}
</channel>

Decide whether this experiment gives a new result beyond what has been known: a complete proof (no step missing, conceded or left conditional) of a definite answer to the problem's question, that goes beyond what was known before, in the literature as you know it and in the earlier experiments. Bounds that were already known, a range or "unknown" that leaves the question open, a conditional proof, or a proof with a gap is not a new result.

<problem>
{problem}
</problem>

Reply with one JSON object, in a ```json block, and nothing else: {{"new": true or false, "reason": "<briefly, why>"}}."""

STATUSES = ("PROVED", "PARTIAL", "CONTRADICTED", "NONE")
SIDE_SYSTEM = "You are a careful research mathematician."  # the judge's, the report's, the manager's and the halves' calls


def bare(answer):
    """An answer without its \\boxed{...} or math delimiters: the claim as a swarm is told it."""
    a = answer.strip()
    for o, c in (("\\(", "\\)"), ("\\[", "\\]"), ("$$", "$$"), ("$", "$")):
        if a.startswith(o) and a.endswith(c) and len(a) > len(o) + len(c):
            a = a[len(o):-len(c)].strip()
    if a.startswith("\\boxed{") and a.endswith("}"):
        a = a[len("\\boxed{"):-1].strip()
    if a.startswith("\\text{") and a.endswith("}") and a.count("{") == 1:
        a = a[len("\\text{"):-1].strip()
    return a or answer.strip()


def text_of(content):
    return content if isinstance(content, str) else "".join(b.get("text", "") for b in content if isinstance(b, dict))


def reply_text(msg):
    return "".join(b.text for b in msg.content if b.type == "text")


class ReadOnly:
    """A sandbox whose runs may read some folders too (Sandbox.run `read_only`): the workspaces of the experiments in
    an agent's lineage."""

    def __init__(self, sandbox, folders):
        self.sandbox, self.folders = sandbox, list(folders)

    def __getattr__(self, name):
        return getattr(self.sandbox, name)

    def run(self, folder, filename, timeout):
        return self.sandbox.run(folder, filename, timeout, read_only=self.folders)


class Node:
    """An agent of the archive: its conversation (`messages`; its own step begins at `step_from`), its scratchpad
    folder, the option it was rolled out from, its answer and the judge's verdict, its experiment, its options."""

    def __init__(self, archive, nid, parent, option, depth):
        self.archive, self.id, self.parent, self.option, self.depth = archive, nid, parent, option, depth
        self.folder = archive.folder / "nodes" / nid
        self.messages, self.step_from, self.take_at = [], 0, None
        self.seen = None
        self.cost, self.responses = 0.0, 0
        self.status = "running"  # running | judging | experiment | options | member | stopped | failed
        self.belief = self.judge = self.experiment = None
        self.options = None
        self.known = []  # the experiments it has been told of (its own, or NEWS), in order
        self.created = time.time()

    def summary(self):
        return {"id": self.id, "parent": self.parent, "depth": self.depth, "option": self.option,
                "status": self.status, "belief": self.belief, "judge": self.judge, "experiment": self.experiment,
                "options": self.options, "cost": round(self.cost, 4), "responses": self.responses,
                "step_from": self.step_from, "known": self.known, "created": self.created}  # fmt: skip

    def carried(self):
        """Its conversation as a child goes on from it: the counterfactual it was told as verified relabelled as an
        assumption it worked under (evs.RELABEL), as vs_branch.carry does for a copy chosen."""
        messages = list(self.messages)
        if self.take_at is not None:
            o = self.option
            messages[self.take_at] = {"role": "system", "content": RELABEL.format(counterfactual=o["counterfactual"],
                                                                                 approach=o["approach"])}  # fmt: skip
        return messages

    def save(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        (self.folder / "conversation.json").write_text(json.dumps({"agent": self.id, "messages": self.messages},
                                                                  indent=1))  # fmt: skip
        (self.folder / "node.json").write_text(json.dumps({**self.summary(), "seen": self.seen,
                                                           "take_at": self.take_at}, indent=1))  # fmt: skip


class Archive:
    """One prover-archive run, in threads of its own; its events kept for any page that (re)connects (serve.py's
    stream reads `events` and `cond`). `llm`: the agents' model (its system prompt and tools are set here);
    `swarm_llm`: the swarms'; `make_sandbox(stop)` makes a sandbox (the swarms' kind); `register(swarm)` lets the
    server stream a swarm to the swarm page."""

    def __init__(self, llm, swarm_llm, make_sandbox, p, settings, register=lambda swarm: None):
        self.s = {**DEFAULTS, **{k: v for k, v in (settings or {}).items() if k in DEFAULTS}}
        self.p, self.problem = p, swarm_play.problem_text(p).strip()
        stamp = time.strftime("%Y%m%d-%H%M%S")
        while (OUT / f"{stamp}-p{p}").exists():
            stamp += "b"
        self.folder = OUT / f"{stamp}-p{p}"
        self.id = self.folder.name
        self.folder.mkdir(parents=True)
        self.events, self.cond, self.stop = [], threading.Condition(), threading.Event()
        self.lock, self.judging = threading.RLock(), threading.Lock()
        self.rng = random.Random(f"{self.s['seed']}:{self.id}")
        self.nodes, self.members, self.exps, self.queue = {}, [], {}, []
        self.swarms = {}  # experiment id -> its Swarm
        self.calls = 0.0  # the judge's, the reports', the manager's, the halves' and the verifier's calls
        self.base_llm, self.contract, self.contract_lock = llm, None, threading.Lock()  # the verifier's model; the answer contract
        self.definites = {}  # an answer (its words) -> verifier.definite's {definite, reason}, for the gate and the stop
        self.busy = 0  # workers in a rollout
        self.listing = self.s["experiments"] == "list"  # explore only: experiments are listed, never run
        self.judged, self.capped, self.started = 0, False, time.time()  # answers judged so far; max_rollouts reached
        self.allowance = 0  # rollouts that may still start while an experiment runs (wait_rollouts)
        self.end_reason, self.ended = None, False
        self.make_sandbox, self.register, self.swarm_llm = make_sandbox, register, swarm_llm
        self.exp_slots = threading.BoundedSemaphore(int(self.s["max_experiments"]))
        self.sandbox = make_sandbox(self.stop)
        box = self.sandbox
        self.run_seconds = int(float(self.s["run_minutes"]) * 60)
        self.limits = {"run_time": swarm_play.duration(self.run_seconds), "memory": swarm_play.size(box.memory_mb * 2**20),
                       "workers": str(max(1, box.processes - 2))}  # fmt: skip
        system = SYSTEM
        for k, v in self.limits.items():
            system = system.replace("{" + k + "}", v)
        self.llm = replace(llm, system=system, tools=longer_runs(Scratchpad.tools, self.run_seconds))
        self.side = lambda prompt, tokens=CALL_TOKENS: replace(llm, system=prompt, tools=[], max_tokens=tokens)
        (self.folder / "settings.json").write_text(json.dumps({"problem": p, **self.s, "model": llm.model,
                                                              "effort": llm.effort, "limits": self.limits}, indent=1))  # fmt: skip
        (self.folder / "prompts.json").write_text(json.dumps(prompts(), indent=1))
        self.save_state()
        threading.Thread(target=self.main, daemon=True).start()

    # ---- bookkeeping ---------------------------------------------------------------

    @property
    def spent(self):
        with self.lock:
            return (sum(n.cost for n in list(self.nodes.values())) + self.calls
                    + sum(w.cost for w in list(self.swarms.values())))  # fmt: skip

    def left(self):
        return float(self.s["budget"]) - self.spent

    def emit(self, a=None, **event):
        if a is not None:
            event["a"] = a
        with self.cond:
            self.events.append(event)
            self.cond.notify_all()
            if event["k"] not in ("think", "say", "args"):
                with open(self.folder / "events.jsonl", "a") as f:
                    f.write(json.dumps(event) + "\n")

    def changed(self, node=None, exp=None):
        """A node's or an experiment's new state, to the page and to state.json."""
        with self.lock:
            if node is not None:
                node.save()
                self.emit(k="node", node=node.summary())
            if exp is not None:
                self.emit(k="exp", exp=exp)
            self.save_state()

    def save_state(self):
        with self.lock:
            state = {"id": self.id, "problem": self.p, "settings": self.s, "spent": round(self.spent, 4),
                     "nodes": [n.summary() for n in self.nodes.values()], "members": self.members,
                     "experiments": list(self.exps.values()), "reason": self.end_reason, "ended": self.ended}  # fmt: skip
            tmp = self.folder / "state.json.tmp"
            tmp.write_text(json.dumps(state, indent=1))
            tmp.replace(self.folder / "state.json")

    def end(self, reason):
        with self.lock:
            if self.end_reason is None:
                self.end_reason = reason
        self.stop.set()
        for w in list(self.swarms.values()):
            if not w.ended:
                w.end(f"the archive ended: {reason}")

    def call(self, what, user, tokens=CALL_TOKENS, **about):
        """One call of the model with no tools (SIDE_SYSTEM, then `user`): its text. Kept in calls.jsonl, with `about`
        (the node judged, the experiment read); its cost counts."""
        prompt = SIDE_SYSTEM
        llm = self.side(prompt, tokens)
        reply = llm.create([{"role": "user", "content": user}])
        spent = cost(llm.model, usage_dict(reply.message.usage))
        with self.lock:
            self.calls += spent
        text = reply_text(reply.message)
        with open(self.folder / "calls.jsonl", "a") as f:
            f.write(json.dumps({"what": what, **about, "time": time.time(), "cost": round(spent, 5), "prompt": prompt,
                                "user": user, "text": text, "request_id": reply.request_id}) + "\n")  # fmt: skip
        return text

    # ---- the run --------------------------------------------------------------------

    def main(self):
        reason = None
        try:
            self.emit(k="start", id=self.id, folder=str(self.folder.relative_to(ROOT)), problem=self.p, settings=self.s)
            if why := self.sandbox.ready():
                raise RuntimeError(f"the sandbox isn't ready: {why}")
            threading.Thread(target=self.watch, daemon=True).start()
            seed = self.seed()
            if seed is not None and not self.stop.is_set():
                self.after(seed)
            workers = [threading.Thread(target=self.worker, daemon=True) for _ in range(int(self.s["workers"]))]
            for t in workers:
                t.start()
            for t in workers:
                t.join()
            while not self.listing and (any(not w.ended for w in self.swarms.values())
                                        or any(e["status"] in ("queued", "running", "reading", "verifying")
                                               for e in self.exps.values())):  # fmt: skip
                time.sleep(2)
        except Exception as e:
            traceback.print_exc()
            reason = f"error: {e!r}"
        if reason:
            self.end(reason)
        self.ended = True
        self.stop.set()
        for n in self.nodes.values():
            if n.status not in ("member", "failed"):
                n.status = "stopped"
                n.save()
        self.save_state()
        self.sandbox.close()
        self.emit(k="end", reason=self.end_reason or "ended", cost=round(self.spent, 4))

    def watch(self):
        """The budget, and the page's running total."""
        last = None
        while not self.ended:
            spent = round(self.spent, 2)
            if spent != last:
                self.emit(k="spent", total=spent)
                self.save_state()
                last = spent
            if spent >= float(self.s["budget"]) and not self.stop.is_set():
                self.end(f"budget (${spent:.2f})")
            for e in self.exps.values():  # a running swarm's cost, for the page
                w = self.swarms.get(e["id"])
                if w is not None and e["status"] == "running" and round(w.cost, 2) != e.get("cost"):
                    e["cost"] = round(w.cost, 2)
                    self.emit(k="exp", exp=e)
            time.sleep(3)

    def worker(self):
        while not self.stop.is_set():
            picked = self.pick()
            if picked is None:
                with self.lock:
                    idle = self.busy == 0 and (self.listing or not any(e["status"] != "ended" for e in self.exps.values()))
                    waiting = any(n.status not in ("member", "failed", "stopped") for n in self.nodes.values())
                if idle and not waiting:
                    return self.end(f"{self.s['max_rollouts']} rollouts" if self.capped else "no options left")
                self.stop.wait(3)
                continue
            parent, option, child = picked
            try:
                self.rollout(parent, option, child)
                if self.stop.is_set():
                    break
                self.after(child)
            except InterruptedError:
                break
            except Exception as e:
                traceback.print_exc()
                child.status = "failed"
                self.emit(child.id, k="note", text=f"error: {e!r}")
                self.changed(node=child)
            finally:
                with self.lock:
                    self.busy -= 1

    def pick(self):
        """(parent, option, child) for the next rollout: the page's pick if one is queued, or else a member drawn
        uniformly among those with an option left and one of its options left, drawn uniformly. The option is marked
        taken (its child's id). While an experiment is queued or runs, only `allowance` drawn rollouts start (set to
        wait_rollouts when one starts); the page's picks always do."""
        with self.lock:
            if self.stop.is_set() or self.left() <= 0:
                return None
            if 0 < int(self.s["max_rollouts"]) <= len(self.nodes) - 1:  # every agent but the seed is a rollout
                self.capped = True
                return None
            parent = option = None
            while self.queue and option is None:
                nid, branch = self.queue.pop(0)
                node = self.nodes.get(nid)
                option = next((o for o in (node.options or []) if o["branch"] == branch and o["child"] is None), None)
                parent = node
            if option is None:
                proving = not self.listing and any(e["status"] in ("queued", "running", "reading", "verifying")
                                                   for e in self.exps.values())  # fmt: skip
                if proving and self.allowance <= 0:  # the tree waits for an experiment to end
                    return None
                open_ = [self.nodes[m] for m in self.members if any(o["child"] is None for o in self.nodes[m].options)]
                if not open_:
                    return None
                parent = self.rng.choice(open_)
                option = self.rng.choice([o for o in parent.options if o["child"] is None])
                if proving:
                    self.allowance -= 1
            child = Node(self, f"n{len(self.nodes)}", parent.id, {k: option.get(k) for k in
                                                                 ("branch", "counterfactual", "approach", "p")},
                         parent.depth + 1)  # fmt: skip
            option["child"] = child.id
            self.nodes[child.id] = child
            self.busy += 1
        self.changed(node=parent)
        return parent, option, child

    def enqueue(self, nid, branch):
        """The page's pick: this member's option is rolled out next."""
        with self.lock:
            node = self.nodes.get(nid)
            if node is None or nid not in self.members or not any(o["branch"] == branch and o["child"] is None
                                                                  for o in node.options or []):  # fmt: skip
                raise ValueError("no such option left")
            self.queue.append((nid, branch))

    # ---- an agent's turns ------------------------------------------------------------

    def toolbox(self, node):
        """Its scratchpad (its folder's scratch/), its runs reading the workspaces of the experiments it knows."""
        reads = [self.folder / e / "workspace" for e in node.known]
        pad = Scratchpad(node.folder / "scratch", ReadOnly(self.sandbox, reads), max_seconds=self.run_seconds)
        pad._seen = node.seen if node.seen is not None else pad._seen
        box = Toolbox(pad)
        assert [t["name"] for t in box.tools] == [t["name"] for t in self.llm.tools]
        return pad, box

    def turns(self, node, most):
        """Up to `most` turns of `node`, streamed to the page; ending at a turn that calls no tool."""
        pad, box = self.toolbox(node)
        emit, refusals = partial(self.emit, node.id), 0
        taken = 0
        while taken < most and not self.stop.is_set():
            node.responses += 1
            n = node.responses
            self.emit(node.id, k="response", n=n)
            reply = respond(self.llm, node.messages, n, emit, self.stop)  # InterruptedError at Stop
            node.cost += cost(self.llm.model, usage_dict(reply.usage))
            if reply.stop_reason == "refusal":
                refusals += 1
                self.emit(node.id, k="note", text=f"refused ({refusals})")
                if refusals > 2:
                    raise RuntimeError("refused three times")
                continue
            taken += 1
            node.messages.append({"role": "assistant", "content": [b.to_dict() for b in reply.content]})
            results, calls = [], []
            for block in (b for b in reply.content if b.type == "tool_use"):
                result = box.handle(block) if reply.stop_reason != "max_tokens" else {
                    "type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": "Not run: your response was cut off at the output limit."}  # fmt: skip
                results.append(result)
                calls.append({"name": block.name, "output": result["content"]})
                self.emit(node.id, k="result", call_id=block.id, out=result["content"], error=result["is_error"])
            node.messages.append({"role": "user", "content": results or (CUT_OFF if reply.stop_reason == "max_tokens"
                                                                         else NO_CALLS)})  # fmt: skip
            node.seen = pad._seen
            self.changed(node=node)
            if not calls and reply.stop_reason != "max_tokens":
                break

    def seed(self):
        node = Node(self, "n0", None, None, 0)
        self.nodes["n0"] = node
        node.messages = [{"role": "user", "content": self.problem}]
        (node.folder / "scratch").mkdir(parents=True, exist_ok=True)
        self.changed(node=node)
        self.emit("n0", k="told", text=self.problem, first=True)
        try:
            self.turns(node, int(self.s["seed_turns"]))
        except InterruptedError:
            return None
        if self.stop.is_set():
            return None
        self.believe(node)
        return node

    def rollout(self, parent, option, child):
        """`child`: `parent`'s conversation (carried) and a copy of its scratchpad, told `option` (none for the
        continuation), then its step."""
        child.messages = copy.deepcopy(parent.carried())
        shutil.copytree(parent.folder / "scratch", child.folder / "scratch", symlinks=True)
        child.seen = parent.seen
        child.known = list(parent.known)
        self.changed(node=child)
        self.tell_news(child)
        child.step_from = len(child.messages)
        if option["counterfactual"] is not None:
            text = TAKE.format(counterfactual=option["counterfactual"], approach=option["approach"],
                               no_answer=NO_ANSWER_STEP)  # fmt: skip
            child.take_at = len(child.messages)
            child.messages.append({"role": "system", "content": text})
            self.changed(node=child)
            self.emit(child.id, k="told", text=text)
        else:
            self.changed(node=child)
        self.turns(child, int(self.s["step_turns"]))
        if self.stop.is_set():
            return
        self.believe(child)

    def tell_news(self, node):
        """NEWS: every experiment that has been read (its report written) and `node` hasn't been told of, as a user
        message, with its workspace linked next to the scratchpad."""
        with self.lock:
            news = [e for e in self.exps.values() if e.get("report") and e["status"] == "ended"
                    and e["id"] not in node.known]  # fmt: skip
        if not news:
            return
        for e in news:
            self.link(node, e["id"])
            node.known.append(e["id"])
        text = NEWS.format(items="\n\n".join(NEWS_ITEM.format(e=e["id"], answer=e["answer"], reason=e["reason"],
                                                                 cost=e["cost"] or 0.0, report=e["report"]["text"])
                                                for e in news))  # fmt: skip
        node.messages.append({"role": "user", "content": text})
        self.emit(node.id, k="told", text=text)

    def link(self, node, eid):
        link = node.folder / "scratch" / "experiments"
        link.mkdir(exist_ok=True)
        if not (link / eid).exists():
            (link / eid).symlink_to((self.folder / eid / "workspace").resolve(), target_is_directory=True)

    def believe(self, node):
        """BELIEF, asked of a copy of its conversation: {answer, confidence}. A reply with no answer is asked once
        more."""
        for _ in range(2):
            reply = self.llm.fork(node.messages, BELIEF, SIDE_TOKENS).message
            node.cost += cost(self.llm.model, usage_dict(reply.usage))
            got = parse(reply_text(reply)) or {}
            if str(got.get("answer") or "").strip():
                node.belief = {"answer": str(got["answer"]).strip(), "confidence": got.get("confidence")}
                break
        else:
            node.belief = {"answer": None, "confidence": None}
        self.emit(node.id, k="note", text=f"would submit: {node.belief['answer']} (confidence {node.belief['confidence']})")
        node.status = "judging"
        self.changed(node=node)

    # ---- after a rollout: the judge, an experiment or not, then options -------------------------

    def after(self, child):
        with self.judging:  # one at a time, so that two agents with one new answer don't both start an experiment
            self.judge(child)
            start = (child.judge["experiment"] and (self.listing or self.left() >= MIN_EXP_BUDGET)
                     and not self.stop.is_set())  # fmt: skip
            if child.judge["experiment"] and not start:
                child.judge["skipped"] = "too little budget left"
            if start:
                exp = self.new_experiment(child)
        if start and not self.listing:  # proved alongside; its options now, so that the tree can explore from it meanwhile
            threading.Thread(target=self.experiment, args=(child, exp), daemon=True).start()
        self.options(child)
        self.admit(child)

    def answers_text(self):
        if not self.exps:
            return "(none yet)"
        return "\n\n".join(f"{e['id']}: {e['answer']} ({e['status']}"
                           + (f", {e['report']['status'].lower()}" if e.get("report") else "") + ")"
                           + (f"\n{e['report']['text'][:3000]}" if e.get("report") else "")
                           for e in self.exps.values())  # fmt: skip

    def judge(self, node):
        self.judged += 1  # the seed's answer is the first judged
        if node.belief["answer"] is None:
            node.judge = {"same_as": None, "answer": None, "experiment": False, "reason": "no answer", "n": self.judged}
            return self.changed(node=node)
        steps = node.messages[node.step_from:]
        told = (text_of(steps[0]["content"]) if node.take_at is not None else
                "nothing: it went on with its own work." if node.parent else
                "nothing but the problem: this was its first step, from a fresh start.")  # fmt: skip
        said = "\n\n".join(b["text"] for m in steps if m["role"] == "assistant" for b in m["content"]
                           if b.get("type") == "text" and b.get("text"))  # fmt: skip
        said = said[-STEP_CHARS:] or "(no text)"
        prompt = JUDGE.format(answers=self.answers_text(), told=told, step=said, answer=node.belief["answer"],
                              confidence=node.belief["confidence"], problem=self.problem)  # fmt: skip
        got = parse(self.call("judge", prompt, node=node.id)) or {}
        same = got.get("same_as")
        same = same if same in self.exps else None
        claim = got.get("claim") is True
        node.judge = {"claim": claim, "same_as": same, "answer": bare(str(got.get("answer") or node.belief["answer"])),
                      "reason": got.get("reason"), "experiment": claim and same is None, "n": self.judged}  # fmt: skip
        if node.judge["experiment"] and self.s["gate"] == "definite":  # a swarm only for an answer that could end it
            d = self.definite(node.judge["answer"], node=node.id)
            node.judge.update(definite=d["definite"], gate=d["reason"], procedure=d.get("procedure") is True,
                              experiment=d["definite"])  # fmt: skip
        verdict = ("same as " + same if same else "no claim" if not claim else
                   "a new answer, a procedure for finding the result and not the result, so no experiment"
                   if node.judge.get("procedure") else
                   "a new answer, not definite, so no experiment" if node.judge.get("definite") is False else "a new answer")
        self.emit(node.id, k="note", text=f"judge: {verdict}")
        self.changed(node=node)

    def new_experiment(self, node):
        with self.lock:
            eid = f"e{len(self.exps) + 1}"
            exp = {"id": eid, "node": node.id, "answer": node.judge["answer"], "status": "queued", "cost": 0.0,
                   "queued_at": time.time(),
                   # when it came up: the answers judged by then (this one counted), the dollars, the seconds
                   "at": {"judged": self.judged, "spent": round(self.spent, 4), "seconds": round(time.time() - self.started)},
                   "key": f"archive/{self.id}/{eid}", "swarm": None, "halves": None, "report": None,
                   "manager": None, "reason": None, "budget": None}  # fmt: skip
            self.exps[eid] = exp
            self.allowance = int(self.s["wait_rollouts"])
            node.experiment = eid
            node.status = "experiment"
        self.changed(node=node, exp=exp)
        return exp

    def experiment(self, node, exp=None):
        """`node`'s answer handed to a prover swarm, then read (REPORT, MANAGER) and told to `node`; then more
        options for it, asked with the result known (their branches prefixed with the experiment's id)."""
        exp = exp or self.new_experiment(node)
        try:
            with self.exp_slots:
                if self.stop.is_set():
                    exp["status"] = "ended"
                    exp["reason"] = "not started: the archive ended"
                    return self.changed(exp=exp)
                self.prove(node, exp)
        except Exception as e:
            traceback.print_exc()
            exp.update(status="ended", reason=exp.get("reason") or f"error: {e!r}")
            self.changed(exp=exp)
        if self.stop.is_set():
            return
        while node.options is None and not self.stop.is_set():  # its first options (after) not in yet
            time.sleep(2)
        if exp.get("report") is None or self.stop.is_set():
            return
        try:
            self.options(node, prefix=exp["id"])
        except InterruptedError:
            return
        self.admit(node)

    def prove(self, node, exp):
        answer = exp["answer"]
        examples = "\n\n".join(swarm_play.HALVES[q] for q in HALVES_FROM if q != self.p)
        exp["halves"] = self.call("halves", HALVES_ASK.format(examples=examples, problem=self.problem,
                                                                  answer=answer), exp=exp["id"]).strip()  # fmt: skip
        prompt = swarm_play.PROMPT.replace("{problem}", self.problem).replace("{answer}", answer).replace(
            "{halves}", exp["halves"])
        exp["budget"] = round(min(float(self.s["exp_budget"]), max(0.0, self.left())), 2)
        swarm = swarm_play.Swarm(self.swarm_llm, self.make_sandbox, self.p, swarm_play.SYSTEM, prompt, [],
                                 int(self.s["agents"]), exp["budget"], answer=answer, folder=self.folder / exp["id"],
                                 run_id=f"{self.id}-{exp['id']}", settle=True, keep=[exp["halves"]])  # fmt: skip
        self.swarms[exp["id"]] = swarm
        self.register(swarm)
        exp.update(status="running", swarm=swarm.id, started=time.time())
        self.changed(exp=exp)
        while not swarm.ended:
            time.sleep(2)
        summary = swarm.folder / "summary.json"  # (a swarm that ends idle keeps its reason there only)
        reason = swarm.end_reason or (json.loads(summary.read_text()).get("reason") if summary.exists() else None)
        exp.update(status="reading", reason=reason or "ended", cost=round(swarm.cost, 4), ended_at=time.time())
        self.changed(exp=exp)
        if self.stop.is_set():  # the archive ended (Stop, the budget, another's new result): not read
            exp["status"] = "ended"
            return self.changed(exp=exp)
        rows = swarm.hub.dump()
        channel = "\n\n".join(f"#{r['id']} {r['sender']}" + (f" (in thread #{r['thread']})" if r.get("thread") else "")
                              + f": {r['body']}" for r in rows)  # fmt: skip
        channel = channel[-CHANNEL_CHARS:] or "(nothing posted)"
        finals = []
        for a in swarm.names:
            path = swarm.folder / "agents" / a / "conversation.json"
            if path.exists():
                msgs = json.loads(path.read_text())["messages"]
                last = next((text_of([b for b in m["content"] if b.get("type") == "text"]) for m in reversed(msgs)
                             if m["role"] == "assistant" and any(b.get("type") == "text" and b.get("text")
                                                                 for b in m["content"])), "")  # fmt: skip
                finals.append(f"<{a}_last_reply>\n{last[-FINAL_CHARS:] or '(none)'}\n</{a}_last_reply>")
        text = self.call("report", REPORT.format(n=len(swarm.names), answer=answer, reason=exp["reason"],
                                                     problem=self.problem, channel=channel, finals="\n\n".join(finals)),
                         exp=exp["id"])  # fmt: skip
        status = next((s for line in reversed(text.strip().splitlines()) for s in STATUSES
                       if line.strip().upper().startswith("STATUS:") and s in line.upper()), "NONE")  # fmt: skip
        body = "\n".join(l for l in text.strip().splitlines() if not l.strip().upper().startswith("STATUS:")).strip()
        exp["report"] = {"status": status, "text": body}
        if self.s["stop_rule"] == "manager":
            earlier = "\n\n".join(f"{e['id']}: told {e['answer']}; {e['report']['status'].lower()}\n{e['report']['text'][:4000]}"
                                  for e in self.exps.values() if e["id"] != exp["id"] and e.get("report")) or "(none)"  # fmt: skip
            got = parse(self.call("manager", MANAGER.format(earlier=earlier, answer=answer, reason=exp["reason"],
                                                                report=body, channel=channel[-40_000:],
                                                                problem=self.problem), exp=exp["id"])) or {}  # fmt: skip
            exp["manager"] = {"new": got.get("new") is True, "reason": got.get("reason")}
        else:
            exp["status"] = "verifying"
            self.changed(exp=exp)
            try:
                exp["verify"] = self.verify(node, exp, swarm)
            except Exception as e:  # the agent is still told the report; the archive goes on
                traceback.print_exc()
                exp["verify"] = {"stop": False, "summary": f"the verifier failed: {e!r}"}
            exp["manager"] = {"new": exp["verify"]["stop"], "reason": exp["verify"]["summary"], "by": "verify"}
        exp.update(status="ended", read_at=time.time())  # agents rolled out from now on are told of it (NEWS)
        self.changed(exp=exp)
        told = EXPERIMENT.format(answer=answer, n=len(swarm.names), reason=exp["reason"], cost=swarm.cost,
                                 report=body, e=exp["id"])  # fmt: skip
        self.link(node, exp["id"])
        node.known.append(exp["id"])
        node.messages.append({"role": "user", "content": told})
        self.emit(node.id, k="told", text=told)
        self.changed(node=node)
        if exp["manager"]["new"]:
            self.end(f"proved: {exp['id']} ({answer})" if exp["manager"].get("by") == "verify"
                     else f"a new result: {exp['id']} ({answer})")

    def answer_contract(self, **about):
        """The problem's answer contract (verifier.contract), asked once and kept in contract.json."""
        with self.contract_lock:
            if self.contract is None:
                self.contract = verifier.contract(lambda what, user: self.call(what, user, **about), self.problem)
                (self.folder / "contract.json").write_text(json.dumps(self.contract, indent=1))
        return self.contract

    def definite(self, answer, **about):
        """verifier.definite for `answer`, asked once per answer: the gate before a swarm and the stop rule's agree."""
        key = " ".join(str(answer).split())
        if key not in self.definites:
            c = self.answer_contract(**about)
            self.definites[key] = verifier.definite(lambda what, user: self.call(what, user, **about), self.problem,
                                                    c, answer)  # fmt: skip
        return self.definites[key]

    def verify(self, node, exp, swarm):
        """The stopping condition (verifier.py): the answer contract's gate, then the verifier on the swarm's whole
        record, working in <e>/verify/. {stop, definite, verdict, acknowledged, review, summary, cost, ...}."""
        d = self.definite(exp["answer"], exp=exp["id"])
        out = {"stop": False, "definite": d["definite"], "definite_reason": d["reason"],
               "procedure": d.get("procedure") is True}  # fmt: skip
        if not d["definite"]:
            what = "a procedure for finding the result, not the result" if out["procedure"] else "not a definite answer"
            self.emit(node.id, k="note", text=f"{exp['id']}: {what}, so it can't end the archive")
            return {**out, "summary": f"{what}: {d['reason']}"}
        got = verifier.verify(self.base_llm, self.sandbox, verifier.Record(swarm.folder), self.folder / exp["id"] / "verify",
                              self.problem, self.contract["form"], exp["answer"], exp["reason"], exp["halves"],
                              emit=lambda t: self.emit(node.id, k="note", text=f"{exp['id']} {t}"), stop=self.stop)  # fmt: skip
        with self.lock:
            self.calls += got["cost"]
        v = got["review"]
        with open(self.folder / "calls.jsonl", "a") as f:
            f.write(json.dumps({"what": "verify", "exp": exp["id"], "time": time.time(), "cost": round(got["cost"], 5),
                                "responses": got["responses"], "runs": got["runs"], "review": v}) + "\n")  # fmt: skip
        summary = (f"{v.get('verdict') or 'no verdict'}"
                   + (", the team acknowledged a gap" if v.get("team_acknowledged_gap") else "")
                   + f": {v.get('reason') or ''}")  # fmt: skip
        return {**out, **{k: got[k] for k in ("stop", "verdict", "acknowledged", "review", "responses", "runs")},
                "cost": round(got["cost"], 4), "summary": summary}

    def options(self, node, prefix=None):
        """CFVS of its conversation (carried), and the continuation: its options; with `prefix`, more of them, added
        to those it has, each branch `prefix/<branch>`."""
        node.status = "options"
        self.changed(node=node)
        found = []
        question = OPTIONS_ASK.format(n=int(self.s["n"]), k=int(self.s["k"]))
        for attempt in range(3):
            if self.stop.is_set():
                break
            asked = node.carried()
            reply = self.llm.fork(asked, question, OPTION_TOKENS)
            node.cost += cost(self.llm.model, usage_dict(reply.message.usage))
            text = reply_text(reply.message)
            found = evs.flatten(evs.counterfactuals(parse(text)) or [])
            with open(node.folder / "cfvs.jsonl", "a") as f:  # each CFVS call: what it was asked of and its reply
                f.write(json.dumps({"prefix": prefix, "attempt": attempt, "upto": len(asked), "time": time.time(),
                                    "question": question, "text": text, "options": len(found),
                                    "request_id": reply.request_id}) + "\n")  # fmt: skip
            if found:
                break
        name = (lambda b: f"{prefix}/{b}") if prefix else (lambda b: b)
        new = [{"branch": name(a["branch"]), "counterfactual": a["counterfactual"], "approach": a["text"],
                "p": round(a["p"], 4), "child": None} for a in found]  # fmt: skip
        new.append({"branch": name("own"), "counterfactual": None, "approach": None, "p": None, "child": None})
        with self.lock:
            node.options = (node.options or []) + new if prefix else new

    def admit(self, node):
        with self.lock:
            node.status = "member"
            if node.id not in self.members:
                self.members.append(node.id)
        self.changed(node=node)


def prompts():
    return {"system": SYSTEM, "options": OPTIONS_ASK, "take": TAKE, "relabel": RELABEL, "belief": BELIEF,
            "judge": JUDGE, "halves": HALVES_ASK, "swarm_system": swarm_play.SYSTEM, "swarm_prompt": swarm_play.PROMPT,
            "report": REPORT, "manager": MANAGER, "experiment": EXPERIMENT, "news": NEWS + "\n\n" + NEWS_ITEM,
            "contract": verifier.CONTRACT, "definite": verifier.DEFINITE, "result": verifier.RESULT,
            "verify_system": verifier.VERIFY_SYSTEM,
            "verify": verifier.VERIFY}  # fmt: skip


# ---- saved runs ---------------------------------------------------------------------------------


def run_folder(rid):
    if not rid or "/" in rid or rid.startswith("."):
        return None
    folder = OUT / rid
    return folder if (folder / "state.json").exists() else None


def saved_runs():
    out = []
    for folder in sorted(OUT.glob("*"), reverse=True):
        if (folder / "state.json").exists():
            s = json.loads((folder / "state.json").read_text())
            out.append({"id": folder.name, "problem": s.get("problem"), "spent": s.get("spent"),
                        "reason": s.get("reason"), "nodes": len(s.get("nodes", [])),
                        "experiments": len(s.get("experiments", [])), "ended": s.get("ended"),
                        "budget": (s.get("settings") or {}).get("budget")})  # fmt: skip
    return out


def replay(rid):
    """A saved run as the page's events: start, each node (its state, then its own step as a live run sent it), each
    experiment, end."""
    folder = run_folder(rid)
    if folder is None:
        return None
    s = json.loads((folder / "state.json").read_text())
    ev = [{"k": "start", "id": rid, "folder": str(folder.relative_to(ROOT)), "problem": s["problem"],
           "settings": s["settings"]}]  # fmt: skip
    for n in s["nodes"]:
        ev.append({"k": "node", "node": n})
        path = folder / "nodes" / n["id"] / "conversation.json"
        if path.exists():
            messages = json.loads(path.read_text())["messages"]
            ev += swarm_play.conversation_events(n["id"], messages[n["step_from"]:], first=n["step_from"] == 0)
            if n.get("belief"):
                ev.append({"a": n["id"], "k": "note", "text": f"would submit: {n['belief']['answer']} "
                                                             f"(confidence {n['belief']['confidence']})"})  # fmt: skip
    ev += [{"k": "exp", "exp": e} for e in s["experiments"]]
    ev.append({"k": "spent", "total": s.get("spent") or 0})
    ev.append({"k": "end", "reason": s.get("reason") or "saved", "cost": s.get("spent") or 0})
    return ev


def exp_times(folder, s):
    """Each experiment's times: `started`, `ended` (its swarm ended), `read` (its report and manager's verdict in, so
    agents rolled out from then on are told of it). Runs before 2026-11-05 kept only `started`: `read` is then the
    manager's call in calls.jsonl (matched by the answer it was told), and `ended` unknown."""
    managers = {}
    path = folder / "calls.jsonl"
    if path.exists():
        for line in path.read_text().splitlines():
            c = json.loads(line)
            if c.get("what") == "manager":
                managers.setdefault(c.get("exp"), c["time"])  # runs from 2026-11-05 name the experiment
                for e in s["experiments"]:
                    if f"its team was told that the answer is {e['answer']}. Its run ended" in c["user"]:
                        managers.setdefault(e["id"], c["time"])
    return {e["id"]: {"started": e.get("started"), "ended": e.get("ended_at"),
                      "read": e.get("read_at") or (managers.get(e["id"]) if e.get("manager") else None)}
            for e in s["experiments"]}  # fmt: skip


def message_kind(i, m):
    c = m["content"]
    if m["role"] == "system":
        return ("verified" if c.startswith(TAKE.split("{")[0]) else
                "assumption" if c.startswith(RELABEL.split("{")[0]) else "system")  # fmt: skip
    if m["role"] == "assistant":
        return "assistant"
    if isinstance(c, list):
        return "tool_result"
    if i == 0:
        return "problem"
    for kind, template in (("news", NEWS), ("experiment", EXPERIMENT)):
        if c.startswith(template.split("{")[0]):
            return kind
    return "nudge" if c in (NO_CALLS, CUT_OFF) else "user"


def cfvs_calls(folder, node, messages, s):
    """`node`'s CFVS calls: {prefix, upto (the messages it was asked after), question, replies}. From cfvs.jsonl where
    the run kept it (from 2026-11-05); before, rebuilt: the first call was asked at the end of its step (before its
    own experiment's result, EXPERIMENT, which is appended when the experiment is read), the call after an
    experiment at the end of that result. Earlier runs kept no replies, only the options parsed from them."""
    path = folder / "nodes" / node["id"] / "cfvs.jsonl"
    if path.exists():
        calls = {}
        for line in path.read_text().splitlines():
            c = json.loads(line)
            got = calls.setdefault(c["prefix"], {"prefix": c["prefix"], "upto": c["upto"], "question": c["question"],
                                                 "replies": []})  # fmt: skip
            got["replies"].append({"text": c["text"], "options": c["options"], "time": c["time"]})
            got["upto"] = c["upto"]
        return list(calls.values())
    if not node.get("options"):
        return []
    question = json.loads((folder / "prompts.json").read_text())["options"].format(n=int(s["settings"]["n"]),
                                                                                   k=int(s["settings"]["k"]))  # fmt: skip
    told = [i for i in range(node["step_from"], len(messages)) if message_kind(i, messages[i]) == "experiment"]
    calls = [{"prefix": None, "upto": told[0] if told else len(messages), "question": question, "replies": None}]
    if node.get("experiment") and told and any(o["branch"].startswith(node["experiment"] + "/") for o in node["options"]):
        calls.append({"prefix": node["experiment"], "upto": told[0] + 1, "question": question, "replies": None})
    return calls


def prompt(folder, nid, which="step"):
    """What one of `nid`'s requests was sent. `which`: "step", its first response (its conversation up to and with
    the option it was told); "cfvs", its CFVS call, or "cfvs:<e>" the one after its experiment <e> was read (its
    conversation then, its own option relabelled as an assumption as Node.carried does, and the question as a system
    message after it, as fork asks it). The system prompt; each message with the agent whose step added it, and its
    kind; the CFVS calls there are; and every experiment's times beside the agent's rollout (`created`: when it was
    drawn; its NEWS was told at once)."""
    s = json.loads((folder / "state.json").read_text())
    nodes = {n["id"]: n for n in s["nodes"]}
    path = folder / "nodes" / nid / "conversation.json"
    if nid not in nodes or not path.exists():
        return None
    node = json.loads((folder / "nodes" / nid / "node.json").read_text())
    messages = json.loads(path.read_text())["messages"]
    s_cfvs = cfvs_calls(folder, node, messages, s)
    call = None
    if which == "step":
        end = node["step_from"] + (1 if node.get("take_at") == node["step_from"] else 0)
    else:
        call = next((c for c in s_cfvs if which == ("cfvs:" + c["prefix"] if c["prefix"] else "cfvs")), None)
        if call is None:
            return None
        end = call["upto"]
        if node.get("take_at") is not None and node.get("option"):
            o = node["option"]
            messages = list(messages)
            messages[node["take_at"]] = {"role": "system", "content": RELABEL.format(counterfactual=o["counterfactual"],
                                                                                      approach=o["approach"])}  # fmt: skip
    chain, at = [], nid
    while at is not None:
        chain.insert(0, nodes[at])
        at = nodes[at]["parent"]
    out = []
    for i, m in enumerate(messages[:end]):
        kind = message_kind(i, m)
        owner = [n for n in chain if n["step_from"] <= i][-1]["id"]
        if kind == "news":  # told just before the step of the agent it was told to
            owner = next((n["id"] for n in chain if n["step_from"] == i + 1), owner)
        out.append({"i": i, "role": m["role"], "kind": kind, "owner": owner, "content": m["content"]})
    if call is not None:
        out.append({"i": end, "role": "system", "kind": "cfvs", "owner": nid, "content": call["question"]})
    settings = json.loads((folder / "settings.json").read_text())
    system = json.loads((folder / "prompts.json").read_text())["system"]
    for k, v in (settings.get("limits") or {}).items():
        system = system.replace("{" + k + "}", v)
    times = exp_times(folder, s)
    exps = [{"id": e["id"], "answer": e["answer"], "node": e["node"], "status": e["status"],
             "report": (e.get("report") or {}).get("status"), **times[e["id"]]} for e in s["experiments"]]  # fmt: skip
    return {"node": nid, "which": which, "created": node.get("created"), "step_from": node["step_from"],
            "known": node.get("known") or [], "chain": [n["id"] for n in chain], "system": system, "messages": out,
            "experiments": exps, "tools": [t["name"] for t in Scratchpad.tools],
            "cfvs": [{"which": "cfvs:" + c["prefix"] if c["prefix"] else "cfvs", "prefix": c["prefix"]} for c in s_cfvs],
            "replies": call["replies"] if call else None}  # fmt: skip


def files(folder, nid):
    base = folder / "nodes" / nid / "scratch"
    if not base.is_dir():
        return []
    found = [p for p in base.rglob("*") if p.is_file() and not p.is_symlink() and ".home" not in p.parts
             and "experiments" not in p.relative_to(base).parts[:1]]  # fmt: skip
    return [{"path": str(p.relative_to(base)), "size": p.stat().st_size} for p in found]


def read(folder, nid, rel):
    if rel not in {f["path"] for f in files(folder, nid)}:
        return None
    path = folder / "nodes" / nid / "scratch" / rel
    if path.suffix in (".pkl", ".npy", ".npz", ".sobj", ".db"):
        return f"(binary, {path.stat().st_size:,} bytes)"
    text = path.read_bytes()[: swarm_play.FILE_CHARS * 4].decode("utf-8", "replace")
    return text[: swarm_play.FILE_CHARS]
