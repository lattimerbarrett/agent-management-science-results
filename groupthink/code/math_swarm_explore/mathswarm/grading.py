"""Is an answer to a benchmark problem right?

    right(problem, answer)      whether it is
    recorded(problem, answer)   the answer as the logs keep it: the problem's `truth` when it is right, otherwise
                                the answer in a tidy form, so that agents who gave the same wrong answer in
                                slightly different writing count as agreeing

How each kind of answer is checked, next to what the Self-Organizing Agent Teams paper says it used (App. D).
This is `src/grading.py` of ../swarm_experiment, unchanged but for one thing: an answer that is not equal to
the known one as it is written is read once more with Python's powers (`n**2`) written as LaTeX's (`n^{2}`),
because an answer here is what a Python file printed (`same_maths`). That can only make an answer right that
was not; no answer without `**` in it is checked otherwise than before.

    integer, latex   math-verify, the paper's checker: the two expressions have to be mathematically equal.
                     The paper checks HMMT with MathArena's own checker instead, which is not used here.
    float, lists     TheoremQA's own rule: within 4% of the known value (lists: the same numbers in any order).
                     The paper names math-verify for these too, but math-verify wants the digits to match, and
                     the known values are rounded and often in scientific notation, which it misreads.
    choice           the same letter, as in the paper
    text             BBEH's own matching rules (`bbeh_match`), as in the paper

Two wrong answers that mean the same but are written differently (\\frac{1}{3} and 0.333) are recorded as
different answers unless both are plain numbers.
"""
from __future__ import annotations

import math
import re
from functools import lru_cache

from math_verify import ExprExtractionConfig, LatexExtractionConfig, parse, verify

from .problems import Problem

TOLERANCE = 0.04   # TheoremQA: a number within 4% of the known value is right
# A number as people write one: 1.2, 1.2e-5, 1.2 \times 10^{-5}, 10^5, and any of those followed by a unit.
_NUMBER = re.compile(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)?"
                     r"\s*(?:(?:\\times|\\cdot|[×x*·])?\s*10\s*\^\s*\{?\s*([-+]?\d+)\s*\}?)?"
                     r"\s*(%|\\?[a-zA-Z°Ωμ][a-zA-Z°Ωμ\s/^·*\\{}()\-\d.]{0,24})?")


# ---- mathematics (math-verify)

@lru_cache(maxsize=4096)
def _maths(text: str) -> tuple:
    """`text` as math-verify reads it. A bare expression is read as LaTeX."""
    text = text.strip()
    if not any(mark in text for mark in ("$", "\\boxed", "\\(", "\\[")):
        text = f"${text}$"
    return tuple(parse(text, extraction_config=[LatexExtractionConfig(), ExprExtractionConfig()]))


def powers(text: str) -> str:
    """Python's powers as LaTeX writes them: `2**20 - 1` is `2^{20} - 1`, `(N + 1)**2*(4*N + 1)` is
    `(N + 1)^{2}*(4*N + 1)`, `30**(1/2)` is `30^{(1/2)}`. What is raised is left where it stands; the power is
    the number, the name or the bracket that follows, with its sign."""
    out, at = [], 0
    while (found := text.find("**", at)) >= 0:
        end = start = found + 2
        end += end < len(text) and text[end] in "+-"
        if end < len(text) and text[end] == "(":
            depth = 0
            for end in range(end, len(text)):
                depth += (text[end] == "(") - (text[end] == ")")
                if depth == 0:
                    break
            end += 1
        else:
            while end < len(text) and (text[end].isalnum() or text[end] in "._"):
                end += 1
        out += [text[at:found], "^{", powers(text[start:end]), "}"]
        at = end
    return "".join([*out, text[at:]])


def same_maths(known: str, said: str) -> bool:
    """Whether what was said is the known value. A file prints an expression as Python writes it (sympy too),
    and math-verify reads `**` as nothing it knows: so what is not the known value as it stands is read again
    with its powers written as LaTeX's."""
    if verify(list(_maths(known)), list(_maths(said))):
        return True
    again = powers(said)
    return again != said and bool(verify(list(_maths(known)), list(_maths(again))))


# ---- numbers (TheoremQA)

