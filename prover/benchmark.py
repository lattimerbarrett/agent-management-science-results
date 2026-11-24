from functools import lru_cache

from datasets import load_dataset

DATASET = "MathArena/arxivmath-0926"  # ArXivMath, September 2026 edition: 53 problems from arXiv papers
# Other editions, by their month. Wherever a problem is a number (run folders, sweeps, the grader's cache), a problem
# of another edition is month * 100 + its problem_idx, so that it stays apart from September's 1-53: October's p12
# is 1012, and its run folders end in -p1012.
EDITIONS = {10: "MathArena/arxivmath-1026"}  # October 2026: 47 problems, 1001-1047
# The October list: October's counterpart of September's nine. The 13 problems that one lone agent, not told the
# answer, didn't solve (the individual baseline of 2026-11-22, oct-solo-v1: 34 of 47 solved), and p38, which Sol (max)
# missed on MathArena.
OCTOBER = [1011, 1013, 1015, 1022, 1024, 1028, 1029, 1033, 1038, 1039, 1040, 1041, 1042, 1045]


@lru_cache(maxsize=None)
def edition(month):
    """Another edition's problems, by their numbers here (month * 100 + problem_idx)."""
    return {
        month * 100 + int(r["problem_idx"]): {
            "idx": month * 100 + int(r["problem_idx"]),
            "problem": r["problem"],
            "answer": r["answer"],
            "source": r["source"],
            "title": r["title"],
        }
        for r in load_dataset(EDITIONS[month], split="train")
    }


def in_edition(idx):
    """Whether idx is a problem of another edition (1012: October's p12)."""
    return isinstance(idx, int) and not isinstance(idx, bool) and idx // 100 in EDITIONS and idx in edition(idx // 100)


class Benchmark:
    """The problems, by MathArena's problem number (problem_idx, 1-53 for September; another edition's by
    month * 100 + problem_idx, see EDITIONS)."""

    def __init__(self, name=DATASET):
        self.name = name
        self.dataset = load_dataset(name, split="train")
        self.problems = {
            r["problem_idx"]: {
                "idx": r["problem_idx"],
                "problem": r["problem"],
                "answer": r["answer"],
                "source": r["source"],
                "title": r["title"],
            }
            for r in self.dataset
        }

    def get_problem(self, idx):
        return self.problems[idx] if idx in self.problems or not in_edition(idx) else edition(idx // 100)[idx]
