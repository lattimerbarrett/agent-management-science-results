"""A sweep of prover archives: one archive a problem, started through the server a few at a time (so the archive page
shows them), then each archive's outcome graded against the reference answer, which no archive sees.

    op-env uv run python archive_sweep.py start --october [--budget 100] [--exp-budget 20] [--max-live 3] [--name NAME]
                                                [--stop-dead-ends]
    op-env uv run python archive_sweep.py start --problems 1011 1013 --adopt 20261123-012828-p1045   # a run already going
    op-env uv run python archive_sweep.py show [--name NAME]

`start` keeps at most `--max-live` archives live on the server (every live archive counts, the sweep's or not) and
starts a problem as one ends; run again, it goes on. An archive the server no longer has and that never ended (the
server restarted) is started once more, once. `--adopt` puts archives that are already running or saved into the
sweep, with the settings they have.

It pauses itself when the swarms' budget looks too small: once more than `--pause-after` archives (4) have told a
swarm the right answer and that swarm ran out of its budget without the proof, no further archive is started (the
ones running go on to their end). For this the driver grades, as it goes, the answer of each swarm that ran out.

`--stop-dead-ends` saves money and nothing else. A dead end is an archive that told a swarm the right answer and whose
swarm ended without the proof: an answer gets one swarm, so the archive can't solve its problem any more, and until
now it went on exploring to its budget. With the flag the driver grades each answer as it is told and stops such an
archive (the page's Stop), noting it in sweep.json (`dead_ends`). The archive sees nothing of this: the grade stays
out here, and nothing in explorer/ knows of it. It changes no solve, but what the archive would have gone on to do
is then not seen, a false stop included, so a sweep run with it shows fewer swarms on wrong answers.

An archive solves its problem when it ends on a proof (the verifier's stop) of an answer that is right. `show` grades
every answer a swarm was told (grading.Grader: MathArena's judge, then whether the answer is the question restated),
so the table also says where the right answer was in the queue and what came of its swarm.

A sweep is kept in runs/archive-sweep/<name>/ (sweep.json, summary.md); the runs are archives, in runs/archive/.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "explorer"))

import benchmark  # noqa: E402
import prover_archive as pa  # noqa: E402

OUT = ROOT / "runs" / "archive-sweep"
PORT = int(os.environ.get("SERVE_PORT", 8765))
NAME = "v1"
BUDGET, EXP_BUDGET, MAX_LIVE = 100.0, 20.0, 3  # dollars an archive, dollars a swarm, archives at once on the server
PAUSE_AFTER = 4  # no new archive once more than this many had the right answer run out of its swarm's budget
POLL, STATUS_EVERY = 20, 900
JUDGE_MODEL = "gpt-6.1-sol"  # the grader's, as swarm_untold's


def api(path, body=None):
    """The server's reply (explorer/serve.py), {"error": ...} for a request it turns down. OSError if it isn't there."""
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=None if body is None else json.dumps(body).encode())
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def load(name):
    path = OUT / name / "sweep.json"
    return json.loads(path.read_text()) if path.exists() else None


def save(sweep):
    folder = OUT / sweep["name"]
    folder.mkdir(parents=True, exist_ok=True)
    tmp = folder / "sweep.json.tmp"
    tmp.write_text(json.dumps(sweep, indent=1))
    tmp.replace(folder / "sweep.json")


def state_of(run):
    path = pa.OUT / run / "state.json"
    try:
        return json.loads(path.read_text()) if path.exists() else None
    except ValueError:  # being written
        return None


def graded(kept, grader, bench, p, run, e):
    """The grade of the answer experiment `e` of `run` was told, asked once (kept in the sweep's grades.json)."""
    key = f"{run}/{e['id']}"
    if key not in kept and grader is not None:
        g = grader.grade(bench.get_problem(p), e["answer"])
        kept[key] = {"correct": g.correct, "restated": g.restated is True, "note": g.note}
    return kept.get(key) or {}


def short(st, kept, grader, bench, p, run):
    """The experiments of an archive that were told the right answer and whose swarm ran out of its budget without
    the proof: the sign that a swarm's budget is too small."""
    out = []
    for e in (st or {}).get("experiments", []):
        if e["status"] == "ended" and str(e.get("reason") or "").startswith("budget") and not (e.get("manager") or {}).get("new"):
            if graded(kept, grader, bench, p, run, e).get("correct"):
                out.append(e["id"])
    return out


def dead_end(st, grade):
    """The experiments that make a running archive a dead end, [] when it isn't one: each was told a right answer and
    its swarm is over without the stop, and no swarm on a right answer is still to come or to end. An answer gets one
    swarm, so the archive can't end on the right answer any more. `grade(e)`: the grade of the answer `e` was told.
    A swarm that the archive's own end cut off or kept from starting doesn't count: the archive is ending anyway."""
    if not st or st.get("ended") or st.get("reason"):
        return []
    right = [e for e in st.get("experiments", []) if grade(e).get("correct")]
    over = [e for e in right if e["status"] == "ended" and e.get("started") and not (e.get("manager") or {}).get("new")
            and not str(e.get("reason") or "").startswith(("the archive ended", "not started"))]  # fmt: skip
    return [e["id"] for e in over] if right and len(over) == len(right) else []


def stop_dead_ends(sweep, live, grade, stop):
    """Stops each live archive of the sweep that is a dead end (`stop(run)`) and notes it in sweep["dead_ends"]: what
    it had spent, and the experiments told the right answer. The problems stopped. `grade(p, run, e)` as in dead_end."""
    stopped = []
    for p, run in sweep["runs"].items():
        st = state_of(run)
        if run not in live or p in sweep.get("dead_ends", {}):
            continue
        if ids := dead_end(st, lambda e: grade(int(p), run, e)):
            if (stop(run) or {}).get("error"):  # the server no longer has it: it ended in the meantime
                continue
            sweep.setdefault("dead_ends", {})[p] = {"run": run, "exps": ids, "spent": round(st.get("spent") or 0.0, 4),
                                                    "time": time.time()}  # fmt: skip
            stopped.append(p)
    return stopped


def start(args):
    if args.stop_dead_ends and args.no_grade:
        raise SystemExit("--stop-dead-ends needs the grader: it can't go with --no-grade")
    sweep = load(args.name) or {"name": args.name, "settings": {"budget": args.budget, "exp_budget": args.exp_budget},
                                "runs": {}, "earlier": {}, "adopted": [], "started": time.time()}  # fmt: skip
    s = sweep["settings"]
    if (s["budget"], s["exp_budget"]) != (args.budget, args.exp_budget):
        raise SystemExit(f"sweep {args.name} has ${s['budget']:g} an archive and ${s['exp_budget']:g} a swarm: use "
                         "another --name")  # fmt: skip
    for run in args.adopt or []:
        st = state_of(run)
        if st is None:
            raise SystemExit(f"no archive run {run}")
        sweep["runs"][str(st["problem"])] = run
        if run not in sweep["adopted"]:
            sweep["adopted"].append(run)
    problems = sorted(set(args.problems or (benchmark.OCTOBER if args.october else [])) | {int(p) for p in sweep["runs"]})
    if bad := [p for p in problems if p not in pa.PROBLEMS]:
        raise SystemExit(f"problems the archive doesn't offer: {bad} (prover_archive.PROBLEMS)")
    save(sweep)
    print(f"sweep {args.name}: {len(problems)} problems, at most {args.max_live} archives live, ${s['budget']:g} an "
          f"archive and ${s['exp_budget']:g} a swarm", flush=True)  # fmt: skip
    grader = bench = None
    if not args.no_grade and (args.pause_after or args.stop_dead_ends):
        from grading import Grader
        from llm import openai_client

        grader, bench = Grader(openai_client(), judge_model=JUDGE_MODEL), benchmark.Benchmark()
    grades = OUT / sweep["name"] / "grades.json"
    kept = json.loads(grades.read_text()) if grades.exists() else {}
    if args.stop_dead_ends:
        print("dead ends are stopped: an archive whose swarm on the right answer ended without the proof", flush=True)
    noted, last, paused = set(), 0.0, False
    while True:
        try:
            live = {r["id"] for r in api("/api/archive/runs") if r.get("live")}
        except OSError:
            print("no answer from the server; waiting for it", flush=True)
            time.sleep(POLL)
            continue
        running = 0
        for p in problems:
            run = sweep["runs"].get(str(p))
            if run is None:
                continue
            st = state_of(run)
            if run in live:
                running += 1
            elif st and st.get("ended"):
                if run not in noted:
                    noted.add(run)
                    print(f"{time.strftime('%H:%M')} p{p}: {run} ended ({st.get('reason')}), ${st.get('spent') or 0:.2f}, "
                          f"{len(st['experiments'])} experiments", flush=True)  # fmt: skip
            elif run not in noted:  # the server no longer has it and it never ended
                noted.add(run)
                if sweep["earlier"].get(str(p)):
                    print(f"p{p}: {run} was cut off again; left as it is", flush=True)
                else:
                    print(f"p{p}: {run} was cut off (the server restarted); starting the problem once more", flush=True)
                    sweep["earlier"].setdefault(str(p), []).append(run)
                    del sweep["runs"][str(p)]
                    save(sweep)
        if grader is not None and args.stop_dead_ends:  # only to save money (see the docstring)
            before = set(sweep.get("dead_ends", {}))
            try:
                stop_dead_ends(sweep, live, lambda p, run, e: graded(kept, grader, bench, p, run, e),
                               lambda run: api("/api/archive/stop", {"id": run}))  # fmt: skip
            except Exception as e:  # the grader's call failed, or the server's: tried again at the next round
                print(f"stopping dead ends failed ({e!r}); going on", flush=True)
            for p in sorted(set(sweep.get("dead_ends", {})) - before):  # those stopped before a call failed, too
                d = sweep["dead_ends"][p]
                save(sweep)
                print(f"{time.strftime('%H:%M')} p{p}: {d['run']} stopped at ${d['spent']:.2f}, a dead end: the swarm "
                      f"told the right answer ({' '.join(d['exps'])}) ended without the proof", flush=True)  # fmt: skip
            grades.write_text(json.dumps(kept, indent=1))
        if grader is not None and args.pause_after and not paused:  # is a swarm's budget too small? (see the docstring)
            try:
                found = {p: ids for p in problems if (run := sweep["runs"].get(str(p)))
                         and (ids := short(state_of(run), kept, grader, bench, p, run))}  # fmt: skip
                grades.write_text(json.dumps(kept, indent=1))
            except Exception as e:  # the grader's call failed: asked again at the next round
                print(f"grading failed ({e!r}); going on", flush=True)
                found = {}
            if len(found) > args.pause_after:
                paused = True
                print(f"{time.strftime('%H:%M')} PAUSED: no further archive is started. On {len(found)} problems a swarm "
                      f"was told the right answer and ran out of its ${s['exp_budget']:g} without the proof: "
                      + ", ".join(f"p{p} ({' '.join(ids)})" for p, ids in found.items()), flush=True)  # fmt: skip
        todo = [] if paused else [p for p in problems if str(p) not in sweep["runs"]]
        for p in todo[: max(0, args.max_live - len(live))]:
            got = api("/api/archive/run", {"problem": p, "settings": {"budget": s["budget"], "exp_budget": s["exp_budget"]}})
            if not got.get("id"):
                raise SystemExit(f"p{p}: the server didn't start it: {got}")
            sweep["runs"][str(p)] = got["id"]
            save(sweep)
            running += 1
            print(f"{time.strftime('%H:%M')} p{p}: started {got['id']}", flush=True)
        if not running and (paused or not [p for p in problems if str(p) not in sweep["runs"]]):
            break
        if time.time() - last > STATUS_EVERY:
            last = time.time()
            ended = sum(bool((st := state_of(r)) and st.get("ended")) for r in sweep["runs"].values())
            print(f"{time.strftime('%H:%M')} {running} running, {ended} ended of {len(problems)}", flush=True)
        time.sleep(POLL)
    show(args)


def measured(p, run, grader, bench, kept, dead=None):
    """An archive's row: how it ended, each answer a swarm was told with its grade and what came of the swarm.
    `dead`: the sweep's note of the driver stopping this problem's archive as a dead end, if it did."""
    st = state_of(run)
    if st is None:
        return None
    if not (dead and dead.get("run") == run and st.get("reason") == "stopped"):  # another run, or it ended otherwise
        dead = None
    exps = []
    for e in st["experiments"]:
        v, g = e.get("verify") or {}, graded(kept, grader, bench, p, run, e)
        exps.append({"id": e["id"], "answer": e["answer"], "correct": g.get("correct"), "restated": g.get("restated"),
                     "by": g.get("by"), "status": e["status"], "report": (e.get("report") or {}).get("status"), "verdict": v.get("verdict"),
                     "acknowledged": v.get("acknowledged"), "stop": bool((e.get("manager") or {}).get("new")),
                     "cost": e.get("cost") or 0.0, "reason": e.get("reason")})  # fmt: skip
    stopped = next((e for e in exps if e["stop"]), None)
    right = next((i for i, e in enumerate(exps) if e["correct"]), None)
    created = [n["created"] for n in st["nodes"]]
    minutes = ((pa.OUT / run / "state.json").stat().st_mtime - min(created)) / 60 if created and st.get("ended") else None
    return {"problem": p, "run": run, "ended": st.get("ended"), "reason": st.get("reason"), "spent": st.get("spent") or 0.0,
            "agents": len(st["nodes"]), "minutes": minutes, "exps": exps, "stopped": stopped, "dead": dead,
            "solved": bool(stopped and stopped["correct"]), "false_stop": bool(stopped and not stopped["correct"]),
            "right": None if right is None else right + 1, "budget": (st.get("settings") or {}).get("budget")}  # fmt: skip


def show(args):
    sweep = load(args.name)
    if sweep is None:
        raise SystemExit(f"no sweep {args.name} in {OUT}")
    grader = bench = None
    if not args.no_grade:
        from grading import Grader
        from llm import openai_client

        grader, bench = Grader(openai_client(), judge_model=JUDGE_MODEL), benchmark.Benchmark()
    path = OUT / sweep["name"] / "grades.json"
    kept = json.loads(path.read_text()) if path.exists() else {}
    rows = [r for p, run in sorted(sweep["runs"].items(), key=lambda kv: int(kv[0]))
            if (r := measured(int(p), run, grader, bench, kept, sweep.get("dead_ends", {}).get(p)))]  # fmt: skip
    path.write_text(json.dumps(kept, indent=1))
    s = sweep["settings"]
    cell = lambda text, n=70: "`" + " ".join(str(text).split())[:n].replace("|", "\\|").replace("`", "'") + "`"  # noqa: E731
    mark = lambda e: ("right" if e["correct"] else "the question restated" if e["restated"] else  # noqa: E731
                      "wrong" if e["correct"] is False else "ungraded") + (", by hand" if e["by"] == "hand" else "")  # fmt: skip
    came = lambda e: ("proved, the archive ended" if e["stop"] else  # noqa: E731
                      f"{(e['report'] or 'not read').lower()}" + (f", verifier: {e['verdict']}" if e["verdict"] else "")
                      + (", a gap acknowledged" if e["acknowledged"] else "") if e["status"] == "ended" else e["status"])  # fmt: skip
    out = [f"# Prover archives: sweep {sweep['name']}", "",
           f"One prover archive a problem (${s['budget']:g} an archive, ${s['exp_budget']:g} a swarm; an adopted run has "
           f"its own). Solved: the archive ended on a proof (the verifier's stop) of an answer that is right. Each answer "
           f"a swarm was told is graded here, outside the archive; an answer that restates the question is wrong."
           + (" A grade marked \"by hand\" was compared with the reference by hand, not by the grader (grades.json's `by`)."
              if any(e["by"] == "hand" for r in rows for e in r["exps"]) else "")
           + (" A dead end was stopped by the driver (`--stop-dead-ends`), only to save money: a swarm had been told the "
              "right answer and had ended without the proof, and an answer gets one swarm, so the archive could no longer "
              "solve its problem. What it would have gone on to do, a false stop included, isn't known."
              if any(r["dead"] for r in rows) else ""), "",
           "| problem | outcome | ended | $ | minutes | agents | swarms | the right answer's place | ended on |",
           "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in rows:
        outcome = ("solved" if r["solved"] else "false stop" if r["false_stop"] else
                   f"not solved: a dead end, stopped by the driver at ${r['dead']['spent']:.2f}" if r["dead"] else
                   "not solved" if r["ended"] else "running, or cut off")  # fmt: skip
        out.append(f"| p{r['problem']} | {outcome} | {str(r['reason']).split(' (')[0] if r['ended'] else ''} | ${r['spent']:.2f} | "
                   + (f"{r['minutes']:.0f}" if r["minutes"] is not None else "") + f" | {r['agents']} | {len(r['exps'])} | "
                   + (str(r["right"]) if r["right"] else "never told") + " | "
                   + (f"{r['stopped']['id']}: {cell(r['stopped']['answer'])} ({mark(r['stopped'])})" if r["stopped"] else "")
                   + " |")  # fmt: skip
    done = [r for r in rows if r["ended"]]
    out += ["", f"Solved {sum(r['solved'] for r in done)} of {len(done)} ended archives ({len(rows)} problems); "
                f"{sum(r['false_stop'] for r in done)} ended on a wrong answer; the right answer was told to a swarm in "
                f"{sum(r['right'] is not None for r in done)}. They cost ${sum(r['spent'] for r in rows):.2f}."
                + (f" The driver stopped {n} as dead ends." if (n := sum(bool(r["dead"]) for r in rows)) else "")]  # fmt: skip
    out += ["", "## Each archive's swarms, in order", ""]
    for r in rows:
        out.append(f"- p{r['problem']} ({r['run']}): " + ("; ".join(
            f"{e['id']} {cell(e['answer'], 80)} ({mark(e)}): {came(e)}, ${e['cost']:.2f}" for e in r["exps"]) or "none"))  # fmt: skip
    text = "\n".join(out) + "\n"
    (OUT / sweep["name"] / "summary.md").write_text(text)
    print(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for cmd in ("start", "show"):
        sp = sub.add_parser(cmd)
        sp.add_argument("--name", default=NAME)
        sp.add_argument("--no-grade", action="store_true", help="grade nothing more (no keys needed)")
        if cmd == "start":
            sp.add_argument("--problems", type=int, nargs="+", help="default: the sweep's own")
            sp.add_argument("--october", action="store_true", help="the October list (benchmark.OCTOBER)")
            sp.add_argument("--adopt", nargs="+", help="archive runs, running or saved, to put in the sweep as they are")
            sp.add_argument("--budget", type=float, default=BUDGET, help="dollars an archive (everything in it)")
            sp.add_argument("--exp-budget", type=float, default=EXP_BUDGET, help="dollars a swarm")
            sp.add_argument("--max-live", type=int, default=MAX_LIVE, help="archives live on the server at once")
            sp.add_argument("--pause-after", type=int, default=PAUSE_AFTER, help="start no further archive once more "
                            "than this many had the right answer run out of its swarm's budget (0: never pause)")  # fmt: skip
            sp.add_argument("--stop-dead-ends", action="store_true", help="stop an archive once its swarm on the right "
                            "answer has ended without the proof: it can't solve the problem any more (saves money only)")  # fmt: skip
    args = ap.parse_args()
    {"start": start, "show": show}[args.cmd](args)


if __name__ == "__main__":
    main()
