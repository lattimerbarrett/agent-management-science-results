"""A benchmark problem: one question with a known answer, the thing a swarm is asked.

Problems come from files with one JSON object per line: `benchmark`, `split`, `id`, `question`, `answer`,
`answer_type`, and for some sources `options` or `task` (`mathswarm/benchmarks.py` writes them). `answer_type`
says what a right answer looks like and so how it is checked (`mathswarm/grading.py`):

    integer         a whole number (AIME; some TheoremQA)
    latex           an exact value, written as a number or a LaTeX expression (HMMT, the Apex Shortlist)
    float           a decimal number (TheoremQA)
    list of float   several numbers (TheoremQA); also "list of integer"
    choice          the letter of one option (GPQA Diamond, MMLU-Pro)
    text            a short answer in the form the question itself asks for (BBEH)
"""
from __future__ import annotations

import json
import random
import zlib
from dataclasses import dataclass
from pathlib import Path

from .paths import BENCHMARKS

LETTERS = "ABCDEFGHIJ"

# The paper's two suites, in the order of its tables. A team learns on the train split of the first benchmark
# of its suite (AIME 2024, GPQA Diamond) and is tested on everything else.
SUITES = {
    "math": ("aime_2024", "aime_2025", "aime_2026", "hmmt_feb_2026", "theoremqa_physics"),
    "logic": ("gpqa_diamond", "mmlu_pro", "bbeh"),
}
ALL = SUITES["math"] + SUITES["logic"]
OTHERS = ("apex_shortlist",)     # built here beside the paper's (mathswarm/benchmarks.py): asked for by name, in no suite
ORDER_SEED = 0

# What an agent is told about the form of its answer, by answer type.
WANTED = {
    "integer": "The answer is a whole number.",
    "latex": "The answer is an exact value. Give it as a number or a LaTeX expression, fully simplified.",
    "float": "The answer is a number. Give its value as a decimal, without units.",
    "list": "The answer is a list of numbers. Give it as [x, y, ...], without units.",
    "choice": "The answer is the letter of one option ({letters}).",
    "text": "Give the answer in exactly the form the problem asks for.",
}


@dataclass(frozen=True)
class Problem:
    benchmark: str
    split: str
    id: str                          # the source's own id, unique within its benchmark
    question: str
    answer: object                   # the known answer: a number, a list of numbers, or text
    answer_type: str
    options: tuple[str, ...] = ()    # MMLU-Pro: the options, lettered A, B, ... in order when shown
    task: str = ""                   # BBEH: which of its tasks the problem belongs to

    @property
    def key(self) -> str:
        return f"{self.benchmark}/{self.id}"

    @property
    def seed(self) -> int:
        """A number that stands for this problem: it fixes every agent's randomness on it, so the same problem
        can be replayed under another arm and compared."""
        return zlib.crc32(self.key.encode())

    @property
    def truth(self) -> str:
        """The known answer as text, the way it is written in the logs."""
        return self.answer if isinstance(self.answer, str) else json.dumps(self.answer)

    @property
    def letters(self) -> str:
        """The option letters an answer may be, for a multiple choice problem ("" otherwise). GPQA questions
        carry their four options in the question text."""
        if self.answer_type != "choice":
            return ""
        return LETTERS[:len(self.options)] if self.options else "ABCD"

    @property
    def statement(self) -> str:
        """The problem as an agent reads it: the question, its options when they are kept apart from it, and
        the form the answer should take."""
        parts = [self.question.strip()]
        if self.options:
            parts.append("\n".join(f"{letter}. {option}" for letter, option in zip(LETTERS, self.options)))
        kind = "list" if self.answer_type.startswith("list") else self.answer_type
        letters = f"{self.letters[0]} to {self.letters[-1]}" if self.letters else ""
        parts.append(WANTED.get(kind, WANTED["text"]).format(letters=letters))
        return "\n\n".join(parts)


def read(path: str | Path) -> list[Problem]:
    """The problems in one file, in the file's order."""
    problems = []
    for line in Path(path).read_text().splitlines():
        row = json.loads(line)
        problems.append(Problem(row["benchmark"], row["split"], str(row["id"]), row["question"], row["answer"],
                                row["answer_type"], tuple(row.get("options") or ()), row.get("task", "")))
    return problems


def names(wanted: list[str]) -> list[str]:
    """Benchmark names, with a suite ("math", "logic") or "all" written out. "all" is the paper's eight: a set
    that was added here (`OTHERS`) is asked for by its name."""
    out: list[str] = []
    for name in wanted:
        for b in (ALL if name == "all" else SUITES.get(name, (name,))):
            if b not in ALL + OTHERS:
                raise SystemExit(f"no benchmark {b!r}: choose from {', '.join(ALL + OTHERS)}, or a suite: math, logic, all "
                                 "(the paper's eight)")
            if b not in out:
                out.append(b)
    return out


def load(benchmark: str, split: str = "test", folder: Path | None = None) -> list[Problem]:
    """A split's problems in a fixed shuffled order, so that the first n are a random n of them and asking for
    more later adds to those. Empty if the benchmark has no such split (only two have a train split)."""
    folder = folder or BENCHMARKS / "problems"
    if not folder.exists():
        raise SystemExit(f"no problems at {folder}: build them first with `lab data`")
    path = folder / f"{benchmark}.{split}.jsonl"
    found = read(path) if path.exists() else []
    random.Random(ORDER_SEED).shuffle(found)
    return found


def select(benchmarks: list[str], split: str = "test", n: int | dict | None = None, folder: Path | None = None) -> list[Problem]:
    """The first `n` problems of each benchmark's order (all of them if `n` is None), benchmark by benchmark.
    `n` may be a number per benchmark: {"aime_2024": 2, "gpqa_diamond": 3}."""
    def count(benchmark: str) -> int | None:
        return n.get(benchmark) if isinstance(n, dict) else n
    return [p for b in names(benchmarks) for p in load(b, split, folder)[:count(b)]]
