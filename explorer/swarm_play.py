"""The swarm playground: a team of fresh agents (no trajectory, no context) on one problem, talking on a Slack channel
(slack.py) and sharing a workspace folder, with the system prompt and the first message you edit on the page
(explorer/swarm.html, served by serve.py).

Each agent gets the system prompt and the message with {name}, {n} and {roster} filled in, plus its own note if the
page gives it one. Its tools: its own scratchpad (runs of up to serve.RUN_SECONDS) and the channel (slack_post,
slack_read). Next to its scratchpad.py is workspace/, a link to the run's shared folder, which every agent's runs can
read and write (Sandbox `shared`) and nothing else of the others'.

After a response with tool calls, an agent with unread messages is told so (Slack.unread_notice, a developer message).
A response without one stops it: it is idle until it is tagged or someone replies in a thread it's in (Slack.wakes),
then it is told what woke it (WOKEN) and carries on. You can post on the channel from the page as HUMAN (tagging wakes
agents too). The run ends at Stop, at the budget, when every agent is done (MAX_RESPONSES, refusals, errors), or once
every agent has stopped for NUDGE_AFTER seconds and no nudge will come (both used, or the judge found the proof
complete); IDLE_END is only a fallback.

Each run is kept in runs/basin/swarm/<time>-p<problem>/: settings.json, system.txt and prompt.txt (as written, before
filling in), slack.db and slack.jsonl, events.jsonl, summary.json, workspace/, and agents/<name>/ (conversation.json,
conversation.<i>.json from before each compaction (COMPACT_AT), scratchpad.py and what its runs wrote).

A team may also be left untold (Swarm `told` False, PROMPT_UNTOLD, JUDGE_UNTOLD): it finds the answer as well as
proving it. swarm_untold.py runs those and reads what each ended with (reading.json and verify/ in the run's folder).

The individual baseline (Swarm `solo`): one agent alone under a swarm's rules, with no Slack, no partners and no
shared workspace. Its prompts are the team's with what coordinates a team taken out (SYSTEM_SOLO, PROMPT_SOLO, ...),
and the nudge reaches it as a user message. See "A lone agent" below.

A team may be handed an earlier team's results on the problem (Swarm `lemmas`, a set in LEMMA_SETS): statements with
their proof files, in workspace/lemmas/ and listed in the first message as claims to check. See "Lemmas" below.
"""

import json
import os
import shutil
import threading
import time
import traceback
from dataclasses import replace
from functools import lru_cache, partial
from pathlib import Path

import benchmark
from llm import OpenAILLM, cost, openai_client, prompt_tokens, usage_dict
from scratchpad import Scratchpad
from slack import CHANNEL, HUMAN, Slack, SlackHub
from streamed import CUT_OFF, NO_CALLS, longer_runs, respond
from toolkit import Toolbox

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs" / "basin"  # (named for the earlier work these runs grew out of)
OUT = RUNS / "swarm"
PROBLEMS = [12, 30, 9, 43, 48, 25, 37, 1, 41]  # the problems the page offers: September's nine
# The agents' model, in every system here: its system prompt and its tools are set by whoever runs it (a Swarm,
# an Archive, the verifier).
MODEL, EFFORT, MAX_TOKENS = "gpt-6.1-sol", "medium", 64000
MAX_AGENTS = 8
MAX_RESPONSES = 1000  # per agent: the default, and the most the page may ask for
BUDGET = 20.0  # dollars, the default for a whole run: the dearest proof so far (p41's swarm) cost $11.04, every other
# under $6 (the agents aren't told it, so it changes nothing until a run reaches it). It was $50 until 2026-11-04.
RUN_MINUTES = 360  # the longest scratchpad run an agent may ask for: the default, and the most the page may ask for
IDLE_END = 600  # fallback: seconds with every agent idle and nothing posted before the run ends (see Swarm.watch)
# When every agent has stopped (none working) for NUDGE_AFTER seconds and a judge (the same model, no tools, reading
# the channel's last messages) finds the team's proof incomplete, the lead posts NUDGE, waking everyone: at most
# MAX_NUDGES times a run. A team that claims a complete proof is left to end.
NUDGE = "@channel Stopping isn't an option without proving the result"
NUDGE_AFTER = 60
MAX_NUDGES = 2
JUDGE = """You read the end of a team's Slack channel. The team was told a math problem's answer and asked to prove it completely, every step checked. They have all stopped working. Decide whether their messages claim that the whole proof is done, or whether they stopped short (a part or a step is missing, unproved, or conceded).

Answer with one word: COMPLETE or INCOMPLETE."""
# Compaction: once an agent's request has more than COMPACT_AT input tokens, the agent writes a handoff (COMPACT_ASK,
# in a fork of its conversation, no tool calls) and its conversation becomes the first message, the handoff
# (COMPACTED) and its last COMPACT_KEEP responses, kept whole. Past 272k input tokens every token of a gpt-6.1-sol
# request costs about twice as much, and each request re-reads the whole conversation: in the p1 swarm of
# 2026-11-04, every agent passed 272k after 73–94 minutes, and the 25% of responses above it cost $29 of the run's
# $50. Compacting at 240k would have happened once per agent there (about $30 for the same work) and never in the
# other swarms (whose largest agent reached 164k). Each conversation before a compaction is kept as
# conversation.<i>.json; replay joins them. A handoff takes about 5 minutes and $0.40, mostly its output (tried on
# a p1 agent's conversation: about 2,000 words, after some 30k tokens of reasoning and text).
COMPACT_AT = 240_000
COMPACT_KEEP = 4
COMPACT_TOKENS = 64_000  # the handoff's output limit (its reasoning included), as an agent's response has
COMPACT_RETRY = 20_000  # after a handoff that failed, the input tokens more before trying again
COMPACT_ASK = """Your conversation has grown to about {k}k tokens and is about to be compacted: everything in it before your last {keep} responses will be replaced by what you write now, while the problem statement (your first message) and your instructions stay as they are. Write a handoff to yourself, as your reply, without calling any tool. Cover:
1. What you are working on now, and your plan for what comes next.
2. What is proved or checked so far, by you and by teammates, and where it is: Slack message numbers, and the files in workspace/ and in your own folder, with what each holds and how to use it (function names, file formats).
3. What is still open, what you tried that failed and why, and what you have claimed, promised or been asked for on Slack.
4. The facts, numbers, formulas and parameters you would need again and could not quickly rebuild.
Be specific and complete: up to about 6,000 words."""
COMPACTED = """Your conversation was compacted after it reached about {k}k tokens (compaction {i}): what came before your last few responses has been replaced by the handoff you wrote, below. Slack's history is all still there (slack_read with thread=<id> shows a whole thread, include_read=true the latest messages), and so are your files and workspace/.

{handoff}"""
FILE_CHARS = 400_000  # the most of a file the page is sent

WOKEN = "You had stopped. Since then on Slack, {why}. {notice} Carry on."

