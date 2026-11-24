"""Pull the eight public benchmarks behind "Self-Organizing Agent Teams Learn to Reason Together" (Pappu et al.,
2026; papers/self_organizing_agent_teams.pdf) and cut them into the paper's splits, as closely as those can be
recovered. The paper released no data, problem lists or split ids; data/README.md says what each choice rests on.
One set is built beside them that is not the paper's (`OURS`): MathArena's Apex Shortlist, hard problems.

    lab data

Results go to data/benchmarks/:
    sources/      the files as downloaded, each from a pinned commit (not tracked by git)
    problems/     <benchmark>.<split>.jsonl, one problem per line, all in one shape (not tracked by git)
    splits.json   which problems are in which split, by id, with the sha256 of every file above
    summary.md    the table of what was built
No model is needed. Running it again rebuilds the same files without downloading anything twice.

This is `experiments/agent_teams/benchmarks.py` of ../swarm_experiment, moved here unchanged in what it builds
of the paper's: the same sources at the same commits, the same splits. The Apex Shortlist was added here.
"""
import hashlib
import json
import random
import shutil
import time
import urllib.request
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq

from .paths import BENCHMARKS as OUT
from .tables import markdown

SEED = 42   # the sampling seed in the first author's earlier code (see `paper_order`)

HF = "https://huggingface.co/datasets/{repo}/resolve/{commit}/{path}"
GITHUB = "https://raw.githubusercontent.com/{repo}/{commit}/{path}"

# benchmark: (host, repository, commit, file, licence). Every file is fetched at a fixed commit.
SOURCES = {
    "aime_2024": (HF, "Maxwell-Jia/AIME_2024", "8d88b2876a82a080e2f172cc9b25d0d9d2cb4792",
                  "aime_2024_problems.parquet", "MIT"),
    "aime_2025": (HF, "MathArena/aime_2025", "c94da77eb22bbd6439e62a323bec18493a421302",
                  "data/train-00000-of-00001.parquet", "CC BY-NC-SA 4.0"),
    "aime_2026": (HF, "MathArena/aime_2026", "d2de22f3c656b4f56cf8981212186377d1e23bc3",
                  "data/train-00000-of-00001.parquet", "CC BY-NC-SA 4.0"),
    "hmmt_feb_2026": (HF, "MathArena/hmmt_feb_2026", "02fba4f74d8e68e73e66a02d540fd979c05c274c",
                      "data/train-00000-of-00001.parquet", "CC BY-NC-SA 4.0"),
    "theoremqa_physics": (GITHUB, "TIGER-AI-Lab/TheoremQA", "acfc9686aa9b49f3c8f189364a9a9ee9c53da039",
                          "theoremqa_test.json", "MIT"),
    # An ungated copy of GPQA Diamond with the four options already lettered. It is the copy the paper used:
    # its row 132 is the problem the paper calls "GPQA Diamond 132", with the same letters (Figure 10).
    "gpqa_diamond": (HF, "fingertap/GPQA-Diamond", "68be7564497676e07a77a042fdb587deb88c51c3",
                     "test/gpqa_diamond.parquet", "CC BY 4.0"),
    "mmlu_pro": (HF, "TIGER-Lab/MMLU-Pro", "b189ec765aa7ed75c8acfea42df31fdae71f97be",
                 "data/test-00000-of-00001.parquet", "MIT"),
    "bbeh": (GITHUB, "google-deepmind/bbeh", "80d12ca916b7158f22293fcf3144f4d3d854d4be",
             "bbeh/benchmark_tasks/bbeh_{task}/task.json", "CC BY 4.0"),
    # Not the paper's (`OURS`). MathArena's shortlist for its Apex set: 47 problems with a final answer from
    # competitions of 2025, picked as those the strongest models of the time got right about half the time.
    "apex_shortlist": (HF, "MathArena/apex-shortlist", "f3efdf224ef665f129ddaae37699f6098c65781b",
                       "data/train-00000-of-00001.parquet", "CC BY-NC-SA 4.0"),
}
OURS = ("apex_shortlist",)      # built beside the paper's benchmarks and held against nothing of the paper's

