"""A very simple harness for an agent who works in a Python file (Arm.scratchpad).

The agent has one conversation, which carries on from step to step, and three tools:

    write_file(content)       the file becomes `content`
    edit_file(old, new)       the one place where `old` stands in the file becomes `new`
    submit()                  the agent is done: it hands in the answer it holds

A step is one reply from the model: a thought, then tool calls, which are carried out in order. Whenever a step
changes the file, Python runs it (mathswarm/python.py: in a sandbox, the code being a model's) and what it
printed is what the tool says back, so no step is spent asking for a run and no change goes unchecked.

The file says its own answer: the last line it prints that starts `ANSWER:`. The answer an agent holds is the
last one a run without errors printed, so it is always something a file of its own computed and anyone can run
again, and an agent that runs out of steps still holds one. `submit` only says that the agent is done.

What a tool says back never depends on the known answer, which this module is never given. It says what the
file did and what the file is like (whether anything in it checks the answer it prints), in the same words
whether that answer is right or wrong.

The calls are in the model's own format: `TOOLS` goes to its chat template (through ../swarm_engine), and the
template says how a call is written. For Qwen3.5 that is

    <tool_call>
    <function=edit_file>
    <parameter=old>
    print(f(3))
    </parameter>
    <parameter=new>
    print(f(4))
    </parameter>
    </function>
    </tool_call>

with every value as plain text, so code needs no escaping. `Desk` is one agent's file; it needs no model, and
is handed whatever runs a file. `Workshop` in mathswarm/swarm.py seats a swarm at desks.
"""
from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Callable

from .python import FILE, TIMEOUT, Ran
from .python import answered as answered

LINES = 300               # how long a file may be: a longer one is not written (agents write 12 to 15 tokens a line,
                          # so a file of this length fits in the 5,760 tokens of `Arm.desk`, 19.2 a line).
                          # An arm may ask for another length (`Arm.lines`), and then needs the room for it (`max_tokens`).
                          # It was 80, with 1,536 tokens, until 2026-10-12: every run before that is of 80 lines but
                          # two of 200 (`hard_set/steps_20_lines_200`, `apex_shortlist/trial`), and until then a file
                          # that was too long was run all the same

SYSTEM = f"""You are solving a math problem by writing a Python file, {FILE}. Python runs the file every time you \
change it and you are shown what it printed. So let Python do the computing and the checking, and use your own \
thinking to decide what the file should do next.

- Each reply is one step: think briefly, then call a tool.
- Keep the file short, {{lines}} lines at most: a few comment lines at the top for the approach, then code that \
computes each step. Do not copy the problem into the file.
- When the code has worked the answer out, end the file with `print("ANSWER:", value)`. The last `ANSWER:` line \
that a run without errors printed is the answer you hold.
- When a run goes wrong, find out why before you change course: print the values involved, or try the piece on \
a small case you can check by hand.
- Once the file prints an answer and checks it (an `assert` of something the problem states, a second method, a \
small case), call submit. Test a doubt by adding to the file, not by working it out again in your head. Do not \
keep polishing a file that is done.

Python is {sys.version_info.major}.{sys.version_info.minor} with sympy and numpy, and a run is stopped after \
{TIMEOUT} seconds. You have at most {{steps}} steps."""

# What stands for the harness in a run's settings (Arm.describe): a run is not carried on under another harness
# than the one it began with. It is this file and the one that runs an agent's Python.
VERSION = hashlib.sha256(Path(__file__).read_bytes() + Path(__file__).with_name("python.py").read_bytes()).hexdigest()[:12]


def system(steps: int, lines: int = LINES) -> str:
    return SYSTEM.replace("{steps}", str(steps)).replace("{lines}", str(lines))


def tool(name: str, description: str, **parameters: str) -> dict:
    return {"type": "function", "function": {"name": name, "description": description, "parameters": {
        "type": "object", "properties": {key: {"type": "string", "description": about} for key, about in parameters.items()},
        "required": list(parameters)}}}