SYSTEM = """You are {name}, one of {n} agents ({roster}) working together on one math problem.

## How you work
You call tools; they run in the order you call them, and you see their results in your next response. There is no turn limit. You stop by ending a response without calling a tool. If a teammate tags you, or replies in a thread you're in, after you stop, you are woken and carry on.

## Execution environment
You have your own Python scratchpad file, scratchpad.py: you can read, write, edit and run it. Each run is a fresh Python process, and may take up to {run_time}; while it runs you see nothing on Slack, and what it holds in memory is lost when it ends. A run may use {memory} of memory in all and write files of up to {file_size} each, and it may use multiprocessing with up to {workers} worker processes (no more: it is killed if it has more processes at once).
Next to it is workspace/, a folder the whole team shares: every agent's runs can read and write it, and what one writes there the others can use at once. Put code and results that others can reuse there (for example shared code in workspace/tools.py, or results in workspace/results.json), import shared code with `sys.path.insert(0, "workspace")`, and say on Slack what you put there. Don't overwrite a file someone else wrote: write your own.
The Python environment includes NumPy, SciPy, SymPy, NetworkX, pandas, scikit-learn, gmpy2, Z3, mpmath and SageMath. Sage is imported in the same interpreter (`from sage.all import *`), and GAP and PARI work through it; Sage's Singular-based multivariate ideal methods (such as groebner_basis) crash here, so use SymPy's groebner for those.
There is no public internet access or web search. Do not try to access websites, remote APIs, or install packages. A run cannot start other programs, except more Python processes for multiprocessing.

## Slack
The team shares one Slack channel, #proof. slack_post posts to it, or replies in a message's thread; write @name to tag a teammate. slack_read shows what you haven't read, and after each response you are told when something is waiting. The lead, a person, may post too.
Use the channel to work as a team: split the work, and claim a piece before you start on it so that nobody duplicates it; keep the discussion of one piece in its thread; post each result as soon as it is checked (what was shown, and where in workspace/ its code is); and tag the teammate you need something from."""

PROMPT = """{problem}

The answer is {answer}. This was proved recently, so it is not an open problem: your team's task is to prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at any other answer is not acceptable, and neither is conceding: when an approach fails, try another.

{halves} Split the work, and the pieces of each part, between you on Slack.

Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left."""

# The not-told swarm (swarm_untold.py): the same team, not told the answer, so with no halves either (they state the
# answer). PROMPT_UNTOLD is PROMPT word for word with those taken out: the team finds the answer as well as proving
# it, an answer that settles less than the question asks (a hedge) takes the place of "any other answer", and one
# sentence on what proving an answer means takes the place of the halves.
# JUDGE_UNTOLD is the nudge's judge for it: a team that stops with no answer, or with one that settles less than the
# question asks, stopped short.
# Neither names a shape of answer (2026-11-22). Until then PROMPT_UNTOLD said "Proving it takes two halves" and both
# listed the hedges as "bounds, a range, "not known"": the nine problems they were written on all ask for a value
# pinned between two bounds, which about a third of ArXivMath October does (the rest ask for a set of parameters, or
# for an object to compute).
BUDGET_UNTOLD = 50.0  # dollars, the default for a not-told run
PROMPT_UNTOLD = """{problem}

The answer was proved recently, so it is not an open problem: your team's task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is. Split the work, and the pieces of each part, between you on Slack.

Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left."""
JUDGE_UNTOLD = """You read the end of a team's Slack channel. The team was given a math problem, not its answer, and asked to find the answer and prove it completely, every step checked. They have all stopped working. Decide whether their messages claim that the whole proof of one answer is done, or whether they stopped short (no answer, or one that settles less than the question asks; or a part or a step is missing, unproved, or conceded).

Answer with one word: COMPLETE or INCOMPLETE."""


# A lone agent (Swarm `solo`; swarm_untold.py --solo runs the baseline): one agent under a swarm's rules (the same
# limits, budget, compaction, and the nudge at most twice) with no Slack, no partners and no shared workspace. Each
# of its prompts is the team's word for word with what coordinates a team taken out or put in the singular; every
# changed phrase must be found in the team's prompt (`reworded`), so the two can't drift apart.
# - Its tools are the scratchpad's alone.
# - Each time it stops, its reply is kept where a team's posts are (the run's hub, slack.jsonl), and so are the
#   lead's messages (the nudge, or the page's): that dialogue is what the judge, the page and the readers of the run
#   see in place of a channel. The agent has no Slack: a lead's message reaches it as a user message.
def reworded(text, pairs):
    for old, new in pairs:
        assert old in text, f"not in the prompt: {old!r}"
        text = text.replace(old, new)
    return text


SYSTEM_SOLO = reworded(SYSTEM, [
    ("You are {name}, one of {n} agents ({roster}) working together on one math problem.",
     "You are working on one math problem."),
    (" If a teammate tags you, or replies in a thread you're in, after you stop, you are woken and carry on.", ""),
    ("; while it runs you see nothing on Slack, and what it holds", "; what it holds"),
    (next(line for line in SYSTEM.split("\n") if line.startswith("Next to it is workspace/")) + "\n", ""),
    (SYSTEM[SYSTEM.index("\n\n## Slack"):], ""),
])  # fmt: skip
assert not any(word in SYSTEM_SOLO for word in ("Slack", "team", "workspace", "{name}", "{n}", "{roster}"))
ALONE = [
    ("your team's task is", "your task is"),
    (" Split the work, and the pieces of each part, between you on Slack.", ""),
    ("Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left.",
     "Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left."),
]  # fmt: skip
PROMPT_SOLO, PROMPT_UNTOLD_SOLO = reworded(PROMPT, ALONE), reworded(PROMPT_UNTOLD, ALONE)
NUDGE_SOLO = reworded(NUDGE, [("@channel ", "")])
JUDGE_ALONE = [
    ("You read the end of a team's Slack channel. The team was",
     "You read what an agent wrote each time it stopped working, and what its lead answered. The agent was"),
    ("They have all stopped working. Decide whether their messages claim", "It has stopped. Decide whether it claims, at the end,"),
    ("or whether they stopped short", "or whether it stopped short"),
]  # fmt: skip
JUDGE_SOLO, JUDGE_UNTOLD_SOLO = reworded(JUDGE, JUDGE_ALONE), reworded(JUDGE_UNTOLD, JUDGE_ALONE)
COMPACT_ASK_SOLO = reworded(COMPACT_ASK, [
    (", by you and by teammates, and where it is: Slack message numbers, and the files in workspace/ and in your own folder,",
     ", and where it is: the files in your folder,"),
    (", and what you have claimed, promised or been asked for on Slack.", ", and what you have been asked for."),
])  # fmt: skip
COMPACTED_SOLO = reworded(COMPACTED, [
    (" Slack's history is all still there (slack_read with thread=<id> shows a whole thread, include_read=true the "
     "latest messages), and so are your files and workspace/.", " Your files are all still there."),
])  # fmt: skip
NO_REPLY = "(stopped without writing anything)"  # kept as the reply of a lone agent that stops with no text
REPLY_CHARS = 10**7  # of a lone agent's reply in the hub: all of it (a team's post is held to SlackHub's 6,000)