# The paper used "five BIG-Bench Extra Hard logical-reasoning subtasks" and does not name them. The first four
# are the tasks BBEH's own paper tags with logical or deductive reasoning (its Table 1); zebra puzzles, the
# classic logic-grid puzzle, is our pick for the fifth.
BBEH_TASKS = ("boardgame_qa", "boolean_expressions", "causal_understanding", "web_of_lies", "zebra_puzzles")

# benchmark: (suite, what the paper says it used, how the problems here were chosen, how well that is known)
ABOUT = {
    "aime_2024": ("math and physics", "15 problems to learn from, the rest held out",
                  "the 30 in seed-42 order: first 15 train, last 15 test", "split is a guess"),
    "aime_2025": ("math and physics", "transfer", "all 30", "same set"),
    "aime_2026": ("math and physics", "transfer", "all 30", "same set"),
    "hmmt_feb_2026": ("math and physics", "transfer", "all 33", "same set"),
    "theoremqa_physics": ("math and physics", "transfer", "the physics questions that have no picture",
                          "set inferred from the paper's percentages"),
    "gpqa_diamond": ("knowledge and logic", "25 problems to learn from, 100 others held out",
                     "the 198 in seed-42 order: first 25 train, next 100 test",
                     "same source; split is a guess that fits the one problem the paper names"),
    "mmlu_pro": ("knowledge and logic", "transfer, 100 questions", "first 100 of the 12,032 in seed-42 order",
                 "sample is a guess"),
    "bbeh": ("knowledge and logic", "transfer, 75 questions from five logical-reasoning subtasks",
             "first 15 of each of five tasks in seed-42 order", "tasks and sample are a guess"),
    "apex_shortlist": ("hard math, not the paper's", "not used", "all 47", "not in the paper: MathArena's own set"),
}

# How many problems the paper's numbers imply per split. The paper states 15 (AIME 2024 train), 25 and 100
# (GPQA), 100 (MMLU-Pro) and 75 (BBEH); the rest are read off its percentages (see `fits`).
PAPER_SIZES = {"aime_2024": {"train": 15, "test": 15}, "aime_2025": {"test": 30}, "aime_2026": {"test": 30},
               "hmmt_feb_2026": {"test": 33}, "theoremqa_physics": {"test": 114},
               "gpqa_diamond": {"train": 25, "test": 100}, "mmlu_pro": {"test": 100}, "bbeh": {"test": 75}}

# The paper's reported percentages on each test set, each a mean over three seeds: Tables 1 and 2 top to bottom
# (best member, self-consistency, self-reflection, linearization, member-vote, debate, Mixture of Agents,
# homogeneous team, SAT, routing-oracle coverage, SAT coverage).
PAPER_PERCENT = {
    "aime_2024": (64.4, 75.8, 71.1, 74.0, 60.7, 66.7, 75.6, 66.7, 84.7, 73.3, 93.3),
    "aime_2025": (40.0, 44.4, 41.1, 43.3, 38.5, 41.1, 46.7, 46.7, 60.8, 51.1, 73.3),
    "aime_2026": (42.2, 53.4, 52.2, 68.5, 40.9, 53.3, 57.8, 60.0, 71.2, 57.8, 73.3),
    "hmmt_feb_2026": (26.3, 31.9, 29.3, 39.4, 25.3, 30.3, 32.3, 36.4, 39.4, 36.4, 54.5),
    "theoremqa_physics": (71.1, 71.5, 72.2, 68.4, 71.3, 72.2, 74.0, 70.2, 77.2, 76.6, 81.6),
    "gpqa_diamond": (72.7, 71.6, 77.7, 79.0, 67.0, 73.7, 72.0, 78.0, 80.0, 84.0, 94.0),
    "mmlu_pro": (79.7, 81.2, 81.7, 84.0, 79.9, 79.7, 84.3, 76.0, 82.4, 88.0, 91.0),
    "bbeh": (45.3, 49.8, 54.7, 53.3, 43.6, 57.3, 57.3, 58.7, 56.0, 66.7, 78.7),
}
PAPER_SEEDS = 3
# Table 4: the initial strategy, which the paper ran once per problem. A single run pins the size hardest.
PAPER_INITIAL = {"aime_2024": 73.3, "aime_2025": 50.0, "aime_2026": 50.0, "hmmt_feb_2026": 24.2,
                 "theoremqa_physics": 72.8, "gpqa_diamond": 73.0, "mmlu_pro": 81.0, "bbeh": 54.7}


