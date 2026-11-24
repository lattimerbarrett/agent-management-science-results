"""The result tables, rebuilt from the logs in runs/. No keys, no model calls, standard library only.

    python results/make_tables.py

Reads results/runs.json (which runs belong to which month and system) and results/archive_grades.json (the grade of
each answer a full-system team was told, against the reference answer), and writes:

    results/tables.md              the tables the README shows
    results/runs.csv               every lone-agent run, team run and told-team run, a run a row
    results/full_system.csv        the full system, a problem a row
    results/full_system_teams.csv  every proof team the full system started, a team a row

What "solved" means here is in the README.
"""

import csv
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
OUT = ROOT / "results"
NUDGES = ("@channel Stopping isn't an option without proving the result", "Stopping isn't an option without proving the result")
LEAD = "lead"  # who posts a nudge (slack.HUMAN)


def load(path):
    return json.loads(path.read_text()) if path.exists() else None


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def one_line(text, n=None):
    text = " ".join(str(text).split())
    return text if n is None or len(text) <= n else text[: n - 1] + "…"


def money(x):
    return f"${x:,.2f}"


# ---- lone agents, teams, told teams: one run each ---------------------------------------------------------


def sweep_runs(names):
    """{problem: [run, ...]} over the sweeps named, in order (a problem's first run first)."""
    out = {}
    for name in names:
        sweep = load(RUNS / "basin" / "untold" / name / "sweep.json")
        for p, runs in sweep["runs"].items():
            out.setdefault(int(p), []).extend([runs] if isinstance(runs, str) else runs)
    return out


def swarm_run(month, system, p, i, run):
    """A run's row. For a lone agent or a team: its reading (reading.json), written when the run ended. For a told
    team: the verifier's read of it (runs/stopbench)."""
    folder = RUNS / "basin" / "swarm" / run
    settings, summary, r = load(folder / "settings.json"), load(folder / "summary.json") or {}, load(folder / "reading.json")
    row = {"month": month, "system": system, "problem": f"p{p % 100}", "run_no": i, "folder": f"runs/basin/swarm/{run}",
           "agents": settings["n"], "cost": round(summary.get("cost") or 0.0, 4), "ended": summary.get("reason"),
           "nudges": sum(m["sender"] == LEAD and m["body"] in NUDGES for m in jsonl(folder / "slack.jsonl"))}
    if system == "told":
        v = jsonl(RUNS / "stopbench" / "results" / "verify" / f"swarm__{run}.jsonl")[0]
        row.update(answer="(told the reference answer)", definite=v.get("definite"), verdict=v.get("verdict"),
                   gap_acknowledged=v.get("acknowledged"), stop=v["stop"], right=True, solved=v["stop"])
    elif r is not None:
        v = r.get("verify") or {}
        row.update(answer=one_line(r["answer"]) if r.get("answer") else "", definite=r.get("definite"),
                   procedure=r.get("procedure", False), verdict=v.get("verdict"), gap_acknowledged=v.get("acknowledged"),
                   stop=r["stop"], right=r["correct"] is True, restated=r.get("restated", False), solved=r["solved"],
                   reading_cost=r.get("cost"))
    return row


# ---- the full system: one archive a problem (p41 of September: an archive and its continuation) ----------------


def minutes(folder, state, first=True):
    """From the first explorer's start to the last thing the archive recorded. A continuation (`first` False) starts
    from an earlier archive's saved state, so it is timed from its own first call."""
    times = [c["time"] for c in jsonl(folder / "calls.jsonl") if c.get("time")]
    times += [n["created"] for n in state["nodes"]] if first else []
    times += [e[k] for e in state["experiments"] for k in ("started", "ended_at", "read_at")
              if e.get(k) and (first or (folder / e["id"]).is_dir())]  # fmt: skip
    return (max(times) - min(times)) / 60 if times else None