# Each problem's answer as the first message states it (the reference answer), and its two halves: what each bound
# means, in the problem's own terms (no method).
ANSWERS = {12: "44", 30: r"\(D_s=3\cdot 2^{s-1}-2\)", 9: r"\(\beta(p)=1+\frac{1}{p(p-1)}\)", 43: "2",
           48: r"\(\lim_{j\to\infty}\kappa(U_j)=3\)", 25: r"\(\frac{1}{9}\)", 37: r"\(F(d)=d-3\)", 1: "4",
           41: r"\(b(d,k)=d-2\)"}
HALVES = {
    12: "Proving 44 takes two halves: dim ≤ 44 (enough independent relations among the degree-12 kappa monomials) and "
        "dim ≥ 44 (enough independent linear functionals on degree-12 kappa polynomials that vanish on every true "
        "relation).",
    30: r"Proving it takes two halves, for every \(s\ge3\): \(D_s\le 3\cdot2^{s-1}-2\) (in dimension "
        r"\(3\cdot2^{s-1}-2\), every collection of \(2^s-2\) such measures has two hyperplanes cutting each of them "
        r"into four quarters) and \(D_s\ge 3\cdot2^{s-1}-2\) (in every dimension \(d<3\cdot2^{s-1}-2\), some "
        r"collection of \(2^s-2\) such measures has no such pair of hyperplanes).",
    9: r"Proving it takes two halves, for every \(p\in(1,2)\cup(2,\infty)\): \(\beta(p)\le1+\frac1{p(p-1)}\) (the "
       r"inequality holds, with a constant independent of \(W\) and \(f\), for \(\gamma=1+\frac1{p(p-1)}\)) and "
       r"\(\beta(p)\ge1+\frac1{p(p-1)}\) (for every smaller \(\gamma\), no constant works: there are weights \(W\) "
       r"with \([W]_{A_p}\) as large as you like and functions \(f\) for which the ratio "
       r"\(\|Hf\|_{L^p(W)}/\|f\|_{L^p(W)}\) exceeds every multiple of \([W]_{A_p}^{\gamma}\)).",
    43: r"Proving 2 takes two halves: every such Hamiltonian whose time-one map has finitely many fixed points has at "
        r"least 2 of them, and some smooth 1-periodic Hamiltonian \(H\) has a time-one map \(\varphi_H^1\) with "
        r"exactly 2 fixed points (an explicit \(H\), and a proof that it has no others).",
    48: r"Proving it takes two halves, for every large \(j\): \(\kappa(U_j)\le3\) (a smooth \(\psi\) on \(U_j\) "
        r"with every sublevel set compact whose Levi form has at least 2 strictly positive eigenvalues outside a "
        r"compact set) and \(\kappa(U_j)\ge3\) (no such \(\psi\) has at least 3 strictly positive eigenvalues "
        r"outside a compact set).",
    25: r"Proving it takes two halves: every \(c>\frac19\) has the property (a finite triangle-free \(H_c\) to which "
        r"every such \(G\) on any number of vertices maps), and no \(c<\frac19\) has it (for every finite "
        r"triangle-free \(H\), some such \(G\) with minimum degree at least \(cn\) has no homomorphism to \(H\)).",
    37: r"Proving it takes two halves, for every \(d\ge8\): \(F(d)\le d-3\) (every nonempty finite poset \(P\) with "
        r"\(\dim P\ge3\) has \(\dim(P\times Q_d)\le\dim P+d-3\)) and \(F(d)\ge d-3\) (some such \(P\) has "
        r"\(\dim(P\times Q_d)\ge\dim P+d-3\)).",
    1: r"Proving 4 takes two halves: for \(s=1,2,3\), every nonterminating orbit, for every \(n,A,b,x_0\), has "
       r"\((y_{2k})\) converging in Euclidean norm; and for \(s=4\) there exist \(n,A,b,x_0\) with \(r_k\ne0\) for "
       r"every \(k\) for which \((y_{2k})\) does not converge.",
    41: r"Proving it takes two halves, for all integers \(d\ge3\) and \(k\ge1\): \(b(d,k)\le d-2\) (for every "
        r"such \(\Delta\), \(d-2\) new vertices and some ordering keep every \(\Delta_i\) \(k\)-decomposable) and "
        r"\(b(d,k)\ge d-2\) (some such \(\Delta\) admits no such ordering with fewer than \(d-2\) new vertices).",
}


# Earlier defaults of SYSTEM: a page that still holds one unedited is given SYSTEM instead. The first said less of
# the environment ("up to 30 minutes", no multiprocessing), before the run's limits were filled in. Both gave p12's
# files as the example of what to share (until 2026-11-22).
SYSTEM_P12 = SYSTEM.replace("(for example shared code in workspace/tools.py, or results in workspace/results.json)",
                            "(for example workspace/relations.py, or a matrix in workspace/pairing.json)")  # fmt: skip
assert SYSTEM_P12 != SYSTEM
SUPERSEDED = [
    SYSTEM_P12.replace(
        " and may take up to {run_time}; while it runs you see nothing on Slack, and what it holds in memory is lost when "
        "it ends. A run may use {memory} of memory in all and write files of up to {file_size} each, and it may use "
        "multiprocessing with up to {workers} worker processes (no more: it is killed if it has more processes at once).",
        " and may take up to 30 minutes.",
    ).replace(" A run cannot start other programs, except more Python processes for multiprocessing.",
              " A run cannot start other programs."),
    SYSTEM_P12,
]  # fmt: skip


def offered(p, told=True):
    """Whether a swarm can be started on problem p: one of the page's problems, or, when it isn't told the answer, a
    problem of another ArXivMath edition (benchmark.EDITIONS: 1012 is October's p12). Those have no answer or halves
    here, so no told first message."""
    return p in PROBLEMS or (not told and benchmark.in_edition(p))


@lru_cache(maxsize=None)
def september():
    """September's problems (benchmark.DATASET), loaded once."""
    return benchmark.Benchmark()