def paper_order(n: int) -> list[int]:
    """Row numbers 0..n-1 in the order the first author's earlier code draws a subset in: `random.Random(42)`
    shuffles the row numbers and a run takes the first `limit` of them (run_gpqa_diamond.py and
    run_mmlu_pro.py in github.com/apappu97/multi-agent-teams-hold-experts-back, commit a8833a2). Whether this
    paper drew its subsets the same way is not known."""
    order = list(range(n))
    random.Random(SEED).shuffle(order)
    return order


def cut(problems: list[dict], **sizes: int) -> dict[str, list[dict]]:
    """Cut `problems`, taken in the paper's order, into consecutive splits of the given sizes, each put back in
    source order: cut(p, train=25, test=100) makes the first 25 drawn train and the next 100 test."""
    order, splits, start = paper_order(len(problems)), {}, 0
    for name, size in sizes.items():
        splits[name] = [problems[i] for i in sorted(order[start:start + size])]
        start += size
    return splits


def fits(percent: float, problems: int, runs: int = PAPER_SEEDS) -> bool:
    """Whether a percentage printed to one decimal can be a mean over `runs` runs of `problems` problems, that
    is k / (runs x problems) for a whole number k."""
    total = runs * problems
    return any(round(100 * k / total, 1) == percent for k in range(total + 1))


def paper_fit(benchmark: str, problems: int) -> tuple[int, int]:
    """How many of the paper's percentages on a test set can come from this many problems, and out of how many."""
    values = PAPER_PERCENT[benchmark]
    fit = sum(fits(v, problems) for v in values) + fits(PAPER_INITIAL[benchmark], problems, runs=1)
    return fit, len(values) + 1


# ---- one function per source: its rows in, problems in the common shape out (source order kept)

def aime_2024(rows: list[dict]) -> list[dict]:
    return [{"id": r["ID"], "question": r["Problem"], "answer": int(r["Answer"]), "answer_type": "integer"}
            for r in rows]


def matharena_aime(rows: list[dict]) -> list[dict]:
    """MathArena numbers a year's problems 1 to 30, AIME I then AIME II. Ids are written the way the paper
    writes them: problem 23 is II-08."""
    problems = []
    for r in rows:
        second, number = divmod(r["problem_idx"] - 1, 15)
        problems.append({"id": f"{'II' if second else 'I'}-{number + 1:02d}", "question": r["problem"],
                         "answer": int(r["answer"]), "answer_type": "integer"})
    return problems


def hmmt(rows: list[dict]) -> list[dict]:
    return [{"id": str(r["problem_idx"]), "question": r["problem"], "answer": r["answer"], "answer_type": "latex",
             "problem_type": r["problem_type"]} for r in rows]


def apex_shortlist(rows: list[dict]) -> list[dict]:
    """MathArena numbers the problems 1 to 47 and says where each is from (`source`: a competition and a problem
    of it). 35 answers are whole numbers and 12 are not (a fraction, a root, a formula in n). All are
    checked as exact values, as HMMT's are, so that what an agent is told of the answer's form is the same for
    every problem and does not say which of the two its problem has."""
    return [{"id": str(r["problem_idx"]), "question": r["problem"], "answer": r["answer"], "answer_type": "latex",
             "source": r["source"]} for r in rows]


def theoremqa_physics(rows: list[dict]) -> list[dict]:
    """The physics questions that come without a picture: 114 of TheoremQA's 131 physics questions."""
    return [{"id": r["id"], "question": r["Question"], "answer": r["Answer"], "answer_type": r["Answer_type"],
             "subfield": r["subfield"], "theorem": r["theorem"]}
            for r in rows if r["field"] == "Physics" and not r["Picture"]]


