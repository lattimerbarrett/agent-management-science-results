"""Looks: the contact between agents who work at desks (mathswarm/harness.py).

Every agent of a problem is at work at once, each at its own pace, and nobody stops for anybody. A look is one
agent reading another's file:

    1. After one of its steps, agent A is picked to read the file of agent B.
    2. A is shown B's file and what Python printed when it ran, and says what it makes of the file. That reply
       is an extra turn, not one of A's steps, and A's own file is not touched by it. If it says nothing, it
       is asked once more.
    3. B has gone on working meanwhile. After its next step it is shown A's words, and goes on.

An agent at a desk answers with a tool call and next to never in plain words (4 replies in 782 had any, in
`desk_work`), and in the pilot of this the two agents who were asked to "reply in words only" each wrote their
own file instead. So what a reader says goes in a call too: for the one reply of a look it is offered one more
function, `say(words)`, in the look itself. The functions an agent is told of at the start stay the three of
the harness, so an agent under an arm with looks is still the baseline's agent until its first look. Offered
`say`, one reader in eight of a second pilot used it and the others went on changing their own files, having
read the other's: so a reader that says nothing is asked once more, in two sentences, before it goes on.

Who reads whose file, and after which step, is a random graph drawn before anybody starts (`RandomLooks.plan`),
from the problem and the run's seed. So it is the same graph whenever the run is played, and the same in the arm
that is its control: under `RandomLooks(at="own")` an agent reads its own file at exactly the moments at which
it would have read another's, and writes about that. The two arms differ in whose file is read and in nothing
else, so what contact adds is not confused with what an extra turn of reading adds.

The swarm's clock is the step count, not the wall clock: A, after its step s, is shown B's file as it stood
after B's step s (or as B left it, if B stopped earlier), and B reads A's words after its step s + 1. A waits
for B only if B has not got that far, and nobody else waits. What an agent is shown therefore does not depend
on which agent the machine happened to serve first, or on which replies were recalled from the cache instead of
written: a run that is stopped carries on where it was, and an agent is the same agent as in the control until
the first look that touches it. `Workshop` in mathswarm/swarm.py keeps that clock.

What an agent is told at a look is here, and nothing in it comes from the known answer: a file and what Python
printed when it ran, in the same words whatever the file prints, and another agent's words, marked as that
agent's own.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path

import numpy as np

from . import harness
from .python import Ran, middle

# What stands for this file in a run's settings (Arm.describe): a run is not carried on under other rules or
# other words than it began with.
VERSION = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]

LINES = harness.LINES     # how much of a file a reader is shown: all of a file that is as long as it may be (300 lines
                          # since 2026-10-13; it was 120 while a file was to stay under 80)
HEAD = 2 * LINES // 3     # of a longer one (an arm that gives its files more room), its first lines, and the rest of
                          # the room for its last
PRINTED = 2400            # how much of what the file printed and Python said, in characters
SAID = 1200               # how much of a reader's words is passed on, in characters
ASKS = 2                  # how often a reader is asked what it makes of a file: once more, if it said nothing
DRAW = 1001               # sets these draws apart from any other made from the same problem and seed


def chance(*parts: int) -> np.random.Generator:
    """Randomness fixed by what it is for (a problem, a run, an agent, a step ...)."""
    return np.random.default_rng([int(p) for p in parts])


def describe(rule) -> dict | str | None:
    """A rule as it is written in a run's settings."""
    if rule is None:
        return None
    return {"rule": type(rule).__name__, **asdict(rule)} if is_dataclass(rule) else repr(rule)


