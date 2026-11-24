#!/usr/bin/env python3
"""Rebuild the result files of this section from the logs in runs/.

    python3 results/make_tables.py        (from contingency-theory/)

It reads, for every run, runs/<task>/<arrangement>/score.json, posts.jsonl and agents/*.jsonl. Where a run has
only its score.json here, it takes the score and leaves the run's other columns empty. It writes beside this
script:

    scores.csv    a task a row: the two scores, their difference in points, and the task's number in Figure 3
    runs.csv      a run a row: its score, how long it ran, and how much its agents posted and pushed
    tables.md     the tables of the README

Standard library only. No keys and no model calls.
"""

import csv
import json
import re
import statistics
from datetime import datetime
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"

# The folder names the runs came with, and what the post calls them.
ARRANGEMENTS = {"1x10": "one group of ten", "2x5": "two groups of five"}

TIMESTAMP = re.compile(r'"timestamp": "([^"]+)"')


def when(line):
    """The time of one transcript record. Every record starts with its timestamp."""
    found = TIMESTAMP.search(line, 0, 120)
    stamp = found.group(1) if found else json.loads(line)["timestamp"]
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def read_run(folder):
    """One run: its score, its length, and the counts of what its agents posted and pushed."""
    score = Decimal(str(json.loads((folder / "score.json").read_text())["score"]))

    first = last = None
    records = 0
    transcripts = sorted((folder / "agents").glob("*.jsonl"))
    if not transcripts:      # this run's transcripts are not in the repo (see the README): only its score is
        return {"score": score, "minutes": None, "agents": None, "records": None,
                "posts_group": None, "posts_public": None, "pushes": None}
    for transcript in transcripts:
        with transcript.open(encoding="utf-8") as lines:
            for line in lines:
                if not line.strip():
                    continue
                records += 1
                at = when(line)
                first = at if first is None or at < first else first
                last = at if last is None or at > last else last

    posts_group = posts_public = pushes = 0
    with (folder / "posts.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            if not line.strip():
                continue
            post = json.loads(line)
            if post["kind"].startswith("push"):      # the platform's notice of a push to a group's main
                pushes += 1
            elif post.get("channel_arg") == "public":
                posts_public += 1
            else:
                posts_group += 1

    return {
        "score": score,
        "minutes": round((last - first).total_seconds() / 60, 1),
        "agents": len(transcripts),
        "records": records,
        "posts_group": posts_group,
        "posts_public": posts_public,
        "pushes": pushes,
    }


def points(difference):
    """A difference of two scores, in points of the pass rate, with its sign: 0.131 -> '+13.1'."""
    return f"{difference * 100:+.1f}"


def main():
    tasks = sorted(folder.name for folder in RUNS.iterdir() if folder.is_dir())
    runs = {(task, arrangement): read_run(RUNS / task / arrangement) for task in tasks for arrangement in ARRANGEMENTS}

    # --- scores.csv: a task a row -----------------------------------------------------------------------------
    difference = {task: runs[task, "1x10"]["score"] - runs[task, "2x5"]["score"] for task in tasks}
    # Figure 3 orders the tasks from the largest lead of one group of ten to the largest lead of two groups of five.
    in_figure = sorted(tasks, key=lambda task: (-difference[task], task))
    figure_task = {task: number for number, task in enumerate(in_figure, start=1)}

    with (HERE / "scores.csv").open("w", newline="") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["task", "2x5", "1x10", "difference_points", "figure_task"])
        for task in tasks:
            rows.writerow([
                task,
                f"{runs[task, '2x5']['score']:.3f}",
                f"{runs[task, '1x10']['score']:.3f}",
                points(difference[task]),
                figure_task[task],
            ])

    # --- runs.csv: a run a row --------------------------------------------------------------------------------
    columns = ["score", "minutes", "agents", "records", "posts_group", "posts_public", "pushes"]
    with (HERE / "runs.csv").open("w", newline="") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["task", "arrangement", "folder"] + columns)
        for task in tasks:
            for arrangement in ARRANGEMENTS:
                run = runs[task, arrangement]
                rows.writerow([task, arrangement, f"runs/{task}/{arrangement}", f"{run['score']:.3f}"]
                              + ["" if run[column] is None else run[column] for column in columns[1:]])

    # --- tables.md: the tables of the README ------------------------------------------------------------------
    def of(arrangement, column):
        """A column over the runs of one arrangement: every run for the score, and for the rest the runs whose
        transcripts are here."""
        return [runs[task, arrangement][column] for task in tasks if runs[task, arrangement][column] is not None]

    mean = {a: sum(of(a, "score")) / len(tasks) for a in ARRANGEMENTS}
    ahead = {"1x10": [t for t in tasks if difference[t] > 0], "2x5": [t for t in tasks if difference[t] < 0]}
    level = [t for t in tasks if difference[t] == 0]
    best = {"1x10": in_figure[0], "2x5": in_figure[-1]}

    def short(task):
        """'vladimirmarkelov__ttdl.f0e6ecb' -> 'ttdl'"""
        return task.split(".")[0].split("__")[-1]

    def minutes(arrangement):
        spans = of(arrangement, "minutes")
        return f"{statistics.median(spans):.1f} ({min(spans):.1f} to {max(spans):.1f})"

    def total(arrangement, column):
        return f"{sum(of(arrangement, column)):,}"

    lines = [
        "<!-- Written by results/make_tables.py from the logs in runs/. Change the script, not this file. -->",
        "",
        "## Headline",
        "",
        f"| {len(tasks)} ProgramLab tasks | one group of ten | two groups of five |",
        "|---|---|---|",
        f"| mean score | **{mean['1x10']:.3f}** | **{mean['2x5']:.3f}** |",
        f"| tasks on which it scored higher | **{len(ahead['1x10'])} of {len(tasks)}** | **{len(ahead['2x5'])} of {len(tasks)}** |",
        f"| its largest lead on a task | **{abs(difference[best['1x10']] * 100):.1f} points** ({short(best['1x10'])}) "
        f"| **{abs(difference[best['2x5']] * 100):.1f} points** ({short(best['2x5'])}) |",
        "",
        f"Tasks on which the two scored the same: {len(level)}.",
        "",
        "## Task by task",
        "",
        "| task in Figure 3 | task | one group of ten | two groups of five | difference, points |",
        "|---|---|---|---|---|",
    ]
    for task in in_figure:
        lines.append(f"| {figure_task[task]} | `{task}` | {runs[task, '1x10']['score']:.3f} "
                     f"| {runs[task, '2x5']['score']:.3f} | {points(difference[task])} |")
    lines.append(f"| | **mean of {len(tasks)}** | **{mean['1x10']:.3f}** | **{mean['2x5']:.3f}** "
                 f"| **{points(mean['1x10'] - mean['2x5'])}** |")
    lines += [
        "",
        "## The runs",
        "",
        "| | one group of ten | two groups of five |",
        "|---|---|---|",
        f"| runs | {len(tasks)} | {len(tasks)} |",
        f"| runs whose transcripts are here | {len(of('1x10', 'agents'))} | {len(of('2x5', 'agents'))} |",
        f"| agents in a run | {of('1x10', 'agents')[0]} | {of('2x5', 'agents')[0]} |",
        f"| minutes from a run's first record to its last: median (shortest to longest) | {minutes('1x10')} | {minutes('2x5')} |",
        f"| posts by agents in a group's channel | {total('1x10', 'posts_group')} | {total('2x5', 'posts_group')} |",
        f"| posts by agents in the public channel | no such channel | {total('2x5', 'posts_public')} |",
        f"| pushes to a group's `main` | {total('1x10', 'pushes')} | {total('2x5', 'pushes')} |",
        "",
        "The last four rows are over the runs whose transcripts are here.",
        "",
    ]
    (HERE / "tables.md").write_text("\n".join(lines), encoding="utf-8")

    assert all(run["agents"] in (10, None) for run in runs.values()), "a run does not have ten agents"
    print(f"{len(runs)} runs of {len(tasks)} tasks read from {RUNS}")
    print("wrote scores.csv, runs.csv and tables.md in", HERE)


if __name__ == "__main__":
    main()