def gpqa_diamond(rows: list[dict]) -> list[dict]:
    """The id is the row number, which is how the paper numbers GPQA problems. The question already ends with
    its four lettered options."""
    return [{"id": str(i), "question": r["question"], "answer": r["answer"], "answer_type": "choice"}
            for i, r in enumerate(rows)]


def mmlu_pro(rows: list[dict]) -> list[dict]:
    return [{"id": str(r["question_id"]), "question": r["question"], "options": list(r["options"]),
             "answer": r["answer"], "answer_type": "choice", "category": r["category"], "src": r["src"]}
            for r in rows]


def bbeh(task: str, examples: list[dict]) -> list[dict]:
    return [{"id": f"{task}/{i}", "question": e["input"], "answer": e["target"], "answer_type": "text",
             "task": task} for i, e in enumerate(examples)]


def build(raw: dict) -> dict[str, dict[str, list[dict]]]:
    """Every benchmark's splits from the downloaded rows: {benchmark: {split: [problem, ...]}}."""
    return {
        "aime_2024": cut(aime_2024(raw["aime_2024"]), train=15, test=15),
        "aime_2025": {"test": matharena_aime(raw["aime_2025"])},
        "aime_2026": {"test": matharena_aime(raw["aime_2026"])},
        "hmmt_feb_2026": {"test": hmmt(raw["hmmt_feb_2026"])},
        "theoremqa_physics": {"test": theoremqa_physics(raw["theoremqa_physics"])},
        "gpqa_diamond": cut(gpqa_diamond(raw["gpqa_diamond"]), train=25, test=100),
        "mmlu_pro": cut(mmlu_pro(raw["mmlu_pro"]), test=100),
        "bbeh": {"test": [p for task in BBEH_TASKS for p in cut(bbeh(task, raw["bbeh"][task]), test=15)["test"]]},
        "apex_shortlist": {"test": apex_shortlist(raw["apex_shortlist"])},
    }


def check_against_paper(built: dict) -> list[tuple[str, bool]]:
    """What the paper lets us check: the size of every split of its benchmarks, and the four problems it names.
    And of the set that is not the paper's, that it is the 47 problems it was when it was added."""
    def answer(benchmark, split, id_):
        return next((p["answer"] for p in built[benchmark][split] if p["id"] == id_), None)

    sizes = {b: {s: len(ps) for s, ps in splits.items()} for b, splits in built.items()}
    ids = [(b, p["id"]) for b, splits in built.items() for ps in splits.values() for p in ps]
    named = next((p for p in built["gpqa_diamond"]["test"] if p["id"] == "132"), {"question": "", "answer": None})
    return [
        ("every split has the size the paper implies", {b: s for b, s in sizes.items() if b not in OURS} == PAPER_SIZES),
        ("the Apex Shortlist is its 47 problems, numbered 1 to 47",
         [p["id"] for p in built["apex_shortlist"]["test"]] == [str(i) for i in range(1, 48)]),
        ("no problem is in two splits", len(ids) == len(set(ids))),
        ("AIME 2026 II-01 has the paper's answer, 178", answer("aime_2026", "test", "II-01") == 178),
        ("AIME 2026 II-08 has the paper's answer, 245", answer("aime_2026", "test", "II-08") == 245),
        ("HMMT February 2026 problem 6 has the paper's answer, 3840", answer("hmmt_feb_2026", "test", "6") == "3840"),
        ("GPQA Diamond 132 is held out, is the paper's question (1-bromobenzene-2-d) and its answer is B",
         "bromobenzene-2-d" in named["question"] and named["answer"] == "B"),
    ]


# ---- files

def fetch(url: str, to: Path) -> Path:
    """Download once. A file already in sources/ is kept: every url names a commit, so it cannot have changed."""
    if not to.exists():
        to.parent.mkdir(parents=True, exist_ok=True)
        part = to.with_name(to.name + ".part")
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "math_swarm_explore"})
                with urllib.request.urlopen(request, timeout=120) as response, open(part, "wb") as f:
                    shutil.copyfileobj(response, f)
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(5)
        part.rename(to)
    return to


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path):
    if path.suffix == ".parquet":
        return pq.read_table(path).to_pylist()
    return json.loads(path.read_text())