@lru_cache(maxsize=None)
def tools(lines: int = LINES) -> tuple[dict, ...]:
    """The three tools, as an agent whose file should stay within `lines` lines is told of them."""
    return (
        tool("write_file", f"Create {FILE}, or replace the whole of it. Python then runs it and you are shown what it printed.",
             content=f"The whole file: {lines} lines at most."),
        tool("edit_file", f"Change one place in {FILE}: the lines `old` become `new`. Python then runs the file and you are "
             "shown what it printed.", old="The lines to replace, copied from the file. A few are enough, if they stand in "
             "it only once.", new="The lines to put in their place."),
        tool("submit", "Hand in the answer you hold, and end your work."),
    )


TOOLS = tools()
NAMES = [t["function"]["name"] for t in TOOLS]

SHOWN = 2400              # how much of what a run printed and said an agent is shown, in characters
LISTED = 80               # how many lines of its file an agent is shown when an edit did not find its place: all of a
                          # file that is no longer, and of a longer one the part nearest to what was meant
NEAR = 0.85               # an `old` that is not in the file word for word is found where every line of it is this
                          # like the file's: a line miscopied is, a line of an earlier version of the file is not
NO_CALL = f"No tool call could be read in your reply. Reply with a call to one of the tools: {', '.join(NAMES)}."
NO_FILE = "There is no file yet: write_file creates it."
CUT_OFF = "Your reply ran into its length limit before this call was complete, so it was not carried out, and the step is used up."
CUT_FILE = ("Your reply ran into its length limit {lines} lines into the file, so nothing was written, and the step is "
            "used up.{prose} Write a file of at most {most} lines.")
TOO_LONG = ("That file is {lines} lines and a file may be {most} at most, so it was not written, and the step is used "
            "up.{prose} Write a file of at most {most} lines.")
TOO_LONG_EDIT = ("That edit would make the file {lines} lines and a file may be {most} at most, so nothing was changed, "
                 "and the step is used up.")
CUT_PROSE = " {prose} of those lines were comments: do the reasoning in your thinking, and put only the code in the file."
NO_ANSWER = "It printed no `ANSWER:` line, so this run gives you no answer."
BARE = 'The file\'s line `{line}` is not a print, so Python goes past it: write print("ANSWER:", value).'
NOT_ONE = "`ANSWER: {text}` is not an answer of the kind the problem asks for, so this run gives you no answer."
KEPT = "You still hold {answer}, from an earlier run."
HELD = "Your answer now stands at {answer}."
STILL = "Your answer still stands at {answer}."
MOVED = "Your answer was {old} and now stands at {answer}. Be sure which of them is right, and why."
CHECKED = " The file's {asserts} held: if a wrong answer would have failed there, call submit to hand it in."
UNCHECKED = (" Nothing in the file checks it: add an `assert` that would fail if it were wrong (of something the "
             "problem states, or that a different method gives the same value), or call submit if you are sure of it.")
AGAIN = (" Nothing in this file checks it. Two files that reach an answer by different methods are a check: if that "
         "is what you have, call submit. If not, add an `assert` that would fail if the answer were wrong.")
TYPED = " But the file prints it as text you typed in, and no code computes it: have the code compute the value it prints."
SAME = "That is the file as it already stands, so nothing changed and Python did not run it again."
NOTHING = 'Not submitted: you hold no answer. End the file with print("ANSWER:", value), so that a run prints it, and then submit.'

_CALL = re.compile(r"<function=([\w.-]+)>(.*?)(</function>|\Z)", re.S)
_PARAMETER = re.compile(r"<parameter=([\w.-]+)>\n?(.*?)(?:\n?</parameter>|\Z)", re.S)
_BEFORE = re.compile(r"<tool_call>|<function=")
_ASSERT = re.compile(r"^[ \t]*assert\b", re.M)
_BARE = re.compile(r"^[ \t]*(ANSWER[ \t]*:[ \t]*\S.*?)[ \t]*$", re.M)        # a line of the file that is `ANSWER: ...` and no print
_TYPED = re.compile(r"""print\(\s*f?(["'])(?:\\[nrt]|\s)*ANSWER\s*[:=](?:[^{"']*\d[^{"']*\1|\s*\1\s*,\s*-?\d[\d./]*)\s*\)""", re.I)   # print("ANSWER: 2"), print("\nANSWER:", 2)