@dataclass(frozen=True)
class RandomLooks:
    """After each of its steps, an agent is picked with probability `p` to read one other agent's file, drawn
    at random among the others. `at="own"` is the control: the same agents are picked at the same steps, and
    each reads its own file."""
    p: float = 0.25
    first: int = 2            # nobody is picked before it has taken this many steps: there is little to read
    at: str = "others"        # whose file: "others", or "own"

    def __post_init__(self):
        if not 0 <= self.p <= 1 or self.first < 1 or self.at not in ("others", "own"):
            raise ValueError('RandomLooks: p is between 0 and 1, first is 1 or more, at is "others" or "own"')

    def plan(self, problem: int, run: int, agents: int, steps: int) -> dict[tuple[int, int], int]:
        """Every look: {(reader, after which of its steps): whose file}. An agent's draws are its own, so it is
        picked at the same steps however many others there are, and whichever file `at` has it read. Nobody
        is picked after its last step: it would have nothing to go on with."""
        out = {}
        for reader in range(agents):
            for step in range(self.first, steps):
                rng = chance(problem, run, DRAW, reader, step)
                picked, other = rng.random() < self.p, int(rng.integers(max(agents - 1, 1)))
                if picked and agents > 1:
                    out[reader, step] = reader if self.at == "own" else other + (other >= reader)
        return out


# ---------------------------------------------------------------- what an agent is told

SAY = harness.tool("say", "Say what you make of the file you were just shown.",
                   words="A few sentences: what you checked in the file and what you found.")
BEFORE = "Before your next step, read {whose} and say what you make of it."
OFFER = ("This is not one of your {steps} steps. To answer it you have one more function:\n\n<tools>\n"
         + json.dumps(SAY) + "\n</tools>\n\nA call to " + ", ".join(harness.NAMES[:-1]) + " or " + harness.NAMES[-1]
         + " in your answer is not carried out.")
OTHERS = "The other agent has the same problem. Its file reads:"
OWN = "Your file reads:"
FOUND = "what you checked in {it} and what you found (a mistake: which line, and why; a check it lacks; or the part you can confirm)"
STAYS = "Leave your own file as it is in this reply: you go on with it in your next."
NOW = "Reply now with one call to say."
TO_IT = "Your words are for that agent: a few sentences on " + FOUND.format(it="its file") + ". " + STAYS + " " + NOW
TO_NOBODY = ("What you say will not reach that agent: it has stopped work, or will have before it could read it. Say all "
             "the same, in a few sentences, " + FOUND.format(it="its file") + ". " + STAYS + " " + NOW)
TO_SELF = "Say, in a few sentences, " + FOUND.format(it="the file") + ". Leave the file as it is in this reply: you go on with it in your next. " + NOW
AGAIN = "You have said nothing yet about {whose}. This reply is not one of your steps either. " + NOW      # asked once more
LEFT_OUT = "     … ({lines} lines are left out here) …"
HEARD = ("Another agent working on the same problem read your file as it was before your last step, and said this about "
         "it:\n\n{said}\n\n(These are that agent's own words. Nothing has checked them.)")
NOT_KEPT = ("What you called in reply to that ({tools}) was not carried out, and is not kept: call it again now if you "
            "still mean to.")
GO_ON = "Now go on with your own file."


_TAG = re.compile(r"</?parameter[^>\n]*>")      # what is left of a parameter that was opened or closed and not both
_JSON_CALL = re.compile(r"<tool_call>\s*(\{.*?\})\s*(?:</tool_call>|\Z)", re.S)      # a call written as JSON
_WHOLE_CALL = re.compile(r"(?:<tool_call>\s*)?<function=([\w.-]+)>.*?(?:</function>\s*(?:</tool_call>)?|\Z)", re.S)


def numbered(code: str) -> str:
    """A file as a reader is shown it, each line under its number; a long one without its middle."""
    lines = code.split("\n")
    shown = [f"{n:>3}  {line}" for n, line in enumerate(lines, 1)]
    if len(lines) <= LINES:
        return "\n".join(shown)
    return "\n".join(shown[:HEAD] + [LEFT_OUT.format(lines=len(lines) - LINES)] + shown[len(lines) - (LINES - HEAD):])