def full_system(month, p, archives, grades):
    """A problem's row and its teams' rows. The proof the system stopped on is the experiment its stopping rule
    accepted (state.json: `manager.new`). An archive of 4 to 6 November ran under the earlier rule (the manager). The
    verifier read those teams' saved records afterwards: runs/stopbench, and for September p41's e7, which the stop
    bench doesn't have, the team's own verify/result.json. Such a problem is solved only if the verifier accepted the
    proof afterwards. Where the manager accepted none, the proof is the one the verifier accepted afterwards."""
    teams, cost, mins, explorers, accepted, judge = [], 0.0, 0.0, 0, None, None
    for archive in archives:
        folder = RUNS / "archive" / archive
        state, settings = load(folder / "state.json"), load(folder / "settings.json")
        cost += state["spent"]
        mins += minutes(folder, state, first=archive == archives[0]) or 0.0
        later = {v["id"].split("/")[-1]: v for v in jsonl(RUNS / "stopbench" / "results" / "verify" / f"archive__{archive}.jsonl")}
        rule = settings.get("stop_rule") or "manager"
        explorers += len(state["nodes"]) if archive == archives[0] else 0  # a continuation explores no further
        for e in state["experiments"]:
            if not (folder / e["id"]).is_dir():  # never started here: queued when the archive ended, or run elsewhere
                continue
            g, v, m = grades.get(f"{archive}/{e['id']}", {}), e.get("verify") or {}, e.get("manager") or {}
            after = later.get(e["id"]) or load(folder / e["id"] / "verify" / "result.json") or {}
            team = {"month": month, "problem": f"p{p % 100}", "folder": f"runs/archive/{archive}/{e['id']}",
                    "told": one_line(e["answer"]), "right": g.get("correct"), "graded_by": g.get("by"),
                    "cost": round(e.get("cost") or 0.0, 4), "ended": e.get("reason"),
                    "report": (e.get("report") or {}).get("status"), "rule": rule,
                    "accepted": m.get("new") is True, "verdict": v.get("verdict"),
                    "gap_acknowledged": v.get("acknowledged"),
                    "verifier_afterwards": after.get("verdict") if rule == "manager" else None,
                    "stop_afterwards": after.get("stop") if rule == "manager" else None}
            teams.append(team)
            if team["accepted"] and accepted is None:
                accepted = team
                judge = ("the verifier" if rule == "verify" else
                         "the manager, and the verifier afterwards" if team["stop_afterwards"] else "the manager")
    if accepted is None:  # an archive under the earlier rule: the verifier's later read of its teams
        accepted = next((t for t in teams if t["stop_afterwards"]), None)
        judge = "the verifier, afterwards" if accepted else None
    state = load(RUNS / "archive" / archives[-1] / "state.json")
    row = {"month": month, "problem": f"p{p % 100}", "folders": " + ".join(f"runs/archive/{a}" for a in archives),
           "ended": one_line(state["reason"], 60), "cost": round(cost, 4), "minutes": round(mins), "explorers": explorers,
           "teams": len(teams), "right_answer_told": next((i for i, t in enumerate(teams, 1) if t["right"]), None),
           "accepted": accepted["folder"].split("/")[-1] if accepted else None, "accepted_by": judge,
           "answer": accepted["told"] if accepted else None, "right": accepted["right"] if accepted else None,
           "solved": bool(accepted and accepted["right"] and (accepted["rule"] == "verify" or accepted["stop_afterwards"]))}
    return row, teams


# ---- the tables ---------------------------------------------------------------------------------------