def calls(text: str) -> list[tuple[str, dict[str, str], bool]]:
    """The tool calls in a reply, in order: (name, arguments, whether the call was written to its end). Only the
    last can be unfinished: a reply cut short keeps what it had of it."""
    return [(name, dict(_PARAMETER.findall(body)), bool(end)) for name, body, end in _CALL.findall(text)]


def said(text: str) -> str:
    """What a reply says in words, before its first tool call."""
    return _BEFORE.split(text, maxsplit=1)[0].strip()


def finished(text: str) -> str:
    """A reply without its last tool call, if that call was not written to its end."""
    last = None
    for last in _CALL.finditer(text):
        pass
    return text if last is None or last.group(3) else text[:last.start()].removesuffix("<tool_call>\n").rstrip()


def written(name: str, **arguments: str) -> str:
    """A tool call as Qwen3.5 writes it (for stand-ins and tests)."""
    inside = "".join(f"<parameter={key}>\n{value}\n</parameter>\n" for key, value in arguments.items())
    return f"<tool_call>\n<function={name}>\n{inside}</function>\n</tool_call>"


def prose(code: str) -> int:
    """How many lines of a file are comments or docstrings."""
    count, inside = 0, False
    for line in (line.strip() for line in code.split("\n")):
        quotes = line.count('"""') + line.count("'''")
        count += bool(line) and (inside or line.startswith("#") or quotes > 0)
        inside ^= quotes % 2 == 1
    return count


def wordy(content: str, lines: int) -> str:
    """What a file that was not written is told of its comments, if over a third of it was comments."""
    comments = prose(content)
    return CUT_PROSE.format(prose=comments) if comments > lines // 3 else ""


def numbered(lines: list[str], first: int = 1) -> str:
    return "\n".join(f"{first + i:>3}  {line}" for i, line in enumerate(lines))


def span(first: int, last: int) -> str:
    return f"line {first}" if last <= first else f"lines {first} to {last}"


def like(mine: str, theirs: str) -> bool:
    """Whether a line of `old` is a line of the file, miscopied at most: the same margin, and nearly the same text
    (the text alone: a deep margin in common does not make two lines alike)."""
    return mine == theirs or (indent(mine) == indent(theirs)
                              and SequenceMatcher(None, mine.strip(), theirs.strip(), autojunk=False).ratio() >= NEAR)


def places(lines: list[str], old: list[str]) -> list[int]:
    """Where in a file `old` stands but for the blank space at the ends of lines; if nowhere, where every line
    of it is like the file's line."""
    a, b = [line.rstrip() for line in lines], [line.rstrip() for line in old]
    spots = range(len(a) - len(b) + 1)
    return [at for at in spots if a[at:at + len(b)] == b] or [at for at in spots if all(map(like, b, a[at:at + len(b)]))]


def nearest(lines: list[str], old: list[str]) -> int:
    """The line of a file at which most lines of `old` stand: where to look when it is not found."""
    a, b = [line.strip() for line in lines], [line.strip() for line in old]
    return max(range(max(len(a) - len(b) + 1, 1)), key=lambda at: sum(x == y for x, y in zip(a[at:at + len(b)], b)))


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


