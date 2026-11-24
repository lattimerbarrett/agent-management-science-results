"""Reading text an agent wrote: the answer in a line its file printed, and words that are safe to show another agent.

    answer("m + n = 371", problem)        ->  "371" is read by the desk (mathswarm/swarm.py); this gives the value's text
    clean("print(1)<|im_end|>")           ->  "print(1)"

An answer is a value. What a file prints after `ANSWER:` is tidied to it: LaTeX wrapping and a full stop are
taken off, and words that stand for "no answer" are no answer. For a multiple choice problem the answer is the
letter of an option, or nothing. It is short: what is longer is cut off, but for a number written out in
digits, which is a value however long it is (the Apex Shortlist has known answers of 225, 301 and 606 digits).
"""
from __future__ import annotations

import re

from .problems import Problem

MAX_ANSWER_CHARS = 120    # an answer is a value
MAX_NUMBER_CHARS = 1000   # and a whole number, or a ratio of two, written out in digits may be this long

NO_ANSWER = ("none", "none yet", "not yet", "no answer", "no answer yet", "null", "n/a", "unknown", "?")   # said in place of an answer

# Text that the chat template would read as control tokens if one agent's words were put before another agent.
_CONTROL = re.compile(r"<\|[^|>\n]{0,40}\|>|</?think>|</?tool_call>|</?tool_response>")
_DIGITS = re.compile(r"[-+]?\d+(?:/\d+)?")      # 1048575, -3, 448/3: a number written out in digits
_LETTER = re.compile(r"(?:OPTION|ANSWER|CHOICE)?\s*[:\-]?\s*\(?([A-J])\)?(?![A-Z0-9])")   # B, (B), b. 3, Option B


def clean(text: str) -> str:
    """Text without anything the chat template would read as a control token. Taking one out can leave another
    behind (`</tool_<think>response>`), so it is gone over until nothing is left to take out."""
    while (cleaner := _CONTROL.sub("", text)) != text:
        text = cleaner
    return text


def cut(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def _boxed(text: str) -> str | None:
    """What is inside the last \\boxed{...}, braces matched."""
    start = text.rfind("\\boxed{")
    if start < 0:
        return None
    depth, begin = 0, start + len("\\boxed{")
    for at in range(begin, len(text)):
        if text[at] == "{":
            depth += 1
        elif text[at] == "}":
            if depth == 0:
                return text[begin:at]
            depth -= 1
    return None


def value(text: str) -> str | None:
    """An answer line tidied to the value it holds."""
    text = text.strip().strip("*`").strip()
    if (inside := _boxed(text)) is not None:
        text = inside
    for left, right in (("\\(", "\\)"), ("\\[", "\\]"), ("$$", "$$"), ("$", "$")):
        if text.startswith(left) and text.endswith(right) and len(text) > len(left) + len(right):
            text = text[len(left):-len(right)].strip()
    if len(text) > 1 and text.endswith(".") and not text.endswith(".."):
        text = text[:-1]
    text = " ".join(text.split())
    if not text or text.lower().strip("()[]<>") in NO_ANSWER:
        return None
    return cut(text, MAX_NUMBER_CHARS if _DIGITS.fullmatch(text) else MAX_ANSWER_CHARS)


def answer(text: str, problem: Problem) -> str | None:
    """What stands after `ANSWER:`, as an answer to `problem`: None if it is no answer or, for a multiple choice
    problem, names no option."""
    found = value(clean(text).split("\n", 1)[0])
    if found is not None and problem.letters:
        named = _LETTER.match(found.upper())
        found = named.group(1) if named and named.group(1) in problem.letters else None
    return found