def problem_text(p):
    """Problem p's statement, as the dataset has it."""
    if benchmark.in_edition(p):
        return benchmark.edition(p // 100)[p]["problem"]
    return september().get_problem(p)["problem"]


def agent_llm(gate):
    """The agents' model as every run here called it (MODEL at EFFORT). `gate`: a semaphore that caps its calls in
    flight."""
    return OpenAILLM(client=openai_client(), model=MODEL, system="", tools=[], max_tokens=MAX_TOKENS, effort=EFFORT,
                     gate=gate)  # fmt: skip


def first_message(p, told=True, solo=False):
    """The first message on problem p, {name}, {n} and {roster} still to fill in: told p's answer and its halves or
    not, a team's or a lone agent's."""
    template = {(True, False): PROMPT, (True, True): PROMPT_SOLO, (False, False): PROMPT_UNTOLD,
                (False, True): PROMPT_UNTOLD_SOLO}[bool(told), bool(solo)]  # fmt: skip
    text = template.replace("{problem}", problem_text(p).strip())
    return text.replace("{answer}", ANSWERS[p]).replace("{halves}", HALVES[p]) if told else text


def defaults(p):
    return {"problem": p, "answer": ANSWERS[p], "system": SYSTEM, "system_solo": SYSTEM_SOLO,
            "prompt": first_message(p), "prompt_untold": first_message(p, told=False),
            "prompt_solo": first_message(p, solo=True), "prompt_untold_solo": first_message(p, told=False, solo=True),
            "n": 4, "budget": BUDGET, "budget_untold": BUDGET_UNTOLD, "max_agents": MAX_AGENTS,
            "max_responses": MAX_RESPONSES, "run_minutes": RUN_MINUTES,
            "idle_end": IDLE_END, "nudge_after": NUDGE_AFTER, "max_nudges": MAX_NUDGES, "superseded": SUPERSEDED}  # fmt: skip


# ---- Lemmas: an earlier team's results, handed to a team ---------------------------------------------------------
# Teams on one problem prove the same things over and over (the p1 archive of 2026-11-20: s = 1 four times, s = 2
# twice), so a team can be given what an earlier one proved. Only statements and their proofs are handed over: not
# the answer that team was told, how its run ended, or what it tried and dropped, which would pass its frame on. And
# they are handed over as claims to check, never as facts: the verifier has called false proofs sound (p43, the same
# day), and a false lemma given as a fact would turn every later team.
# A set is a folder LEMMA_SETS/<name>/: lemmas.json ([{"statement": ..., "files": [...]}]) and the files it names.

LEMMA_SETS = RUNS / "lemmas"
LEMMAS = """An earlier team worked on this problem and left the results below, each with its proof, in \
workspace/lemmas/. They are that team's claims, and nobody has checked them: check a proof before you rely on it, \
and say in your proof which of them you used.

{lemmas}"""


def lemma_set(name):
    """A lemma set: its folder and its list ([{statement, files}]). ValueError if there is none by that name, or it
    names a file it doesn't have."""
    folder = LEMMA_SETS / str(name)
    if Path(str(name)).name != str(name) or not (folder / "lemmas.json").exists():
        raise ValueError(f"no lemma set {name!r} in {LEMMA_SETS}")
    lemmas = json.loads((folder / "lemmas.json").read_text())
    if missing := [f for lemma in lemmas for f in lemma["files"] if Path(f).name != f or not (folder / f).is_file()]:
        raise ValueError(f"lemma set {name!r} has no {', '.join(missing)}")
    return folder, lemmas


def with_lemmas(prompt, lemmas):
    """The first message with the lemmas listed (LEMMAS) before its last paragraph (when to stop), which stays last."""
    note = LEMMAS.format(lemmas="\n".join(
        f"{i}. {lemma['statement']} Files: {', '.join('workspace/lemmas/' + f for f in lemma['files'])}."
        for i, lemma in enumerate(lemmas, 1)))  # fmt: skip
    head, sep, last = prompt.rstrip().rpartition("\n\n")
    return f"{head}\n\n{note}\n\n{last}" if sep else f"{prompt}\n\n{note}"


def fill(template, name, names, limits=None, keep=()):
    """{name}, {n} and {roster} filled in, and the run's `limits` ({run_time}, {memory}, ...); any other brace is left
    as it is (the prompt has LaTeX). The texts in `keep` are left as they are wherever the template has them: the
    problem's statement, and the answer and halves a team is told, are LaTeX, and a {n} in them isn't ours. (Until
    2026-11-22 it was filled in there too: p1045's \\frac{r(...)}{n} reached a lone agent as {1}.)"""
    values = {"name": name, "n": str(len(names)), "roster": ", ".join(names), **(limits or {})}
    for i, text in enumerate(keep):  # a kept text with one of our braces in it: fill only what is around it
        if text in template and any("{" + k + "}" in text for k in values):
            return text.join(fill(part, name, names, limits, keep[i + 1 :]) for part in template.split(text))
    for k, v in values.items():
        template = template.replace("{" + k + "}", v)
    return template


def size(n_bytes):
    return f"{n_bytes / 2**30:g} GB" if n_bytes >= 2**30 else f"{n_bytes / 2**20:g} MB"


def duration(seconds):
    return f"{seconds / 3600:g} hours" if seconds >= 3600 else f"{seconds / 60:g} minutes"


class WithWorkspace:
    """A sandbox whose runs may read and write the shared folder too (Sandbox.run `shared`), for Scratchpad."""

    def __init__(self, sandbox, workspace):
        self.sandbox, self.workspace = sandbox, workspace

    def __getattr__(self, name):  # memory_mb, max_output, ...
        return getattr(self.sandbox, name)

    def run(self, folder, filename, timeout):
        return self.sandbox.run(folder, filename, timeout, shared=[self.workspace])


class Swarm:
    """One swarm run: an agent thread each and a thread that waits for them; its events kept for any page that
    (re)connects (serve.py's stream reads `events` and `cond`)."""

    def __init__(self, llm, make_sandbox, p, system, prompt, notes, n, budget, max_responses=MAX_RESPONSES,
                 run_minutes=RUN_MINUTES, answer=None, folder=None, run_id=None, settle=True, told=True, solo=False,
                 lemmas=None, keep=()):
        """`llm`: the model, its tools set here (run_scratchpad's limit shown as `run_minutes`). `answer`: the answer
        the first message states, if it isn't the problem's (ANSWERS): what the judge is told the team was told (a
        wrong answer, as a negative control). `folder` and `run_id`: where the run is kept and its id, if not
        OUT/<time>-p<problem> and that folder's name (a prover archive's experiment, prover_archive.py). `settle` (the
        default): end as soon as every agent is idle and no nudge will come (see watch); False waits IDLE_END.
        `told` False: the first message states no answer (PROMPT_UNTOLD), so the nudge's judge is JUDGE_UNTOLD and
        is told none. `solo`: a lone agent (see "A lone agent" above): n is 1, `system` and `prompt` are a lone
        agent's (SYSTEM_SOLO, first_message(p, told, solo=True)). `lemmas`: a lemma set's name (see "Lemmas" above):
        its files are copied to workspace/lemmas/ and its statements listed in the first message. `keep`: texts of
        the first message's to leave as written when its braces are filled in (see fill), besides the problem's
        statement and the answer, which always are: the halves an archive's model wrote."""
        if solo and n != 1:
            raise ValueError("a lone agent is one agent")
        if solo and lemmas:
            raise ValueError("a lone agent has no workspace/ for lemmas")
        self.lemmas = str(lemmas) if lemmas else None
        if self.lemmas:
            lemma_folder, listed = lemma_set(self.lemmas)
            prompt = with_lemmas(prompt, listed)
        self.settle, self.told, self.solo = settle, told, solo
        self.names = [f"agent_{i}" for i in range(1, n + 1)]
        self.run_seconds = int(run_minutes * 60)
        llm = replace(llm, tools=longer_runs(Scratchpad.tools, self.run_seconds) + ([] if solo else Slack.tools))
        self.llm, self.p, self.system, self.prompt, self.budget = llm, p, system, prompt, budget
        self.answer = None if not told else str(answer).strip() if answer and str(answer).strip() else ANSWERS[p]
        self.keep = [problem_text(p).strip(), *(str(k) for k in keep), *([self.answer] if self.answer else [])]
        self.max_responses = max_responses
        self.notes = {name: str(notes[i]).strip() if i < len(notes) else "" for i, name in enumerate(self.names)}
        stamp = time.strftime("%Y%m%d-%H%M%S")
        while (OUT / f"{stamp}-p{p}").exists():  # two swarms on one problem started in the same second
            stamp += "b"
        self.folder = Path(folder) if folder else OUT / f"{stamp}-p{p}"
        self.id = run_id or self.folder.name  # unique: swarms on different problems often start in the same second
        self.workspace = self.folder / "workspace"
        self.events, self.cond, self.stop, self.wake = [], threading.Condition(), threading.Event(), threading.Condition()
        self.state = {a: "working" for a in self.names}  # working | idle | done
        self.responses = {a: 0 for a in self.names}
        self.spent = {a: 0.0 for a in self.names}
        self.compactions = {a: 0 for a in self.names}
        self.told_upto = {a: 0 for a in self.names}  # the last message id an agent has been told about
        self.last_activity = time.time()
        self.end_reason, self.ended = None, False
        self.nudges, self.judged = 0, None  # nudges posted; last_activity when the judge last found a proof complete
        (self.folder if solo else self.workspace).mkdir(parents=True)  # a lone agent has no shared folder
        if self.lemmas:  # only the files the set lists: a note on where they came from stays behind
            (self.workspace / "lemmas").mkdir()
            for f in sorted({f for lemma in listed for f in lemma["files"]}):
                shutil.copyfile(lemma_folder / f, self.workspace / "lemmas" / f)
        self.nudge = NUDGE_SOLO if solo else NUDGE
        self.hub = SlackHub(self.names, db_path=str(self.folder / "slack.db"), on_post=self.on_post,
                            **({"max_chars": REPLY_CHARS} if solo else {}))  # fmt: skip
        self.sandbox = make_sandbox(self.stop)
        box = self.sandbox
        self.limits = {"run_time": duration(self.run_seconds), "memory": size(box.memory_mb * 2**20),
                       "file_size": size(box.max_file), "workers": str(max(1, box.processes - 2))}  # fmt: skip
        (self.folder / "system.txt").write_text(system)
        (self.folder / "prompt.txt").write_text(prompt)
        (self.folder / "settings.json").write_text(json.dumps(
            {"problem": p, "answer": self.answer, "told": told, "solo": solo, "lemmas": self.lemmas, "n": n, "budget": budget,
             "notes": self.notes,
             "model": llm.model,
             "effort": llm.effort, "max_responses": max_responses, "run_minutes": run_minutes, "idle_end": IDLE_END, "limits": self.limits,
             "nudge": self.nudge, "max_nudges": MAX_NUDGES, "nudge_after": NUDGE_AFTER, "settle": settle, "compact_at": COMPACT_AT,
             "compact_keep": COMPACT_KEEP},
            indent=1))  # fmt: skip
        threading.Thread(target=self.main, daemon=True).start()

    @property
    def cost(self):
        return sum(self.spent.values())

    def emit(self, a=None, **event):
        if a is not None:
            event["a"] = a
        with self.cond:
            self.events.append(event)
            self.cond.notify_all()
            if event["k"] not in ("think", "say", "args"):  # deltas are many; the conversations keep their text
                with open(self.folder / "events.jsonl", "a") as f:
                    f.write(json.dumps(event) + "\n")

    def poke(self):
        with self.wake:
            self.wake.notify_all()

    def on_post(self, row):
        self.last_activity = time.time()
        self.emit(k="slack", **row)
        self.hub.export(self.folder / "slack.jsonl")
        self.poke()

    def post(self, body, thread=None):
        """A message from the person on the page (to a lone agent: a user message, see `loop`)."""
        if self.ended:
            raise ValueError("the run has ended")
        return self.hub.post(HUMAN, body, None if self.solo else thread)

    def end(self, reason):
        if self.end_reason is None:
            self.end_reason = reason
        self.stop.set()
        self.poke()

    def set_state(self, a, state, why=""):
        self.state[a] = state
        self.emit(a, k="state", state=state, why=why, n=self.responses[a], cost=round(self.spent[a], 4))
        self.poke()

    # ---- the run ----------------------------------------------------------------

    def main(self):
        try:
            self.emit(k="start", folder=str(self.folder.resolve().relative_to(ROOT)), agents=self.names,
                      channel=CHANNEL, budget=self.budget)  # fmt: skip
            if why := self.sandbox.ready():
                raise RuntimeError(f"the sandbox isn't ready: {why}")
            threads = [threading.Thread(target=self.agent, args=(a,), daemon=True) for a in self.names]
            for t in threads:
                t.start()
            threading.Thread(target=self.watch, daemon=True).start()
            for t in threads:
                t.join()
            reason = self.end_reason or ("all agents idle" if any(s == "idle" for s in self.state.values())
                                         else "all agents done")  # fmt: skip
        except Exception as e:
            traceback.print_exc()
            reason = f"error: {e!r}"
        self.ended = True
        self.stop.set()
        summary = {"reason": reason, "cost": round(self.cost, 4),
                   "agents": {a: {"state": self.state[a], "responses": self.responses[a], "cost": round(self.spent[a], 4),
                                  "compactions": self.compactions[a]} for a in self.names},
                   "messages": len(self.hub.dump())}  # fmt: skip
        (self.folder / "summary.json").write_text(json.dumps(summary, indent=1))
        self.hub.export(self.folder / "slack.jsonl")
        self.sandbox.close()
        self.emit(k="end", reason=reason, cost=round(self.cost, 4))

    def watch(self):
        """The automatic nudge: see NUDGE. With `settle`, the run also ends once every agent has stopped for
        NUDGE_AFTER seconds and no nudge will come: they are all used, or the judge found the proof complete."""
        while not self.stop.wait(5):
            if (any(s == "working" for s in self.state.values()) or not any(s == "idle" for s in self.state.values())
                    or time.time() - self.last_activity < NUDGE_AFTER):  # fmt: skip
                continue
            if self.nudges >= MAX_NUDGES or self.judged == self.last_activity:
                if self.settle:
                    self.end("all agents idle, the nudges used up" if self.nudges >= MAX_NUDGES
                             else "all agents idle, the judge found the proof complete")  # fmt: skip
                continue
            at = self.last_activity
            try:
                complete = self.judge_complete()
            except Exception as e:
                self.emit(k="note", text=f"the judge failed ({e!r}); nudging anyway")
                complete = False
            if self.stop.is_set() or self.last_activity != at:  # someone woke up meanwhile
                continue
            if complete:
                self.judged = at
                self.emit(k="note", text="the judge found the proof complete: no nudge")
                if self.settle:
                    self.end("all agents idle, the judge found the proof complete")
                continue
            self.nudges += 1
            self.emit(k="note", text=f"nudge {self.nudges} of {MAX_NUDGES}: the {'agent' if self.solo else 'team'} stopped short")
            self.hub.post(HUMAN, self.nudge)

    def judge_complete(self):
        """Whether the channel's last messages claim the whole proof (JUDGE); for a lone agent, what it wrote each
        time it stopped and what the lead answered (JUDGE_SOLO). Its cost counts toward the budget."""
        rows = self.hub.dump()[-15:]
        log = "\n\n".join(f"#{r['id']} {r['sender']}: {r['body']}" for r in rows)
        system = {(True, False): JUDGE, (False, False): JUDGE_UNTOLD, (True, True): JUDGE_SOLO,
                  (False, True): JUDGE_UNTOLD_SOLO}[bool(self.told), bool(self.solo)]  # fmt: skip
        llm = replace(self.llm, tools=[], system=system, max_tokens=4000)
        told = f"The answer {'it was' if self.solo else 'they were'} told: {self.answer}\n\n" if self.told else ""
        reply = llm.create([{"role": "user", "content": told + log}])
        self.spent["judge"] = self.spent.get("judge", 0.0) + cost(llm.model, usage_dict(reply.message.usage))
        text = "".join(getattr(b, "text", "") or "" for b in reply.message.content).upper()
        return "INCOMPLETE" not in text and "COMPLETE" in text

    def agent(self, a):
        try:
            self.loop(a)
        except Exception as e:
            traceback.print_exc()
            self.emit(a, k="note", text=f"error: {e!r}")
            self.set_state(a, "done", f"error: {e!r}")

    def loop(self, a):
        slack = self.hub.agent(a)
        folder = self.folder / "agents" / a
        if self.solo:
            box = Toolbox(Scratchpad(folder, self.sandbox, max_seconds=self.run_seconds))
        else:
            pad = Scratchpad(folder, WithWorkspace(self.sandbox, self.workspace), max_seconds=self.run_seconds)
            (folder / "workspace").symlink_to(self.workspace.resolve(), target_is_directory=True)
            box = Toolbox(pad, slack)
        assert [t["name"] for t in box.tools] == [t["name"] for t in self.llm.tools], "the tools shown aren't the tools run"
        llm = replace(self.llm, system=fill(self.system, a, self.names, self.limits))
        first = fill(self.prompt, a, self.names, self.limits, self.keep) + (f"\n\n{self.notes[a]}" if self.notes[a] else "")
        messages = [{"role": "user", "content": first}]
        self.emit(a, k="told", text=first, first=True)
        emit, refusals = partial(self.emit, a), 0
        last_in, compact_at = 0, COMPACT_AT  # the input tokens of the agent's last request; when to compact

        def save():
            (folder / "conversation.json").write_text(json.dumps({"agent": a, "system": llm.system, "messages": messages},
                                                                 indent=1))  # fmt: skip

        def tell(text):
            messages.append({"role": "system", "content": text})
            self.told_upto[a] = slack.last_id()
            self.emit(a, k="told", text=text)

        def hear(rows):  # a lone agent: the lead's messages, each as a user message
            for r in rows:
                messages.append({"role": "user", "content": r["body"]})
                self.emit(a, k="told", text=r["body"])
            self.told_upto[a] = rows[-1]["id"]

        while not self.stop.is_set():
            if self.responses[a] >= self.max_responses:
                return self.set_state(a, "done", f"cap ({self.max_responses} responses)")
            self.responses[a] += 1
            n = self.responses[a]
            self.last_activity = time.time()
            self.emit(a, k="response", n=n)
            try:
                reply = respond(llm, messages, n, emit, self.stop)
            except InterruptedError:
                break
            self.spent[a] += cost(llm.model, usage_dict(reply.usage))
            last_in = prompt_tokens(usage_dict(reply.usage))
            if self.cost >= self.budget:
                self.end(f"budget (${self.cost:.2f})")
            if reply.stop_reason == "refusal":
                refusals += 1
                self.emit(a, k="note", text=f"refused ({refusals}); asking again" if refusals <= 2 else "refused")
                if refusals > 2:
                    return self.set_state(a, "done", "refused")
                continue
            messages.append({"role": "assistant", "content": [b.to_dict() for b in reply.content]})
            results = []
            for block in (b for b in reply.content if b.type == "tool_use"):
                result = box.handle(block) if reply.stop_reason != "max_tokens" else {
                    "type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": "Not run: your response was cut off at the output limit."}  # fmt: skip
                results.append(result)
                self.emit(a, k="result", call_id=block.id, out=result["content"], error=result["is_error"])
            if results or reply.stop_reason != "end_turn":
                messages.append({"role": "user", "content": results or (CUT_OFF if reply.stop_reason == "max_tokens"
                                                                        else NO_CALLS)})  # fmt: skip
            save()
            self.emit(a, k="cost", n=n, cost=round(self.spent[a], 4), total=round(self.cost, 4), stop=reply.stop_reason)
            stopped = reply.stop_reason == "end_turn" and not results
            if stopped and self.solo:  # its reply, kept where a team's posts are
                self.hub.post(a, "".join(b.text for b in reply.content if b.type == "text").strip() or NO_REPLY)
            if self.stop.is_set():
                break
            if stopped:
                woke = self.sleep(a, slack)
                if woke is None:
                    break
                if self.solo:
                    hear(woke)
                else:
                    tell(WOKEN.format(why=why_woken(woke), notice=slack.unread_notice()).replace("  ", " "))
            elif self.solo:
                if said := self.lead_said(a):  # posted from the page while it worked
                    hear(said)
            elif notice := slack.unread_notice():
                tell(notice)
            if last_in > compact_at and not self.stop.is_set():
                kept = self.compact(a, llm, messages, last_in)
                if kept is None:
                    compact_at = last_in + COMPACT_RETRY
                else:
                    messages[:] = kept
                    compact_at = COMPACT_AT
            save()
        if self.state[a] != "idle":
            self.set_state(a, "done", self.end_reason or "stopped")

    def sleep(self, a, slack):
        """Wait, idle, until `a` is tagged or someone replies in a thread it's in (the messages that did it; for a
        lone agent, until the lead says something: those rows), or until the run ends or every agent has been idle
        for IDLE_END seconds with nothing posted (None)."""
        self.set_state(a, "idle", "stopped by the agent")
        with self.wake:
            while not self.stop.is_set():
                if woke := self.lead_said(a) if self.solo else slack.wakes(self.told_upto[a]):
                    self.set_state(a, "working", "woken")
                    return woke
                if all(s != "working" for s in self.state.values()) and time.time() - self.last_activity > IDLE_END:
                    self.poke()
                    return None
                self.wake.wait(timeout=5)
        return None

    def lead_said(self, a):
        """The lead's messages that lone agent `a` hasn't been given yet, as rows."""
        return [r for r in self.hub.dump() if r["sender"] == HUMAN and r["id"] > self.told_upto[a]]

    def compact(self, a, llm, messages, last_in):
        """`a`'s conversation compacted (see COMPACT_AT): the first message, the handoff it writes now, and its last
        COMPACT_KEEP responses with what followed them. None, with a note, when there's nothing to drop or the handoff
        fails; the conversation then goes on as it was. The handoff's cost counts toward the budget."""
        turns = [i for i, m in enumerate(messages) if m["role"] == "assistant"]
        if len(turns) <= COMPACT_KEEP or turns[-COMPACT_KEEP] < 2:
            return None
        k = round(last_in / 1000)
        try:
            ask = COMPACT_ASK_SOLO if self.solo else COMPACT_ASK
            handoff, spent = self.handoff(llm, messages, ask.format(k=k, keep=COMPACT_KEEP))
        except Exception:
            traceback.print_exc()
            handoff, spent = "", 0.0
        self.spent[a] += spent
        if self.cost >= self.budget:
            self.end(f"budget (${self.cost:.2f})")
        if not handoff.strip():
            self.emit(a, k="note", text=f"compaction at {k}k tokens failed (no handoff): carrying on uncompacted")
            return None
        self.compactions[a] += 1
        i = self.compactions[a]
        folder = self.folder / "agents" / a
        (folder / f"conversation.{i}.json").write_text(json.dumps({"agent": a, "system": llm.system, "messages": messages},
                                                                 indent=1))  # fmt: skip
        text = (COMPACTED_SOLO if self.solo else COMPACTED).format(k=k, i=i, handoff=handoff.strip())
        self.emit(a, k="note", text=f"compaction {i}: the conversation reached {k}k tokens; it is now the first message, "
                                    f"the agent's handoff ({len(handoff.split()):,} words) and its last {COMPACT_KEEP} "
                                    f"responses (the whole of it kept in conversation.{i}.json)")  # fmt: skip
        self.emit(a, k="told", text=text)
        return [messages[0], {"role": "user", "content": text}, *messages[turns[-COMPACT_KEEP]:]]

    def handoff(self, llm, messages, ask):
        """The handoff an agent writes when asked (`ask`, a developer message after its conversation): (text, dollars). The
        request is the agent's own, so it reads the conversation from the cache; if the model calls a tool anyway, it is
        asked once more with tools turned off."""
        request = llm.request([*messages, {"role": "system", "content": ask}], COMPACT_TOKENS)
        spent = 0.0
        for req in (request, {**request, "tool_choice": "none"}):
            reply = llm.send(req).message
            spent += cost(llm.model, usage_dict(reply.usage))
            text = "".join(b.text for b in reply.content if b.type == "text")
            if text.strip():
                break
        return text, spent

    def files(self):
        return files(self.folder)

    def read(self, rel):
        return read(self.folder, rel)


def why_woken(woke):
    """'agent_2 tagged you (#14), and agent_3 replied in a thread you're in (#15)'."""
    tags = [f"{s} tagged you (#{i})" for i, s, tagged in woke if tagged]
    replies = [f"{s} replied in a thread you're in (#{i})" for i, s, tagged in woke if not tagged]
    parts = tags + replies
    return ", and ".join([", ".join(parts[:-1]), parts[-1]]) if len(parts) > 1 else parts[0]


# ---- saved runs: what the page shows of a run on disk ---------------------------------------------------------------

KINDS = {"swarm": OUT}
ARCHIVES = ROOT / "runs" / "archive"  # prover_archive.OUT: an archive's experiments are swarms in its folder


def run_folder(key):
    """The folder of a saved run, from its key ('swarm/<name>', or 'archive/<archive>/<e>' for a prover archive's
    experiment), or None."""
    kind, _, name = str(key).partition("/")
    if kind == "archive":
        parts = name.split("/")
        if len(parts) != 2 or not all(parts) or any(x.startswith(".") for x in parts) or not parts[1].startswith("e"):
            return None
        folder = ARCHIVES / parts[0] / parts[1]
        return folder if (folder / "settings.json").exists() else None
    if kind not in KINDS or not name or "/" in name or name.startswith("."):
        return None
    folder = KINDS[kind] / name
    return folder if folder.is_dir() else None


def saved_runs():
    """Every saved run, newest first: [{key, kind, name, agents, reason, cost}]."""
    out = []
    for kind, base in KINDS.items():
        for folder in sorted(base.glob("*"), reverse=True):
            if not folder.is_dir():
                continue
            summary = json.loads((folder / "summary.json").read_text()) if (folder / "summary.json").exists() else {}
            settings = json.loads((folder / "settings.json").read_text()) if (folder / "settings.json").exists() else {}
            reason, spent = summary.get("reason"), summary.get("cost")
            out.append({"key": f"{kind}/{folder.name}", "kind": kind, "name": folder.name, "reason": reason,
                        "cost": spent, "agents": settings.get("n", 1), "problem": settings.get("problem"),
                        "told": settings.get("told", True), "solo": settings.get("solo", False),
                        "reading": reading_of(folder)})  # fmt: skip
    return out


def alive(pid):
    try:
        os.kill(int(pid), 0)
    except PermissionError:
        return True
    except (OSError, TypeError, ValueError):
        return False
    return True


def reading_of(folder):
    """A run's reading (swarm_untold.py), in brief: None if it has none; {state: "reading", stage, started, at,
    answer} while it is read (stage: answer, contract, verify, grade); {state: "interrupted", stage} if its reader
    died; {state: "read", answer, definite, verdict, acknowledged, stop, correct, solved, cost} once read."""
    live, done = folder / "reading.live.json", folder / "reading.json"
    if live.exists():
        try:
            lv = json.loads(live.read_text())
        except (OSError, ValueError):
            lv = {}
        if alive(lv.get("pid")):
            return {"state": "reading", **{k: lv.get(k) for k in ("stage", "started", "at", "answer")}}
        if not done.exists():
            return {"state": "interrupted", "stage": lv.get("stage")}
    if not done.exists():
        return None
    try:
        r = json.loads(done.read_text())
    except (OSError, ValueError):
        return None
    v = r.get("verify") or {}
    return {"state": "read", **{k: r.get(k) for k in ("answer", "definite", "stop", "correct", "solved", "cost")},
            "verdict": v.get("verdict"), "acknowledged": v.get("acknowledged")}  # fmt: skip


VERIFIER_RESULT_CHARS = 4000  # of each tool result the page is sent


def verifier(key):
    """A run's reading in full, for the swarm page's Verifier tab: {state (reading_of), reading (reading.json, or
    None while it is read), task (the verifier's first message), steps}. steps: the verifier's responses so far, from
    verify/conversation.json (written after each one): [{thinking, text, calls: [{name, input, result, error}]}]."""
    folder = run_folder(key)
    if folder is None:
        return None
    load = lambda f: json.loads(f.read_text()) if f.exists() else None  # noqa: E731
    try:
        messages = (load(folder / "verify" / "conversation.json") or {}).get("messages", [])
    except ValueError:  # caught while it is written
        messages = []
    task, steps, results = None, [], {}
    for m in messages:
        if m["role"] == "user" and isinstance(m.get("content"), list):
            for b in m["content"]:
                if b.get("type") == "tool_result":
                    c = b.get("content")
                    c = c if isinstance(c, str) else "".join(x.get("text", "") for x in c or [] if isinstance(x, dict))
                    results[b.get("tool_use_id")] = (c[:VERIFIER_RESULT_CHARS] + ("\n…" if len(c) > VERIFIER_RESULT_CHARS else ""),
                                                     bool(b.get("is_error")))  # fmt: skip
    for m in messages:
        if m["role"] == "user" and isinstance(m.get("content"), str) and task is None:
            task = m["content"]
        if m["role"] != "assistant":
            continue
        step = {"thinking": "", "text": "", "calls": []}
        for b in m.get("content") or []:
            if b.get("type") == "thinking":
                step["thinking"] += b.get("thinking") or ""
            elif b.get("type") == "text":
                step["text"] += b.get("text") or ""
            elif b.get("type") == "tool_use":
                res, err = results.get(b.get("id"), (None, False))
                step["calls"].append({"name": b.get("name"), "input": b.get("input"), "result": res, "error": err})
        steps.append(step)
    return {"state": reading_of(folder), "reading": load(folder / "reading.json"), "task": task, "steps": steps}


def agents_of(folder):
    """{name: conversation file} of a saved run."""
    if (folder / "agents").is_dir():
        return {d.name: d / "conversation.json" for d in sorted((folder / "agents").iterdir())
                if (d / "conversation.json").exists()}  # fmt: skip
    return {"agent": folder / "conversation.json"} if (folder / "conversation.json").exists() else {}


def conversation_events(a, messages, n=0, first=True):
    """A conversation as the page's events, as a live run would have sent them (deltas whole). `n`: the responses
    before it; `first`: whether its first user message is the agent's first message."""
    from streamed import shown

    ev = []
    for m in messages:
        role, content = m["role"], m["content"]
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]
        if role == "assistant":
            n += 1
            ev.append({"a": a, "k": "response", "n": n})
            for b in blocks:
                if b.get("type") == "thinking" and b.get("thinking"):
                    ev.append({"a": a, "k": "think", "text": b["thinking"]})
                elif b.get("type") == "text" and b.get("text"):
                    ev.append({"a": a, "k": "say", "text": b["text"]})
                elif b.get("type") == "tool_use":
                    inp = b.get("input") if isinstance(b.get("input"), dict) else {}
                    ev.append({"a": a, "k": "call", "id": b["id"], "name": b["name"]})
                    ev.append({"a": a, "k": "called", "id": b["id"], "call_id": b["id"], "name": b["name"],
                               "code": shown(b["name"], inp)})  # fmt: skip
            continue
        for b in blocks:
            if b.get("type") == "tool_result":
                out = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"])
                ev.append({"a": a, "k": "result", "call_id": b["tool_use_id"], "out": out, "error": bool(b.get("is_error"))})
            elif b.get("type") == "text" and b.get("text"):
                ev.append({"a": a, "k": "told", "text": b["text"], "first": first and role == "user"})
                first = False
            elif b.get("type") == "tool_addition":
                ev.append({"a": a, "k": "note", "text": f"tool added: {b.get('tool', {}).get('name')}"})
    return ev