@dataclass
class Desk:
    """One agent's file and what it has done with it. `run` runs a file and says what happened (a `Ran`); `read`
    turns what a run printed after `ANSWER:` into an answer, or None if it is not one."""
    run: Callable[[str], Ran]
    read: Callable[[str], str | None] = lambda text: text.strip() or None
    file: str | None = None
    ran: Ran | None = None                   # what Python made of the file as it stands
    answer: str | None = None                # the answer the agent holds: the last one a run without errors printed
    done: bool = False                       # it has submitted
    did: Counter = field(default_factory=Counter)
    lines: int = LINES                       # how long its file may be: a longer one is not written, and it is told so

    def step(self, text: str, cut: bool = False) -> list[list]:
        """Carry out the tool calls of one reply, in order: [name, what the tool said] for each. Python runs the
        file once the step has changed it: after its last change, or before a `submit` that follows one. `cut`
        says the reply ran into its length limit: a last call that was not written to its end is not carried
        out. Nothing is carried out after a submit that was accepted. A reply without a call comes back as one
        entry with no name."""
        self.did["steps"] += 1
        found = calls(text)
        if not found:
            self.did["no_call"] += 1
            return [[None, NO_CALL]]
        out, changed = [], None              # `changed`: what the last call to change the file said, until Python has run it
        for name, arguments, whole in found:
            if self.done:
                break
            if cut and not whole:
                self.did["cut_off"] += 1
                content = arguments.get("content", "") if name == "write_file" else ""
                lines = content.count("\n") + 1
                out.append([name, CUT_FILE.format(lines=lines, prose=wordy(content, lines), most=self.lines) if content else CUT_OFF])
                break
            if name == "submit" and changed is not None:
                changed[1], changed = f"{changed[1]}\n{self.python()}", None
            before = self.file
            out.append([name, self.use(name, arguments)])
            if self.file != before:
                changed = out[-1]
        if changed is not None:
            changed[1] = f"{changed[1]}\n{self.python()}"
        return out

    def python(self) -> str:
        """Run the file as it stands, and say what an agent is told of it: what the run printed, and where it
        leaves the answer the agent holds."""
        self.ran = ran = self.run(self.file)
        self.did["runs"] += 1
        self.did["runs_clean"] += ran.ok
        told, kept = ran.told(SHOWN), [KEPT.format(answer=self.answer)] if self.answer is not None else []
        if not ran.ok:
            return "\n".join([told, *kept])
        text = ran.answer
        answer = None if text is None else self.read(text)
        if answer is None:
            bare = _BARE.search(self.file) if text is None else None
            none = NO_ANSWER if text is None else NOT_ONE.format(text=text)
            return f"{told}\n" + " ".join([none, *([BARE.format(line=bare.group(1))] if bare else []), *kept])
        old, self.answer = self.answer, answer
        asserts, stands = len(_ASSERT.findall(self.file)), HELD if old is None else STILL if old == answer else MOVED
        checks = (TYPED if _TYPED.search(self.file) else CHECKED.format(asserts="assert" if asserts == 1 else f"{asserts} asserts")
                  if asserts else AGAIN if stands is STILL else UNCHECKED)
        return f"{told}\n{stands.format(answer=answer, old=old)}{checks}"

    def use(self, name: str, arguments: dict[str, str]) -> str:
        self.did[name if name in NAMES else "unknown_tool"] += 1
        if name == "write_file":
            if not arguments.get("content", "").strip():
                return "write_file needs `content`: the whole file. Nothing was written."
            return self.write(arguments["content"])
        if name == "edit_file":
            old, new = arguments.get("old", ""), arguments.get("new", "")
            if self.file is None:
                if not new.strip():
                    return NO_FILE
                wrote = self.write(new)
                return wrote + " There was no file yet, so `new` became the file." if self.file is not None else wrote
            return self.edit(old, new)
        if name == "submit":
            if self.answer is None:
                return NOTHING
            self.done = True
            return f"Submitted: {self.answer}."
        return (f"There is no tool `{name}`. The tools are {', '.join(NAMES[:-1])} and {NAMES[-1]}. Python runs the "
                "file by itself whenever you change it.")

    def write(self, content: str) -> str:
        if content == self.file:
            return SAME
        lines = len(content.splitlines())
        if lines > self.lines:               # a file that is too long is not written, and so not run
            self.did["too_long"] += 1
            return TOO_LONG.format(lines=lines, most=self.lines, prose=wordy(content, lines))
        self.file = content
        return f"Wrote {FILE} ({lines} line{'s' * (lines != 1)})."

    def too_long(self, content: str) -> str | None:
        """What an edit is told if it would leave the file longer than a file may be; None if it would not."""
        lines = len(content.splitlines())
        if lines <= self.lines:
            return None
        self.did["too_long"] += 1
        return TOO_LONG_EDIT.format(lines=lines, most=self.lines)

    def edit(self, old: str, new: str) -> str:
        """Put `new` where `old` stands. `old` is found if it stands in the file once, word for word; or if
        there is one place in the file where every line of it is like the file's line (`like`: a line miscopied
        does not lose an edit, and lines of an earlier version of the file do not find a place they do not
        belong). Otherwise nothing is changed, and the agent is shown the lines it most likely meant."""
        if not old.strip():
            self.did["edit_failed"] += 1
            return "edit_file needs `old`: the lines to replace, copied from the file. Nothing was changed."
        stands = self.file.count(old)
        if stands == 1:
            if old == new:
                return SAME
            at = self.file.index(old)
            first = self.file.count("\n", 0, at) + 1
            edited = self.file[:at] + new + self.file[at + len(old):]
            if (refused := self.too_long(edited)):
                return refused
            self.file = edited
            return f"Edited {span(first, first + new.count(chr(10)))}."
        if stands > 1:
            self.did["edit_failed"] += 1
            return (f"`old` stands in {stands} places in the file, so nothing was changed. Include more of the "
                    "lines around the one you mean.")
        lines, wanted = self.file.split("\n"), old.strip("\n").split("\n")
        found, put = places(lines, wanted), new.strip("\n").split("\n") if new.strip() else []
        if len(found) == 1 and lines[found[0]:found[0] + len(wanted)] != put:
            first = found[0]
            edited = "\n".join(lines[:first] + put + lines[first + len(wanted):])
            if (refused := self.too_long(edited)):
                return refused
            self.file = edited
            self.did["edit_near"] += 1
            now = f"They now read:\n{numbered(put[:min(self.lines, LISTED) // 3], first + 1)}" if put else "They were taken out."
            return (f"Edited {span(first + 1, first + max(len(put), 1))}. `old` was not in the file word for word: the "
                    f"{'line' if len(wanted) == 1 else f'{len(wanted)} lines'} nearest to it {'was' if len(wanted) == 1 else 'were'} replaced. {now}")
        if len(found) == 1:
            return SAME
        self.did["edit_failed"] += 1
        first = nearest(lines, wanted)
        listed = min(self.lines, LISTED)
        low = 0 if len(lines) <= listed else max(min(first - (listed - len(wanted)) // 2, len(lines) - listed), 0)
        high = min(low + listed, len(lines))                    # a long file: the part nearest to what was meant
        part = "The file reads:" if high - low == len(lines) else f"Lines {low + 1} to {high} of its {len(lines)} read:"
        return f"`old` is not in the file, so nothing was changed. {part}\n{numbered(lines[low:high], low + 1)}"


def steps_left(now: int, last: int, answer: str | None) -> str:
    """The line under a step's last result once an agent's steps are running out: how many are left, and what
    to do with them."""
    left = last - now
    if left > 3 or left <= 0:
        return ""
    if left == 1:                            # said before the last step is taken: nothing follows it
        if answer is None:
            return ('(Your next step is your last, and you hold no answer. If the file has computed one, end it with '
                    'print("ANSWER:", value) now: the answer you hold when that step is over is the one you hand in.)')
        return f"(Your next step is your last. Your answer stands at {answer}: call submit now to hand it in.)"
    if answer is None:
        return f'(You have {left} steps left and hold no answer. If the file has computed one, end it with print("ANSWER:", value) now.)'
    return f"(You have {left} steps left. Your answer stands at {answer}: submit it unless a check fails.)"