def write_csv(name, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def cell(rows):
    """One system's cell for a problem: a single run's outcome and cost, or how many of several runs solved it."""
    if not rows:
        return "—"
    if len(rows) == 1 and rows[0]["system"] != "lone":
        r = rows[0]
        return ("**solved**" if r["solved"] else "not solved") + f" · {money(r['cost'])}"
    return f"{sum(r['solved'] for r in rows)} of {len(rows)}"


def month_table(month, spec, runs, full):
    told = "told" in spec
    head = ["problem", "lone agent, runs solved", "one team of four", "full system"] + (["team handed the answer"] if told else [])
    lines = ["| " + " | ".join(head) + " |", "|---|" + "---|" * (len(head) - 1)]
    by = lambda system, p: [r for r in runs if (r["month"], r["system"], r["problem"]) == (month, system, f"p{p % 100}")]  # noqa: E731
    for p in spec["problems"]:
        f = next(r for r in full if (r["month"], r["problem"]) == (month, f"p{p % 100}"))
        row = [f"p{p % 100}", cell(by("lone", p)), cell(by("team", p)),
               ("**solved**" if f["solved"] else "not solved") + f" · {money(f['cost'])}"]
        lines.append("| " + " | ".join(row + ([cell(by("told", p))] if told else [])) + " |")
    n = len(spec["problems"])
    lone = [r for r in runs if (r["month"], r["system"]) == (month, "lone") and int(r["problem"][1:]) in [p % 100 for p in spec["problems"]]]
    first = [r for r in lone if r["run_no"] == 1]
    any_ = {r["problem"] for r in lone if r["solved"]}
    team = [r for r in runs if (r["month"], r["system"]) == (month, "team")]
    fs = [r for r in full if r["month"] == month]
    total = [f"**{n} problems**",
             f"**{len(any_)} of {n}** by any run ({sum(r['solved'] for r in first)} of {n} on the first run; "
             f"{sum(r['solved'] for r in lone)} of {len(lone)} runs) · {spend(lone, 'a run')}",
             f"**{sum(r['solved'] for r in team)} of {n}** · {spend(team)}",
             f"**{sum(r['solved'] for r in fs)} of {n}** · {spend(fs)}"]
    if told:
        t = [r for r in runs if (r["month"], r["system"]) == (month, "told")]
        total.append(f"{sum(r['solved'] for r in t)} of {n} · {spend(t)}")
    lines.append("| " + " | ".join(total) + " |")
    return lines


def spend(rows, each=""):
    """A column's cost in a table's last row: the median first, then the sum."""
    return f"median {money(median(r['cost'] for r in rows))}{' ' + each if each else ''} · {money(sum(r['cost'] for r in rows))} in all"


def cost_table(spec, runs, full):
    """What a problem cost (for the lone agent, a run), a system and a month a row. The median comes first: a few
    problems cost many times the rest, so the mean says little about what a problem usually costs."""
    lines = ["| cost | median | mean | least | most | in all |", "|---|---|---|---|---|---|"]
    picked = {}
    for system, label in (("full", "Full system, a problem"), ("team", "One team of four, a problem"), ("lone", "Lone agent, a run")):
        for month, s in spec.items():
            listed = [f"p{p % 100}" for p in s["problems"]]
            rows = ([r for r in full if r["month"] == month] if system == "full" else
                    [r for r in runs if (r["month"], r["system"]) == (month, system) and r["problem"] in listed])
            picked[system, month] = rows
            c = [r["cost"] for r in rows]
            lines.append(f"| {label} · {month.capitalize()}{f' ({len(rows)} runs)' if system == 'lone' else ''} | "
                         + " | ".join(money(x) for x in (median(c), mean(c), min(c), max(c), sum(c))) + " |")
    months = list(spec)
    solved = [[r["cost"] for r in picked["full", m] if r["solved"]] for m in months]
    missed = [r for m in months for r in picked["full", m] if not r["solved"]]
    assert all(r["ended"] == "stopped" for r in missed)  # none of them ran out its budget: a person stopped each
    lines += ["", "A problem the full system solved cost a median of "
              + " and ".join(f"{money(median(c))} in {m.capitalize()}" for m, c in zip(months, solved))
              + f". The {len(missed)} it did not solve ran until a person stopped them, at "
              f"{money(min(r['cost'] for r in missed))} to {money(max(r['cost'] for r in missed))}."]
    return lines


def main():
    spec = load(OUT / "runs.json")
    grades = load(OUT / "archive_grades.json")
    runs, full, teams = [], [], []
    for month, s in spec.items():
        for system in ("lone", "team"):
            for p, ids in sweep_runs(s[system]["sweeps"]).items():
                runs += [swarm_run(month, system, p, i, run) for i, run in enumerate(ids, 1)]
        for p, run in s.get("told", {}).items():
            runs.append(swarm_run(month, "told", int(p), 1, run))
        for p, archives in s["full"].items():
            row, ts = full_system(month, int(p), archives, grades)
            full.append(row)
            teams += ts
    write_csv("runs.csv", runs)
    write_csv("full_system.csv", full)
    write_csv("full_system_teams.csv", teams)

    def top(month, system):
        n = len(spec[month]["problems"])
        if system == "full":
            rows = [r for r in full if r["month"] == month]
            return f"**{sum(r['solved'] for r in rows)} of {n}** · median {money(median(r['cost'] for r in rows))} a problem"
        listed = [f"p{p % 100}" for p in spec[month]["problems"]]
        rows = [r for r in runs if (r["month"], r["system"]) == (month, system) and r["problem"] in listed]
        if system == "team":
            return f"**{sum(r['solved'] for r in rows)} of {n}** · median {money(median(r['cost'] for r in rows))} a problem"
        first = [r for r in rows if r["run_no"] == 1]
        per = max(r["run_no"] for r in rows)
        return (f"**{sum(r['solved'] for r in first)} of {n}** on the first run · **{len({r['problem'] for r in rows if r['solved']})} "
                f"of {n}** by any of up to {per} runs · median {money(median(r['cost'] for r in rows))} a run")

    out = ["## Headline", "",
           "| problems solved | September, 9 problems | October, 14 problems |", "|---|---|---|",
           f"| **Full system** (explore, then a team of four on each candidate answer) | {top('september', 'full')} | {top('october', 'full')} |",
           f"| **One team of four**, given only the problem | {top('september', 'team')} | {top('october', 'team')} |",
           f"| **Lone agent**, given only the problem | {top('september', 'lone')} | {top('october', 'lone')} |", ""]
    every = [r for r in runs if r["month"] == "october" and r["system"] == "lone" and r["run_no"] == 1]
    out += [f"On all {len(every)} October problems, one lone agent each solved **{sum(r['solved'] for r in every)} of {len(every)}** "
            f"(median {money(median(r['cost'] for r in every))} a run, {money(sum(r['cost'] for r in every))} in all).", ""]
    for month, s in spec.items():
        out += [f"## {month.capitalize()}, problem by problem", ""] + month_table(month, s, runs, full) + [""]
    out += ["## Cost", ""] + cost_table(spec, runs, full) + [""]
    (OUT / "tables.md").write_text("\n".join(out))
    print("\n".join(out))
    stops = [r for r in runs if r.get("stop") and not r["solved"]]
    print(f"{len(runs)} runs, {len(full)} full-system problems, {len(teams)} proof teams; stops on an answer that isn't the "
          f"reference's: {len(stops)} ({', '.join(sorted({r['month'][:3] + ' ' + r['system'] + ' ' + r['problem'] for r in stops}))})")


if __name__ == "__main__":
    main()