def agent_events(a, path):
    """An agent's whole trajectory as the page's events: its conversation.json, after the conversations it had before
    each compaction (conversation.<i>.json, see COMPACT_AT). A later part begins with the first message, the handoff
    and the earlier part's last responses: only the handoff and what is new are shown again."""
    parts = sorted(path.parent.glob("conversation.*.json"), key=lambda p: int(p.stem.split(".")[1]))
    ev, n, prev = [], 0, None
    for part in [*parts, path]:
        messages = json.loads(part.read_text())["messages"]
        if prev is None:
            shown = messages
        else:
            turns = [i for i, m in enumerate(prev) if m["role"] == "assistant"]
            tail = len(prev) - turns[-COMPACT_KEEP] if len(turns) >= COMPACT_KEEP else 0
            tail = tail if messages[2:2 + tail] == prev[len(prev) - tail:] else 0
            shown = [messages[1], *messages[2 + tail:]]
        ev += conversation_events(a, shown, n, first=prev is None)
        n += sum(m["role"] == "assistant" for m in shown)
        if part != path:
            ev.append({"a": a, "k": "note", "text": f"compaction {part.stem.split('.')[1]}"})
        prev = messages
    return ev


def replay(key):
    """A saved run as the page's events: start, its Slack messages, each agent's conversation, end."""
    folder = run_folder(key)
    if folder is None:
        return None
    convs = agents_of(folder)
    summary = json.loads((folder / "summary.json").read_text()) if (folder / "summary.json").exists() else {}
    settings = json.loads((folder / "settings.json").read_text()) if (folder / "settings.json").exists() else {}
    ev = [{"k": "start", "folder": str(folder.relative_to(ROOT)), "agents": list(convs), "channel": CHANNEL,
           "budget": settings.get("budget", 0)}]  # fmt: skip
    if (folder / "slack.jsonl").exists():
        ev += [{"k": "slack", **json.loads(l)} for l in (folder / "slack.jsonl").read_text().splitlines() if l.strip()]
    for a, path in convs.items():
        ev += agent_events(a, path)
        info = summary.get("agents", {}).get(a, {})
        ev.append({"a": a, "k": "state", "state": "done" if info.get("state") != "idle" else "idle", "why": "",
                   "n": info.get("responses", 0), "cost": info.get("cost", 0)})  # fmt: skip
        ev.append({"a": a, "k": "cost", "n": info.get("responses", 0), "cost": info.get("cost", 0),
                   "total": summary.get("cost", 0)})  # fmt: skip
    reason = summary.get("reason") or next((r["reason"] for r in saved_runs() if r["key"] == key), None) or "saved"
    cost_ = summary.get("cost") or next((r["cost"] for r in saved_runs() if r["key"] == key), None) or 0
    ev.append({"k": "end", "reason": reason, "cost": cost_ or 0})
    return ev


