#!/usr/bin/env python3
"""Rebuild the result files of this section from the logs in runs/.

    python3 results/make_tables.py        (from groupthink/)

It reads four files of the run in runs/main/:

    config.json       the settings of each arm, the seed, the command and the commit
    engine.jsonl      the model that wrote every reply, and the server it ran on
    episodes.jsonl    a problem under an arm a line: the answer each agent held after each of its steps
    looks.jsonl       a look a line: which agent was shown whose file, after which step

and writes beside this script:

    pairs.csv         a reading rule a row: how the pairs of a problem's agents ended, and how the agents did
    change.csv        each rule with reading against no reading: how much the pairs that agree rose
    problems.csv      a problem under a reading rule a row
    answers.csv       an agent a row: the answer it ended on
    tables.md         the tables of the README

Standard library only. No keys and no model calls.

A pair is two of the eight agents on one problem under one reading rule: 28 pairs a problem. Every pair ends one
of five ways (KINDS below), which add up to all of them. This is `pairs` in
code/math_swarm_explore/mathswarm/metrics.py, written out again here so that it runs without the lab's code.
"""

import csv
import json
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent / "runs" / "main"

# The arms as the logs name them, and what this section calls them, in the order of how often an agent reads.
ARMS = {
    "desk": "no peer reading",
    "look_at_others": "a peer's file after 1 step in 4",
    "always_look_at_others": "a peer's file after every step",
}
BASELINE = "desk"

# How two agents on the same problem ended. An answer is right when it is the known one.
KINDS = {
    "both_right": "both right",
    "same_wrong": "the same wrong answer",
    "different_wrong": "two different wrong answers",
    "right_and_wrong": "one right, one wrong",
    "no_answer": "one or both with no answer",
}

RESAMPLES = 10_000      # for the intervals in change.csv: problems drawn again with replacement, this many times


def jsonl(path):
    with path.open(encoding="utf-8") as lines:
        return [json.loads(line) for line in lines if line.strip()]