def download(folder: Path, say) -> tuple[dict, dict]:
    """Fetch every source. Returns the rows per benchmark (per task for BBEH) and, per benchmark, where each
    file came from and its sha256."""
    raw, files = {}, {}
    for benchmark, (host, repo, commit, path, licence) in SOURCES.items():
        parts = {task: path.format(task=task) for task in BBEH_TASKS} if benchmark == "bbeh" else {None: path}
        files[benchmark] = {"repo": repo, "commit": commit, "licence": licence, "files": {}}
        for task, file in parts.items():
            to = folder / benchmark / (f"{task}.json" if task else Path(file).name)
            fresh = not to.exists()
            rows = read(fetch(host.format(repo=repo, commit=commit, path=file), to))
            files[benchmark]["files"][file] = sha256(to)
            if task:
                raw.setdefault(benchmark, {})[task] = rows["examples"]
            else:
                raw[benchmark] = rows
            say(f"{'downloaded' if fresh else 'have'} {repo} {file}")
    return raw, files


def main(out: Path = OUT, say=print) -> dict:
    """Build everything under `out`. Returns the summary that is also written to summary.json."""
    raw, files = download(out / "sources", say)
    built = build(raw)

    checks = check_against_paper(built)
    for what, ok in checks:
        say(f"{'ok  ' if ok else 'FAIL'}  {what}")
    if not all(ok for _, ok in checks):
        raise SystemExit("the sources no longer give what the paper describes; nothing was written")

    manifest = {"paper": "arXiv:2609.22682", "seed": SEED, "benchmarks": {}}
    rows = []
    for benchmark, splits in built.items():
        suite, _, chosen, known = ABOUT[benchmark]
        manifest["benchmarks"][benchmark] = {"suite": suite, "source": files[benchmark], "chosen": chosen,
                                             "known": known, "splits": {}}
        for split, problems in splits.items():
            path = out / "problems" / f"{benchmark}.{split}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(json.dumps({"benchmark": benchmark, "split": split, **p}, ensure_ascii=False) + "\n"
                                    for p in problems))
            manifest["benchmarks"][benchmark]["splits"][split] = {
                "problems": len(problems), "file": f"problems/{path.name}", "sha256": sha256(path),
                "ids": [p["id"] for p in problems]}
            fit = "{} of {}".format(*paper_fit(benchmark, len(problems))) if split == "test" and benchmark not in OURS else ""
            rows.append([suite, benchmark, split, str(len(problems)), fit, chosen, known])

    summary = {"problems": sum(int(r[3]) for r in rows),
               "sizes": {b: {s: len(ps) for s, ps in splits.items()} for b, splits in built.items()},
               "paper_percentages_that_fit": {r[1]: r[4] for r in rows if r[4]},
               "theoremqa_physics_fit_if_all_131": "{} of {}".format(*paper_fit("theoremqa_physics", 131)),
               "mmlu_pro_categories": dict(Counter(p["category"] for p in built["mmlu_pro"]["test"]).most_common()),
               "checks": [{"check": what, "ok": ok} for what, ok in checks]}
    table = markdown(["suite", "benchmark", "split", "problems", "paper's numbers that fit", "chosen by", "known?"], rows)
    note = (f"{summary['problems']} problems. Paper's numbers that fit: how many of the percentages the paper "
            f"reports on that test set can come from this many problems ({PAPER_SEEDS} seeds; the initial strategy "
            "was run once). The problems themselves are in problems/ (not tracked by git); splits.json lists "
            "every split by problem id.")
    for name, content in (("splits", manifest), ("summary", summary)):
        (out / f"{name}.json").write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n")
    (out / "summary.md").write_text(f"{table}\n\n{note}\n")
    say(f"\n{table}\n\n{note}\n")
    return summary