def info(key):
    """A saved run's prompts and settings: {system, prompt, settings, summary}."""
    folder = run_folder(key)
    if folder is None:
        return None
    text = lambda n: (folder / n).read_text() if (folder / n).exists() else None
    load = lambda n: json.loads((folder / n).read_text()) if (folder / n).exists() else None
    return {"system": text("system.txt"), "prompt": text("prompt.txt"), "settings": load("settings.json"),
            "summary": load("summary.json"), "reading": load("reading.json")}  # fmt: skip


def files(folder):
    """The files of a run the page can show: everything agents wrote (the workspace, each agent's folder, a
    playground run's scratch/), Sage's caches (.home) and the link to the workspace left out. [{path, size, mtime}]."""
    found = []
    for top in ("workspace", "agents", "scratch"):
        base = folder / top
        if base.is_dir():
            found += [p for p in base.rglob("*") if p.is_file() and not p.is_symlink() and ".home" not in p.parts
                      and "workspace" not in p.relative_to(base).parts[1:2]
                      and not (p.name.startswith("conversation.") and p.suffix == ".json")]
    return [{"path": str(p.relative_to(folder)), "size": p.stat().st_size, "mtime": p.stat().st_mtime} for p in found]


def read(folder, rel):
    """A file `files` lists, as text (the first FILE_CHARS), or None."""
    if rel not in {f["path"] for f in files(folder)}:
        return None
    path = folder / rel
    if path.suffix in (".pkl", ".npy", ".npz", ".sobj", ".db"):
        return f"(binary, {path.stat().st_size:,} bytes)"
    text = path.read_bytes()[: FILE_CHARS * 4].decode("utf-8", "replace")
    return text if len(text) <= FILE_CHARS else text[:FILE_CHARS] + f"\n... [cut at {FILE_CHARS:,} characters]"