def pairs(answers, truth):
    """The pairs of one problem's agents by how the two ended, as counts. `answers` is what each agent held at
    the end: the known answer's own text if it was right, its answer as it wrote it if not, None if it had none."""
    held = Counter(answer for answer in answers if answer is not None)
    right = held.get(truth, 0)
    wrong = sum(held.values()) - right
    same = sum(n * (n - 1) // 2 for answer, n in held.items() if answer != truth)
    kinds = {
        "both_right": right * (right - 1) // 2,
        "same_wrong": same,
        "different_wrong": wrong * (wrong - 1) // 2 - same,
        "right_and_wrong": right * wrong,
    }
    kinds["no_answer"] = len(answers) * (len(answers) - 1) // 2 - sum(kinds.values())
    return kinds


def quantile(ordered, q):
    """The q-quantile of a sorted list, between its two nearest values."""
    at = q * (len(ordered) - 1)
    low = int(at)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (at - low)


def interval(values):
    """The mean of a value a problem, and a 95% interval for it: the problems are drawn again with replacement
    RESAMPLES times, and the interval holds the middle 95% of the means. The draws are fixed, so it comes out the
    same every time."""
    draw = random.Random(0)
    n = len(values)
    means = sorted(sum(values[int(draw.random() * n)] for _ in range(n)) / n for _ in range(RESAMPLES))
    return sum(values) / n, quantile(means, 0.025), quantile(means, 0.975)


def percent(share):
    return f"{100 * share:.1f}"


def points(difference):
    return f"{100 * difference:+.1f}"


def main():
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    settings = {arm: config["settings"][f"arm:{arm}"] for arm in ARMS}
    episodes = {(e["arm"], int(e["problem"])): e for e in jsonl(RUN / "episodes.jsonl")}
    looks = jsonl(RUN / "looks.jsonl")
    engine = jsonl(RUN / "engine.jsonl")

    problems = sorted({problem for _, problem in episodes})
    assert set(episodes) == {(arm, problem) for arm in ARMS for problem in problems}, "an arm lacks a problem"
    assert all(e["benchmark"] == "apex_shortlist" and e["seed"] == config["settings"]["seed"] for e in episodes.values())
    truth = {problem: episodes[BASELINE, problem]["truth"] for problem in problems}
    assert all(e["truth"] == truth[problem] for (_, problem), e in episodes.items())

    # What each agent ended on: the answers held after the last step.
    final = {key: e["answers"][-1] for key, e in episodes.items()}
    agents = {len(answers) for answers in final.values()}
    assert len(agents) == 1, "the problems do not all have as many agents"
    agents = agents.pop()
    assert all(settings[arm]["agents"] == agents for arm in ARMS)
    a_problem = agents * (agents - 1) // 2                 # pairs of one problem's agents
    kinds = {key: pairs(answers, truth[key[1]]) for key, answers in final.items()}

    def outcome(answer, problem):
        return "no answer" if answer is None else "right" if answer == truth[problem] else "wrong"

    def ended(arm, problem):
        return Counter(outcome(answer, problem) for answer in final[arm, problem])

    def most_held_wrong(arm, problem):
        wrong = Counter(a for a in final[arm, problem] if a is not None and a != truth[problem])
        if not wrong:
            return "", 0
        top = max(wrong.values())
        return sorted(a for a, n in wrong.items() if n == top)[0], top       # a tie goes to the first in order

    # The looks: a row of looks.jsonl is an agent picked to read after one of its steps. It was shown a file
    # unless the other agent had not written one yet (`seen` is null).
    assert all(look["reader"] != look["of"] for look in looks), "an agent was shown its own file"
    shown = [look for look in looks if look["seen"] is not None]
    files_read = Counter(look["arm"] for look in shown)
    readers = {arm: len({(look["problem"], look["reader"]) for look in shown if look["arm"] == arm}) for arm in ARMS}
    assert files_read[BASELINE] == 0

    # --- pairs.csv: a reading rule a row ----------------------------------------------------------------------
    total = {arm: Counter() for arm in ARMS}               # pairs of each kind, added up over the problems
    share = {arm: {} for arm in ARMS}                      # the share of a problem's pairs, averaged over problems
    people = {arm: Counter() for arm in ARMS}              # agents by how they ended
    people_share = {arm: {} for arm in ARMS}               # the share of a problem's agents, averaged over problems
    for arm in ARMS:
        for problem in problems:
            total[arm].update(kinds[arm, problem])
            people[arm].update(ended(arm, problem))
        for kind in KINDS:
            share[arm][kind] = sum(kinds[arm, p][kind] / a_problem for p in problems) / len(problems)
        for how in ("right", "wrong", "no answer"):
            people_share[arm][how] = sum(ended(arm, p)[how] / agents for p in problems) / len(problems)

    def chance(arm):
        rule = settings[arm]["looks"]
        return 0 if rule is None else rule["p"]

    with (HERE / "pairs.csv").open("w", newline="", encoding="utf-8") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["arm", "reading", "chance_of_reading_after_a_step", "problems", "agents_a_problem", "pairs"]
                      + [f"pairs_{kind}" for kind in KINDS] + [f"pct_pairs_{kind}" for kind in KINDS]
                      + ["agents", "agents_right", "agents_wrong", "agents_no_answer",
                         "pct_agents_right", "pct_agents_wrong", "pct_agents_no_answer",
                         "files_read", "agents_that_read_a_file"])
        for arm, reading in ARMS.items():
            rows.writerow([arm, reading, chance(arm), len(problems), agents, a_problem * len(problems)]
                          + [total[arm][kind] for kind in KINDS] + [percent(share[arm][kind]) for kind in KINDS]
                          + [agents * len(problems), people[arm]["right"], people[arm]["wrong"], people[arm]["no answer"],
                             percent(people_share[arm]["right"]), percent(people_share[arm]["wrong"]),
                             percent(people_share[arm]["no answer"]), files_read[arm], readers[arm]])

    # --- change.csv: each rule with reading, against no reading -----------------------------------------------
    # The same eight agents play a problem under every rule, so the difference is taken problem by problem.
    risen = {}
    for arm in ARMS:
        if arm == BASELINE:
            continue
        for kind in ("same_wrong", "both_right"):
            each = [(kinds[arm, p][kind] - kinds[BASELINE, p][kind]) / a_problem for p in problems]
            mean, low, high = interval(each)
            risen[arm, kind] = {"each": each, "mean": mean, "low": low, "high": high,
                                "rose": sum(d > 0 for d in each), "level": sum(d == 0 for d in each),
                                "fell": sum(d < 0 for d in each)}
    with (HERE / "change.csv").open("w", newline="", encoding="utf-8") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["arm", "reading", "pairs", "rise_points", "interval_low", "interval_high",
                       "problems_rose", "problems_unchanged", "problems_fell"])
        for (arm, kind), r in risen.items():
            rows.writerow([arm, ARMS[arm], kind, points(r["mean"]), points(r["low"]), points(r["high"]),
                           r["rose"], r["level"], r["fell"]])

    # --- problems.csv: a problem under a reading rule a row ---------------------------------------------------
    with (HERE / "problems.csv").open("w", newline="", encoding="utf-8") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["problem", "known_answer", "arm", "reading", "agents_right", "agents_wrong", "agents_no_answer"]
                      + [f"pairs_{kind}" for kind in KINDS] + ["most_held_wrong_answer", "agents_on_it"])
        for problem in problems:
            for arm, reading in ARMS.items():
                how = ended(arm, problem)
                answer, on_it = most_held_wrong(arm, problem)
                rows.writerow([problem, truth[problem], arm, reading, how["right"], how["wrong"], how["no answer"]]
                              + [kinds[arm, problem][kind] for kind in KINDS] + [answer, on_it])

    # --- answers.csv: an agent a row --------------------------------------------------------------------------
    with (HERE / "answers.csv").open("w", newline="", encoding="utf-8") as out:
        rows = csv.writer(out, lineterminator="\n")
        rows.writerow(["problem", "known_answer", "arm", "reading", "agent", "answer", "ended"])
        for problem in problems:
            for arm, reading in ARMS.items():
                for agent, answer in enumerate(final[arm, problem]):
                    rows.writerow([problem, truth[problem], arm, reading, agent,
                                   "" if answer is None else answer, outcome(answer, problem)])

    # --- tables.md: the tables of the README ------------------------------------------------------------------
    all_pairs = a_problem * len(problems)
    densest = list(ARMS)[-1]

    def cell(arm, kind, bold=False):
        text = f"{percent(share[arm][kind])}%"
        return f"**{text}** ({total[arm][kind]} of {all_pairs})" if bold else f"{text} ({total[arm][kind]})"

    def code(text):
        return "`" + str(text).replace("|", "\\|") + "`"

    lines = [
        "<!-- Written by results/make_tables.py from the logs in runs/. Change the script, not this file. -->",
        "",
        "## Headline",
        "",
        "| share of agent pairs | without peer reading | with peer reading (a peer's file after every step) |",
        "|---|---|---|",
        f"| gave the same wrong answer | {cell(BASELINE, 'same_wrong', True)} | {cell(densest, 'same_wrong', True)} |",
        f"| gave the same right answer | {cell(BASELINE, 'both_right', True)} | {cell(densest, 'both_right', True)} |",
        "",
        "## By how often an agent reads",
        "",
        "| " + " | ".join([f"{len(problems)} problems, {agents} agents a problem"] + list(ARMS.values())) + " |",
        "|---|---|---|---|",
        "| after one of its steps, an agent reads a peer's file | "
        + " | ".join("never" if chance(arm) == 0 else "every time" if chance(arm) == 1
                     else f"with a chance of 1 in {1 / chance(arm):g}" for arm in ARMS) + " |",
        "| files read, by how many of the agents | "
        + " | ".join(f"{files_read[arm]:,}, by {readers[arm]}" if files_read[arm] else "none" for arm in ARMS) + " |",
    ]
    for kind, label in KINDS.items():
        name = f"**pairs: {label}**" if kind in ("both_right", "same_wrong") else f"pairs: {label}"
        lines.append(f"| {name} | " + " | ".join(cell(arm, kind) for arm in ARMS) + " |")
    for how, label in (("right", "agents that ended right"), ("wrong", "agents that ended on a wrong answer"),
                       ("no answer", "agents that ended with no answer")):
        lines.append(f"| {label} | " + " | ".join(
            f"{percent(people_share[arm][how])}% ({people[arm][how]})" for arm in ARMS) + " |")
    lines += [
        "",
        f"A percent of pairs is of a problem's {a_problem} pairs, averaged over the {len(problems)} problems, and the "
        f"count beside it is of all {all_pairs} pairs. A percent of agents is of a problem's {agents} agents, averaged "
        f"over the problems, and the count is of all {agents * len(problems)} agents.",
        "",
        "## Against no peer reading, problem by problem",
        "",
        "| the rise in a problem's pairs, in points | " + " | ".join(ARMS[arm] for arm in ARMS if arm != BASELINE) + " |",
        "|---|---|---|",
    ]
    for kind in ("same_wrong", "both_right"):
        lines.append(f"| pairs: {KINDS[kind]} | " + " | ".join(
            f"{points(risen[arm, kind]['mean'])} ({points(risen[arm, kind]['low'])} to {points(risen[arm, kind]['high'])})"
            for arm in ARMS if arm != BASELINE) + " |")
    lines.append("| problems on which the pairs on the same wrong answer rose, stayed, fell | " + " | ".join(
        f"{risen[arm, 'same_wrong']['rose']}, {risen[arm, 'same_wrong']['level']}, {risen[arm, 'same_wrong']['fell']}"
        for arm in ARMS if arm != BASELINE) + " |")
    each = risen[densest, "same_wrong"]["each"]
    largest = sorted(range(len(problems)), key=lambda i: -each[i])[:6]
    lines += [
        "",
        f"In brackets, a 95% interval over the {len(problems)} problems (the problems drawn again with replacement, "
        f"{RESAMPLES:,} times).",
        "",
        f"With a peer's file after every step, the six largest rises in the pairs on the same wrong answer (problems "
        f"{', '.join(str(problems[i]) for i in largest)}) are {100 * sum(each[i] for i in largest) / len(problems):.1f} "
        f"of the {100 * risen[densest, 'same_wrong']['mean']:.1f} points.",
        "",
        "## Problem by problem",
        "",
        f"For each problem, three numbers in the order of the columns above: {', '.join(ARMS.values())}.",
        "",
        f"| problem | known answer | agents right, of {agents} | pairs on the same wrong answer, of {a_problem} "
        f"| agents on the most-held wrong answer |",
        "|---|---|---|---|---|",
    ]
    for problem in problems:
        lines.append(
            f"| {problem} | {code(truth[problem])} "
            f"| {', '.join(str(ended(arm, problem)['right']) for arm in ARMS)} "
            f"| {', '.join(str(kinds[arm, problem]['same_wrong']) for arm in ARMS)} "
            f"| {', '.join(str(most_held_wrong(arm, problem)[1]) for arm in ARMS)} |")

    models = sorted({call["model"] for call in engine})
    servers = sorted({(call["engine"]["backend"], call["engine"].get("vllm") or "", call["engine"]["served_as"],
                       call["engine"]["machine"]) for call in engine})
    setting = settings[BASELINE]
    same_but_looks = all({k: v for k, v in settings[arm].items() if k not in ("name", "looks", "contact")}
                         == {k: v for k, v in setting.items() if k not in ("name", "looks", "contact")} for arm in ARMS)
    assert same_but_looks, "the arms differ in more than who reads"
    lines += [
        "",
        "## The run",
        "",
        "| | |",
        "|---|---|",
        f"| model | {', '.join(code(model) for model in models)} |",
        "| served by | " + "; ".join(f"{backend} {version}, as {code(name)}, on one {machine}"
                                      for backend, version, name, machine in servers) + " |",
        f"| started, finished | {config['started']}, {config['finished']} |",
        f"| problems | {', '.join(map(str, problems))} of `{config['settings']['benchmarks'][0]}` |",
        f"| seed | {config['settings']['seed']} |",
        f"| agents a problem | {agents} |",
        f"| steps an agent has | {setting['steps']} |",
        f"| tokens of thought a step, at most | {setting['thinking']:,} |",
        f"| tokens of reply a step, at most | {setting['max_tokens']:,} |",
        f"| lines a file may have | {setting['lines']} |",
        f"| how a reply is drawn | temperature {setting['sampling']['temperature']}, top-k {setting['sampling']['top_k']}, "
        f"top-p {setting['sampling']['top_p']} (a thought: temperature {setting['thought_sampling']['temperature']}, "
        f"presence penalty {setting['thought_sampling']['presence_penalty']}) |",
        "| model calls | " + ", ".join(f"{sum(episodes[arm, p]['calls'] for p in problems):,}" for arm in ARMS) + " |",
        "| tokens the model wrote | " + ", ".join(f"{sum(episodes[arm, p]['tokens'] for p in problems):,}" for arm in ARMS) + " |",
        f"| commit of the code | `{config['git']['commit'][:12]}`, with "
        f"{'uncommitted changes' if config['git']['uncommitted_changes'] else 'nothing uncommitted'} |",
        "",
        f"The three arms have the same settings but for who reads. Where a row has three numbers, they are in the order: "
        f"{', '.join(ARMS.values())}.",
        "",
    ]
    (HERE / "tables.md").write_text("\n".join(lines), encoding="utf-8")

    for arm in ARMS:
        assert sum(total[arm].values()) == all_pairs and sum(people[arm].values()) == agents * len(problems)
    print(f"{len(episodes)} problems under an arm, {len(looks):,} looks and {len(engine)} engine records read from {RUN}")
    for arm, reading in ARMS.items():
        print(f"  {reading}: {percent(share[arm]['same_wrong'])}% of pairs on the same wrong answer, "
              f"{percent(share[arm]['both_right'])}% both right")
    print("wrote pairs.csv, change.csv, problems.csv, answers.csv and tables.md in", HERE)


if __name__ == "__main__":
    main()