def number(text) -> float | None:
    """The value of a number written as a decimal, in scientific notation (1.2e-5, 1.2 \\times 10^{-5}), as an
    expression math-verify can evaluate (\\frac{3}{4}, 2\\sqrt{5}), or as any of those followed by a unit."""
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip().strip("$").replace(",", "").replace("−", "-").strip()
    try:
        return float(text)
    except ValueError:
        pass
    m = _NUMBER.fullmatch(text)
    if m and (m.group(1) or m.group(2)):
        unit = m.group(3) or ""
        if not unit.startswith("\\") or unit.startswith(("\\text", "\\mathrm")):   # 2\sqrt{5} is not 2 of a unit
            value = float(m.group(1) or 1) * 10.0 ** int(m.group(2) or 0)
            return value / 100 if unit == "%" else value      # TheoremQA reads 45% as 0.45
    parsed = _maths(text)
    try:
        value = float(parsed[0]) if parsed else None
    except (TypeError, ValueError, OverflowError):
        return None
    return value if value is not None and math.isfinite(value) else None


def numbers(text) -> list[float] | None:
    """A list of numbers written as [x, y], (x, y) or x, y. None if any item is not a number."""
    if isinstance(text, (list, tuple)):
        return [float(x) for x in text]
    items = [number(item) for item in text.strip().strip("$").strip("[]()").split(",") if item.strip()]
    return None if not items or any(x is None for x in items) else items


def close(said: float, known: float) -> bool:
    return abs(said - known) <= TOLERANCE * abs(known)


# ---- text (BBEH). Ported from bbeh/evaluate.py in github.com/google-deepmind/bbeh, Copyright 2025 Google LLC,
# Apache License 2.0. The matching rules are theirs, unchanged.

def _bbeh_answer(sample: str) -> str:
    answer = sample.strip()
    for prefix in ("The answer is:", "The final answer is ", "The final answer is: ", "The answer is "):
        if prefix in answer:
            answer = answer.split(prefix)[-1].strip()
    answer = answer.removesuffix(".")
    if answer.startswith("$") and answer.endswith("$"):
        answer = answer[1:-1]
    for wrapper in ("boxed{", "text{", "texttt{"):
        if wrapper in answer and answer.endswith("}"):
            answer = answer[0:-1].split(wrapper)[1]
    answer = answer.lower().replace(", ", ",").replace("**", "").split("\n")[0]
    return answer.removesuffix(".")


def bbeh_match(said: str, known: str) -> bool:
    prediction, reference = _bbeh_answer(said), known.strip().lower().replace(", ", ",")
    if prediction == reference:
        return True
    if len(prediction) == 3 and prediction[0] == "(" and prediction[-1] == ")":      # (a) against a
        return prediction[1] == reference
    if len(reference) == 3 and reference[0] == "(" and reference[-1] == ")":
        return reference[1] == prediction
    try:
        if float(prediction) == float(reference):
            return True
    except ValueError:
        pass
    return (prediction.replace("'", "") == reference.replace("'", "")
            or f"[{reference}]" == prediction or f"[{prediction}]" == reference
            or (prediction.endswith("?") and prediction[:-1] == reference))


# ---- the two things the rest of the code asks

def tidy(problem: Problem, answer: str) -> str:
    """An answer written one way, so that the same answer given twice is the same text."""
    kind, answer = problem.answer_type, str(answer).strip()
    if kind == "choice":
        return answer.upper()
    if kind == "text":
        answer = _bbeh_answer(answer)
        return answer[1] if re.fullmatch(r"\(\w\)", answer) else answer      # BBEH takes (a) and a as the same
    if kind.startswith("list"):
        items = numbers(answer)
        return answer if items is None else "[" + ", ".join(f"{x:.4g}" for x in items) + "]"
    if kind == "float":
        value = number(answer)
        return answer if value is None else f"{value:.4g}"
    plain = answer.strip("$").replace(",", "").replace(" ", "")
    if m := re.fullmatch(r"([-+]?\d+)(?:\.0*)?", plain):     # a whole number however it is written: 033, 3,840, 33.0
        return str(int(m.group(1)))
    return re.sub(r"\s+|\$|\\left|\\right|\\[,;!]", "", answer).replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")


def right(problem: Problem, answer: str | None) -> bool:
    if answer is None or not str(answer).strip():
        return False
    kind, known = problem.answer_type, problem.answer
    if kind == "choice":
        return str(answer).strip().upper() == known
    if kind == "text":
        return bbeh_match(str(answer), known)
    if kind == "float":
        said = number(answer)
        return said is not None and close(said, float(known))
    if kind.startswith("list"):
        said = numbers(answer)
        return (said is not None and len(said) == len(known)
                and all(close(s, k) for s, k in zip(sorted(said), sorted(float(k) for k in known))))
    return tidy(problem, answer) == tidy(problem, problem.truth) or same_maths(problem.truth, str(answer))


def recorded(problem: Problem, answer: str | None) -> str | None:
    if answer is None or not str(answer).strip():
        return None
    return problem.truth if right(problem, answer) else tidy(problem, answer)
