"""What the baseline and the swarm are now, read off the code: `lab current`, and the table in CURRENT.md.

CURRENT.md is the one place that says which approach is the current one and what has been left behind. The
part of it that can be read off the code is written from here (`lab current --write`), between two marks, and
a test fails when the file and the code disagree: what agents are told and how they are set does not change
without that file being changed too.
"""
from __future__ import annotations

from . import harness, looks, python
from .paths import ROOT
from .swarm import VERSION as WORKSHOP
from .swarm import Arm
from .tables import markdown

FILE = ROOT / "CURRENT.md"
GPU_MODEL = "9B-bf16"     # what a run on a rented GPU plays unless it names another: the weights as Qwen released them
BEGIN, END = "<!-- lab current: begin (written by `uv run lab current --write`) -->", "<!-- lab current: end -->"


def drawn(sampling) -> str:
    return f"temperature {sampling.temperature:g}, presence penalty {sampling.presence_penalty:g}"


def table() -> str:
    """The settings that are current, each with where it is set."""
    from swarm_engine.vllm_server import VERSION as VLLM

    from .llm import identity
    desk, rule = Arm("desk"), looks.RandomLooks()
    rows = [
        ["baseline: an agent alone at its desk", f"`Arm(name)`: {desk.steps} steps; a step may think for {desk.thinking:,} tokens and "
         f"write {desk.max_tokens:,}; thoughts drawn at {drawn(desk.thought_sampling)}, replies at {drawn(desk.sampling)}; a reply "
         f"that was cut off is {'kept in' if desk.drafts else 'left out of'} the agent's conversation; nobody reads anybody",
         "mathswarm/swarm.py"],
        ["harness: what an agent is told and what its tools do", f"`{harness.VERSION}`: the tools {', '.join(harness.NAMES)}; a file of at "
         f"most {harness.LINES} lines; a run is stopped after {python.TIMEOUT} seconds", "mathswarm/harness.py, python.py"],
        ["swarm: agents read each other's files", f"`RandomLooks()`: after each of its steps from the {ordinal(rule.first)} on, an agent is "
         f"picked with probability {rule.p:g} to read one other agent's file, as it stood after as many steps, and to say what it "
         f"makes of it through a function, `{looks.SAY['function']['name']}`, that is offered for that reply (an extra turn; asked "
         f"{looks.ASKS - 1} more time{'s' * (looks.ASKS != 2)} if it says nothing; at most {looks.SAID:,} characters passed on); the "
         "other agent reads that after its next step", "mathswarm/looks.py, swarm.py"],
        ["control: the same extra turns, nobody read", '`RandomLooks(at="own")`: the same agents are picked at the same steps, and each '
         "reads its own file", "mathswarm/looks.py"],
        ["looks: the rules and the words of a look", f"`{looks.VERSION}`", "mathswarm/looks.py"],
        ["workshop: what an agent is shown and when, and what counts as its answer", f"`{WORKSHOP}`", "mathswarm/swarm.py, reading.py"],
        ["model", f"`{desk.model}`: {identity(desk.model)}", "../swarm_engine"],
        ["model on a rented GPU (`lab cloud run`)", f"`{GPU_MODEL}`: {identity(GPU_MODEL)}, served by vLLM {VLLM}",
         "../swarm_engine, mathswarm/cloud.py"],
    ]
    return markdown(["what", "now", "where it is set"], rows)


def ordinal(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def between(begin: str, end: str) -> str | None:
    """What CURRENT.md has between two marks; None if the file or its marks are missing."""
    text = FILE.read_text() if FILE.exists() else ""
    if begin not in text or end not in text:
        return None
    return text.split(begin, 1)[1].split(end, 1)[0].strip()


def put(begin: str, end: str, what: str) -> bool:
    """Put `what` into CURRENT.md between two marks. False, and nothing written, if it has no such marks."""
    text = FILE.read_text() if FILE.exists() else ""
    if begin not in text or end not in text:
        return False
    before, rest = text.split(begin, 1)
    FILE.write_text(f"{before}{begin}\n{what}\n{end}{rest.split(end, 1)[1]}")
    return True


def written() -> str | None:
    """The table as CURRENT.md has it; None if the file or its marks are missing."""
    return between(BEGIN, END)


def write() -> str:
    """Put the table into CURRENT.md, between its marks."""
    if not put(BEGIN, END, table()):
        raise SystemExit(f"{FILE.name} has no place for the table: it goes between the lines\n{BEGIN}\n{END}")
    return f"wrote the table into {FILE.name}"