def ran(what: Ran) -> str:
    """What Python made of a file, as its reader is told: what it printed and said, and no advice (the advice
    a run gives is for the agent whose file it is)."""
    error = middle(what.error, PRINTED // 2)
    printed = middle(what.output.rstrip("\n"), PRINTED - len(error))
    before = f"\nBefore that it printed:\n{printed}" if printed else "\nIt had printed nothing."
    if what.status == "ok":
        return (f"Python ran it with no errors. It printed:\n{printed}" if printed else
                "Python ran it with no errors, and it printed nothing.") + (f"\nIt also warned:\n{error}" if error else "")
    if what.status == "error":
        return f"Python ran it, and it stopped with an error:\n{error}" + before
    if what.status in ("timeout", "memory"):
        return f"Python ran it, and it was stopped: {error}." + before
    return f"Python could not be run on it: {error}."


def shows(file: str, what: Ran | None, steps: int, own: bool = False, unread: bool = False) -> str:
    """What a reader is told at a look: what is asked of it and the function it answers with, the file, what
    Python made of the file, and what is asked once more. `own`: the file is its own (the control). `unread`:
    the agent whose file it is will not be shown what is said (it has stopped work, or has one step left)."""
    lead = BEFORE.format(whose="your own file again" if own else "another agent's file") + " " + OFFER.replace("{steps}", str(steps))
    ask = TO_SELF if own else TO_NOBODY if unread else TO_IT
    told = ran(what) if what is not None else "Python has not run it."
    return f"{lead}\n\n{OWN if own else OTHERS}\n\n{numbered(file)}\n\n{told}\n\n{ask}"


def said(reply: str) -> tuple[str, list[str]]:
    """What a reader said in its reply, and the tools it called that are not carried out at a look. Its words are
    those of its calls to `say`, read however the call is written: with its parameter named `words` or
    otherwise, with none named at all (in the trial the one reader who called it wrote its words straight into
    the call, and they were lost), or as JSON. A reply with no call at all is its words as it stands. What a
    reply says before a call to one of its own tools is about that call, and is nobody's words about a file."""
    say, words, others = SAY["function"]["name"], [], []
    for name, body, _ in harness._CALL.findall(reply):
        if name != say:
            others.append(name)
        elif (arguments := dict(harness._PARAMETER.findall(body))):
            words.append(arguments.get("words") or next(iter(arguments.values())))
        else:
            words.append(_TAG.sub("", body))
    for body in _JSON_CALL.findall(reply):                              # {"name": "say", "arguments": {"words": "..."}}
        try:
            call = json.loads(body)
            name, arguments = call.get("name"), call.get("arguments") or {}
        except (ValueError, AttributeError):
            continue
        if name == say and isinstance(arguments, dict):
            words.append(str(arguments.get("words") or next(iter(arguments.values()), "")))
        elif isinstance(name, str):
            others.append(name)
    spoken = "\n\n".join(word.strip() for word in words if word.strip())
    if not spoken and not others and not _JSON_CALL.search(reply):
        spoken = harness.said(reply) if harness._CALL.search(reply) else reply     # in plain words: before an empty `say`, or all of it
    return spoken.strip(), list(dict.fromkeys(others))


def kept(reply: str) -> str:
    """A reader's reply as it stays in its conversation: without the calls to its own tools, which were not carried
    out. Left in, they are what it works from next (in a pilot a reader then edited the file its refused edit
    would have made, and lost the step): the same reason a call that was cut off is not kept (`Arm.drafts`)."""
    say = SAY["function"]["name"]
    without = _WHOLE_CALL.sub(lambda call: call.group(0) if call.group(1) == say else "", reply)
    return re.sub(r"\n{3,}", "\n\n", without).strip()


def again(own: bool) -> str:
    """What a reader is told when its reply said nothing of the file: it is asked once more, in a few words."""
    return AGAIN.format(whose="your file" if own else "the other agent's file")


def heard(said: str) -> str:
    """What an agent is told when another has read its file: that agent's words, as its own. They are about the
    file as it was one step ago: the agent has taken a step since."""
    return HEARD.format(said=said)


def after(called: list[str]) -> str:
    """What a reader is told once it has replied. `called`: the tools it called in reply, which were not carried
    out and are not in its conversation. Nothing is said of where its words went: whether the other agent reads
    them is not known yet."""
    return " ".join([NOT_KEPT.format(tools=", ".join(called))] * bool(called) + [GO_ON])


def asks(text: str) -> bool:
    """Whether a message is a file an agent is asked to read."""
    return text.startswith(BEFORE.split("{")[0])


def tells(text: str) -> bool:
    """Whether a message is another agent's words about the reader's own file."""
    return text.startswith(HEARD.split("{")[0])
