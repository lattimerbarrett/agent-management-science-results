"""The not-told swarm: the prover archive with its exploration side taken out. One prover swarm on a problem, as the
archive's experiments and the swarm playground run one (swarm_play.Swarm: the same system prompt, Slack, shared
workspace, sandbox limits, nudge, compaction), but nothing proposes an answer to it: its first message states none
(swarm_play.PROMPT_UNTOLD), so the team has to find the answer as well as prove it. The nudge is the swarms' own, at
most twice a run, with a judge that isn't told an answer either (swarm_play.JUDGE_UNTOLD).

When a run has ended it is read as the archive reads an experiment, with no oracle:
1. ANSWER_ASK: the answer the team ended with, from its channel and each agent's last reply (REPORT's inputs).
2. The archive's stopping condition (verifier.py): the answer contract's gate, then the verifier on the whole record,
   told that the team was not told the answer (verifier.VERIFY_UNTOLD). "stop": a definite answer, a sound proof, no
   gap the team acknowledged, which is what would have ended an archive.
3. Only then, for the table: whether the answer is right (grading.Grader against the reference answer: MathArena's
   answer judge, and of an answer it counts right, whether it is the answer or the question restated as a computation
   left to be carried out, which is wrong; reading.json keeps the judge's own verdict as "matharena").
A run is solved if it stops and its answer is right.

The individual baseline (--solo): the same, with one agent alone in place of the team (swarm_play.Swarm `solo`: no
Slack, no partners, no shared workspace; the team's prompts with what coordinates a team taken out; the same limits,
budget, compaction and nudge, which reaches the agent as a user message), COPIES_SOLO runs a problem. A run is read
the same way, from what the agent wrote each time it stopped (ANSWER_ASK_SOLO, verifier.VERIFY_UNTOLD_SOLO).

    op-env uv run python explorer/serve.py                 # the server runs the swarms; its swarm page shows them
    op-env uv run python swarm_untold.py start             # the nine problems, $50 a swarm, 5 at once; each read as it ends
                                                           # (it waits for them; ended and run again, it goes on from where it was)
    op-env uv run python swarm_untold.py start --solo      # the individual baseline: 8 lone agents a problem, $50 each, 16 at once
    op-env uv run python swarm_untold.py start --solo --edition 10 --copies 1 --budget 5 --name oct-solo-v1
    op-env uv run python swarm_untold.py start --october --name NAME   # the October list (benchmark.OCTOBER: 14)
                                                           # another ArXivMath edition (benchmark.EDITIONS; 10: October, its
                                                           # 47 problems, numbered 1001-1047): one lone agent each, $5 a run
    op-env uv run python swarm_untold.py read [--solo]     # reads the sweep's ended runs not read yet
    op-env uv run python swarm_untold.py grade [--solo]    # grades the sweep's readings once more, by the grader as it is
                                                           # now (step 3 alone: no answer is read off or verified again)
    uv run python swarm_untold.py show [--solo]            # the table (also summary.md)
    uv run python swarm_untold.py prompts [--problem 12]   # each prompt that differs: told beside not told
    uv run python swarm_untold.py prompts --solo           # each prompt that differs: a team's beside a lone agent's

A sweep is kept in runs/basin/untold/<name>/ (v1 by default, solo-v1 with --solo): sweep.json (its settings and each
problem's runs) and summary.md. Its runs are swarm-playground runs (runs/basin/swarm/<time>-pNN/, settings.json
"told": false, and "solo": true for a lone agent), each with its reading: reading.json, reading_calls.jsonl and
verify/ (the verifier's box and conversation).
"""

import argparse
import json
import os
import shutil
import sys
import textwrap
import threading
import time
import traceback
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "explorer"))

import benchmark  # noqa: E402
import swarm_play  # noqa: E402
import verifier  # noqa: E402
from replies import parse  # noqa: E402
from sandbox import Sandbox  # noqa: E402
from slack import HUMAN  # noqa: E402

OUT = swarm_play.RUNS / "untold"
PROBLEMS = [1, 9, 12, 25, 30, 37, 41, 43, 48]
AGENTS = 4  # a swarm's, as the archive's experiments
PARALLEL = 5  # swarms at once (the server has run 6 of 4 agents: three archives)
READERS = 2  # runs read at once
# The individual baseline (--solo): lone agents, COPIES_SOLO a problem. 16 at once is fewer agents than 5 swarms'.
COPIES_SOLO, PARALLEL_SOLO, READERS_SOLO = 8, 16, 4
PORT = int(os.environ.get("SERVE_PORT", 8765))
POLL = 20  # seconds between looks at the server
CHANNEL_CHARS, FINAL_CHARS = 240_000, 12_000  # of the channel (its end) and of each last reply: prover_archive's, for REPORT
JUDGE_MODEL = "gpt-6.1-sol"  # grades an answer that isn't plainly right or wrong, as the explore sweep's runs did

ANSWER_ASK = """Below is a math problem, and the record of a team of {n} agents who were asked to find its answer and prove it, with Python that checks every step; they were not told the answer. The record: their Slack channel (#proof), then each agent's last reply. Their run ended: {reason}.

Read off the answer the team ended with: the one answer to the problem's question that the team as a whole stands behind at the end. If the agents ended with different answers, or the team ended without one (still undecided between candidates, or nothing stated), there is none. Bounds, a range, or "not known" together with what is known, is an answer if that is where the team ended. Don't solve the problem, don't judge whether the answer is right, and don't repair it: report what they ended with.

<problem>
{problem}
</problem>

<channel>
{channel}
</channel>

{finals}

Reply with one JSON object, in a ```json block, and nothing else: {{"answer": "<the team's final answer alone, as it would be submitted: no explanation or reasons; or null if there is none>", "claims_proof": true or false, "where": "<the posts or replies that state it>", "reason": "<briefly, why>"}}. claims_proof: whether the team claims, at the end, that its proof of that answer is complete."""

# ANSWER_ASK for a lone agent's run: its record is what it wrote each time it stopped and what the lead answered
# (where a team's has its channel); its last words come after only if they aren't among those.
ANSWER_ASK_SOLO = """Below is a math problem, and the record of one agent, working alone, who was asked to find its answer and prove it, with Python that checks every step; it was not told the answer. The record: what the agent wrote each time it stopped, and what its lead answered (a nudge, when it stopped short), in order; if its run was cut off while it was working, the last thing it wrote then comes after. Its run ended: {reason}.

Read off the answer the agent ended with: the one answer to the problem's question that it stands behind at the end. If it ended without one (still undecided between candidates, or nothing stated), there is none. Bounds, a range, or "not known" together with what is known, is an answer if that is where the agent ended. Don't solve the problem, don't judge whether the answer is right, and don't repair it: report what it ended with.

<problem>
{problem}
</problem>

<replies>
{channel}
</replies>

{finals}

Reply with one JSON object, in a ```json block, and nothing else: {{"answer": "<the agent's final answer alone, as it would be submitted: no explanation or reasons; or null if there is none>", "claims_proof": true or false, "where": "<the replies that state it>", "reason": "<briefly, why>"}}. claims_proof: whether the agent claims, at the end, that its proof of that answer is complete."""


# ---- the server -----------------------------------------------------------------------------------


def api(path, body=None):
    """The swarm server's reply (explorer/serve.py), {"error": ...} for a request it turns down. OSError if it isn't
    there."""
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=None if body is None else json.dumps(body).encode())
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def server():
    try:
        health = api("/api/health")
    except OSError:
        raise SystemExit(f"no server on port {PORT}: op-env uv run python explorer/serve.py") from None
    if health.get("stale") == "pending":  # a .py file changed while runs are live; launch() checks `told` took
        print("note: the server's code changed since it started (it restarts once nothing is live)", flush=True)
    elif health.get("stale"):
        raise SystemExit(f"the server's new code doesn't import ({health['stale']}): fix it, then restart the server")


def launch(p, s):
    """A not-told swarm on problem p, or a not-told lone agent (s["solo"]), started on the server: its run's name
    (its folder in swarm_play.OUT)."""
    solo = s["solo"]
    got = api("/api/swarm/run", {"problem": p, "system": swarm_play.SYSTEM_SOLO if solo else swarm_play.SYSTEM,
                                 "prompt": swarm_play.first_message(p, told=False, solo=solo),
                                 "n": s["agents"], "budget": s["budget"], "told": False, "solo": solo})  # fmt: skip
    if "key" not in got:
        raise SystemExit(f"p{p}: the server didn't start it: {got.get('error')}")
    run = got["key"].split("/", 1)[1]
    ran = json.loads((swarm_play.OUT / run / "settings.json").read_text())
    if ran.get("told") is not False or bool(ran.get("solo")) != solo:  # a server from before `told` or `solo`
        api("/api/swarm/stop", {"id": got["id"]})
        raise SystemExit(f"p{p}: the server started {run} as a {'told' if ran.get('told') is not False else 'team'} "
                         "swarm (old code); it was stopped. Restart the server.")
    return run


def state(run, live):
    """running | ended | interrupted (no longer on the server, and it never wrote its summary: the server restarted)."""
    if f"swarm/{run}" in live:
        return "running"
    summary = swarm_play.OUT / run / "summary.json"
    if not summary.exists():
        time.sleep(3)  # a run that has just ended writes it a moment later
    return "ended" if summary.exists() else "interrupted"


# ---- a sweep --------------------------------------------------------------------------------------


def load_sweep(name):
    """A sweep: {name, settings: {problems, budget, agents, solo, copies}, runs: {problem: [run, ...]}, earlier,
    started}. One from before `copies` had one run a problem, kept as a string."""
    f = OUT / name / "sweep.json"
    if not f.exists():
        return None
    sweep = json.loads(f.read_text())
    sweep["settings"] = {"solo": False, "copies": 1, **sweep["settings"]}
    sweep["runs"] = {p: [r] if isinstance(r, str) else r for p, r in sweep["runs"].items()}
    return sweep


def sweep_name(args):
    return args.name or ("solo-v1" if args.solo else "v1")


def runs_of(sweep):
    """Its runs, as (problem, run), in the problems' order."""
    return [(p, run) for p in sweep["settings"]["problems"] for run in sweep["runs"].get(str(p), [])]


def save_sweep(sweep):
    folder = OUT / sweep["name"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "sweep.json").write_text(json.dumps(sweep, indent=1))


def start(args):
    server()
    sweep = load_sweep(sweep_name(args))
    if args.problems is None:  # an edition's, or the sweep's own when it goes on, or the nine
        args.problems = (benchmark.OCTOBER if args.october else sorted(benchmark.edition(args.edition)) if args.edition
                         else sweep["settings"]["problems"] if sweep else PROBLEMS)  # fmt: skip
    if bad := [p for p in args.problems if not swarm_play.offered(p, told=False)]:
        raise SystemExit(f"unknown problems: {bad} (the nine, or another edition's by month * 100 + number: 1012)")
    solo = args.solo or bool(sweep and sweep["settings"]["solo"])
    agents = args.agents or (1 if solo else AGENTS)
    copies = args.copies or (sweep["settings"]["copies"] if sweep else COPIES_SOLO if solo else 1)
    parallel = args.parallel or (PARALLEL_SOLO if solo else PARALLEL)
    if solo and agents != 1:
        raise SystemExit("--solo: a lone agent is one agent a run")
    if sweep is None:
        sweep = {"name": sweep_name(args), "settings": {"problems": args.problems, "budget": args.budget, "agents": agents,
                                                        "solo": solo, "copies": copies},
                 "runs": {}, "earlier": {}, "started": time.time()}  # fmt: skip
    s = sweep["settings"]
    if (s["budget"], s["agents"], s["solo"]) != (args.budget, agents, solo):
        raise SystemExit(f"sweep {sweep['name']} has ${s['budget']:g} a run and "
                         + ("lone agents" if s["solo"] else f"teams of {s['agents']} agents") + ": use another --name")
    s["problems"] = sorted(set(s["problems"]) | set(args.problems))
    s["copies"] = max(s["copies"], copies)
    what = "alone" if solo else f"{agents} agents"
    try:
        live = {r["key"] for r in api("/api/swarm/runs") if r.get("live")}
    except OSError:
        raise SystemExit("the server went away") from None
    for p in args.again or []:
        runs = sweep["runs"].get(str(p), [])
        on = [run for run in runs if f"swarm/{run}" in live]
        redo = [run for run in runs if run not in on and not summary_of(run)]  # its interrupted runs
        if not redo and on:
            raise SystemExit(f"p{p}: {', '.join(on)} still running; stop from the swarm page first")
        redo = redo or runs  # none interrupted: the problem once more
        sweep["runs"][str(p)] = [run for run in runs if run not in redo]
        if redo:
            sweep["earlier"].setdefault(str(p), []).extend(redo)
    save_sweep(sweep)
    reader = Reader()  # before anything is started: no keys, or no sandbox, ends it here
    reading, noted, pool, last = {}, set(), ThreadPoolExecutor(args.readers or (READERS_SOLO if solo else READERS)), 0.0
    while True:
        try:
            live = {r["key"]: r for r in api("/api/swarm/runs") if r.get("live")}
        except OSError:
            print("no answer from the server; waiting for it", flush=True)
            time.sleep(POLL)
            continue
        states = {run: "interrupted" if run in noted else state(run, live) for _, run in runs_of(sweep)}
        for p, run in runs_of(sweep):
            st = states[run]
            if st == "interrupted" and run not in noted:
                noted.add(run)
                print(f"p{p}: {run} was interrupted (the server restarted); to run it again: start --again {p}", flush=True)
            if st == "ended" and run not in reading and not (swarm_play.OUT / run / "reading.json").exists():
                print(f"p{p}: {run} ended ({summary_of(run).get('reason')}, ${summary_of(run).get('cost', 0):.2f}); reading it", flush=True)
                reading[run] = pool.submit(read_one, run, reader)
        running = sum(st == "running" for st in states.values())
        free = parallel - running
        if args.max_live:  # every swarm live on the server counts, this sweep's or not
            free = min(free, args.max_live - len(live))
        # what is still to start, a problem's i-th run before any problem's (i+1)-th
        todo = [p for i in range(s["copies"]) for p in s["problems"] if len(sweep["runs"].get(str(p), [])) <= i]
        for p in todo[: max(0, free)]:
            run = launch(p, s)
            sweep["runs"].setdefault(str(p), []).append(run)
            save_sweep(sweep)
            running += 1
            print(f"p{p}: started {run} (${s['budget']:g}, {what}), {len(sweep['runs'][str(p)])} of {s['copies']}", flush=True)
        if len(todo) <= max(0, free) and not running and all(f.done() for f in reading.values()):
            break
        if time.time() - last > 900:
            last = time.time()
            mine = [live[f"swarm/{run}"] for _, run in runs_of(sweep) if f"swarm/{run}" in live]
            ended = sum(st == "ended" for st in states.values())
            print(time.strftime("%H:%M ") + f"{len(mine)} running (${sum(r['cost'] for r in mine):.2f} so far), {ended} ended of "
                  f"{s['copies'] * len(s['problems'])}, {sum(f.done() for f in reading.values())} read here", flush=True)  # fmt: skip
        time.sleep(POLL)
    show(args)


# ---- reading a run --------------------------------------------------------------------------------


@dataclass
class Ctx:
    """What reading a run uses: `call(what, user, ...)` one call of the model with no tools (its cost counted, kept
    in reading_calls.jsonl), `llm` the agents' model, `folder` where the reading is kept."""

    llm: object
    folder: Path
    calls: list = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def call(self, what, user, system=None, tokens=32000, effort=None):
        from llm import cost, usage_dict
        import prover_archive

        llm = replace(self.llm, system=system or prover_archive.SIDE_SYSTEM, tools=[], max_tokens=tokens,
                      **({"effort": effort} if effort else {}))  # fmt: skip
        t = time.time()
        reply = llm.create([{"role": "user", "content": user}])
        spent = cost(llm.model, usage_dict(reply.message.usage))
        text = "".join(b.text for b in reply.message.content if b.type == "text")
        rec = {"what": what, "time": t, "seconds": round(time.time() - t, 1), "cost": round(spent, 5), "user": user,
               "text": text, "request_id": reply.request_id}  # fmt: skip
        with self.lock:
            self.calls.append(rec)
        return text

    @property
    def cost(self):
        return sum(c["cost"] for c in self.calls)


_box = None
_box_lock = threading.Lock()


def verify_sandbox():
    """The sandbox the verifier's runs use, made once."""
    global _box
    with _box_lock:
        if _box is None:
            _box = Sandbox(memory_mb=5 * 1024, max_output_bytes=8 * 2**20, max_file_bytes=2 * 2**30, processes=4,
                           max_parallel=6)  # fmt: skip
        return _box


class Reader:
    """What reading takes, made once: the archive's side model (the verifier's too), a sandbox for the verifier's
    runs, the grader."""

    def __init__(self):
        from benchmark import Benchmark
        from grading import Grader
        from llm import openai_client

        self.llm = swarm_play.agent_llm(threading.BoundedSemaphore(16))
        self.sandbox = verify_sandbox()
        if why := self.sandbox.ready():
            raise SystemExit(f"the sandbox isn't ready: {why}")
        self.bench = Benchmark()
        self.grader = Grader(openai_client(), judge_model=JUDGE_MODEL)


def summary_of(run):
    f = swarm_play.OUT / run / "summary.json"
    return json.loads(f.read_text()) if f.exists() else {}


def aside(path):
    """An earlier reading's file or folder kept beside the new one: reading.json -> reading.1.json, verify -> verify.1."""
    if path.exists() or path.is_symlink():
        i = 1
        while (new := path.with_name(f"{path.stem}.{i}{path.suffix}")).exists():
            i += 1
        path.rename(new)


def read(run, reader, again=False, out=None):
    """The reading of an ended not-told run (see the module's docstring): kept as reading.json in its folder (or in
    `out`), and returned. One already there is returned as it is, unless `again`. While it is read,
    reading.live.json holds its stage (swarm_play.reading_of shows it on the swarm page)."""
    folder = swarm_play.OUT / run
    out = Path(out) if out else folder
    out.mkdir(parents=True, exist_ok=True)
    if (out / "reading.json").exists() and not again:
        return json.loads((out / "reading.json").read_text())
    settings, summary = json.loads((folder / "settings.json").read_text()), summary_of(run)
    if not summary:
        raise ValueError(f"{run} hasn't ended (no summary.json)")
    for name in ("reading.json", "reading_calls.jsonl", "verify"):
        aside(out / name)
    live = out / "reading.live.json"  # while it is read: the stage, for the swarm page (swarm_play.reading_of)
    t0 = time.time()
    stage = lambda name, **kw: live.write_text(json.dumps({"pid": os.getpid(), "started": t0, "at": time.time(),  # noqa: E731
                                                           "stage": name, **kw}))  # fmt: skip
    try:
        return reading(run, reader, folder, out, settings, summary, stage)
    finally:
        live.unlink(missing_ok=True)


def reading(run, reader, folder, out, settings, summary, stage):
    from prover_archive import bare

    stage("answer")
    p = settings["problem"]
    problem, reason = swarm_play.problem_text(p).strip(), summary.get("reason") or "ended"
    record, ctx = verifier.Record(folder), Ctx(llm=reader.llm, folder=out)
    if record.solo:  # its replies are its channel; its last words only if they aren't among them (it was cut off)
        a = record.agents()[0]
        said, last = [r["body"].strip() for r in record.rows() if r["sender"] == a], record.final(a).strip()
        finals = f"<cut_off_while_working>\n{last[-FINAL_CHARS:]}\n</cut_off_while_working>" if last and last not in said else ""
    else:
        finals = "\n\n".join(f"<{a}_last_reply>\n{record.final(a)[-FINAL_CHARS:] or '(none)'}\n</{a}_last_reply>"
                             for a in record.agents())  # fmt: skip
    ask = ANSWER_ASK_SOLO if record.solo else ANSWER_ASK
    got = parse(ctx.call("answer", ask.format(n=len(record.agents()), reason=reason, problem=problem,
                                              channel=record.channel()[-CHANNEL_CHARS:] or "(nothing posted)",
                                              finals=finals))) or {}  # fmt: skip
    answer = got.get("answer")
    answer = bare(str(answer)) if answer is not None and str(answer).strip().lower() not in ("", "null", "none") else None
    r = {"run": run, "problem": p, "told": settings.get("told", True), "solo": record.solo, "answer": answer,
         "claims_proof": got.get("claims_proof") is True, "where": got.get("where"), "answer_reason": got.get("reason"),
         "definite": False, "verify": None, "stop": False}  # fmt: skip
    spent = 0.0
    if answer:
        stage("contract", answer=answer)
        c = verifier.contract(ctx.call, problem)
        d = verifier.definite(ctx.call, problem, c, answer)
        r.update(contract=c, definite=d["definite"], definite_reason=d["reason"], procedure=d.get("procedure") is True)
        if d["definite"]:
            stage("verify", answer=answer)
            v = verifier.verify(reader.llm, reader.sandbox, record, out / "verify", problem, c["form"], answer, reason,
                                told=False)  # fmt: skip
            spent = v["cost"]
            r["verify"] = {**{k: v[k] for k in ("verdict", "acknowledged", "review", "responses", "runs")},
                           "cost": round(spent, 4)}  # fmt: skip
            r["stop"] = v["stop"]
    stage("grade", answer=answer)
    r.update(graded(reader, r), cost=round(ctx.cost + spent, 4), read_at=time.time())
    with open(out / "reading_calls.jsonl", "a") as f:
        for call in ctx.calls:
            f.write(json.dumps(call) + "\n")
    (out / "reading.json").write_text(json.dumps(r, indent=1))
    return r


def graded(reader, r):
    """A reading's grade against the reference answer, as reading.json keeps it: `correct` (grading.Grader: an answer
    that restates the question as a computation is wrong, `restated`), `matharena` (MathArena's judge alone, which
    counts such an answer right), and `solved`: it stopped and the answer is right."""
    reference = reader.bench.get_problem(r["problem"])
    grade = reader.grader.grade(reference, r["answer"])
    return {"reference": reference["answer"], "correct": grade.correct, "graded_by": grade.method,
            "matharena": grade.matharena, "restated": grade.restated is True, "grade_note": grade.note,
            "solved": bool(r["stop"] and grade.correct)}  # fmt: skip


def mark(r):
    """A reading's grade in a word."""
    return ("right" if r["correct"] else "the question restated" if r.get("restated")
            else "wrong" if r["correct"] is False else "ungraded")  # fmt: skip


def grade_all(args):
    """The sweep's readings graded once more, by the grader as it is now. Nothing else of a reading changes: its
    answer, the gate and the verifier's verdict stay as they were read."""
    from types import SimpleNamespace

    from benchmark import Benchmark
    from grading import Grader
    from llm import openai_client

    sweep = load_sweep(sweep_name(args))
    if sweep is None:
        raise SystemExit(f"no sweep {sweep_name(args)} in {OUT.relative_to(ROOT)}")
    reader = SimpleNamespace(bench=Benchmark(), grader=Grader(openai_client(), judge_model=JUDGE_MODEL))
    for p, run in runs_of(sweep):
        f = swarm_play.OUT / run / "reading.json"
        if not f.exists():
            continue
        r = json.loads(f.read_text())
        new, was = graded(reader, r), mark(r)
        if any(r.get(k) != v for k, v in new.items()):
            r.update(new, graded_at=time.time())
            f.write_text(json.dumps(r, indent=1))
            if mark(r) != was:
                print(f"p{p}: {run}: {was} -> {mark(r)}" + (f" ({r['grade_note']})" if r["grade_note"] else ""), flush=True)
    print(f"the grader was asked {reader.grader.asked} times (${reader.grader.cost:.2f}), and had {reader.grader.recalled} "
          "verdicts already\n", flush=True)  # fmt: skip
    show(args)


def read_one(run, reader, again=False):
    try:
        r = read(run, reader, again)
    except Exception as e:
        traceback.print_exc()
        return print(f"!! {run}: not read: {e!r}", flush=True)
    v = r["verify"] or {}
    print(f"p{r['problem']}: {run}: answer {r['answer']!r} ({mark(r)}); "
          + (f"verifier: {v.get('verdict')}" + (", a gap acknowledged" if v.get("acknowledged") else "") if v
             else "not definite" if r["answer"] else "no answer")
          + f"; {'SOLVED' if r['solved'] else 'stop on a wrong answer' if r['stop'] else 'not solved'} (reading ${r['cost']:.2f})",
          flush=True)  # fmt: skip


def read_all(args):
    sweep = load_sweep(sweep_name(args))
    runs = args.run or [run for _, run in runs_of(sweep or {"settings": {"problems": []}, "runs": {}})]
    if not runs:
        raise SystemExit(f"no runs: sweep {sweep_name(args)} has none, and no --run")
    todo = [run for run in runs if summary_of(run) and (args.again or not (swarm_play.OUT / run / "reading.json").exists())]
    for run in sorted(set(runs) - set(todo)):
        print(f"{run}: " + ("already read" if summary_of(run) else "hasn't ended"))
    if todo:
        reader = Reader()
        with ThreadPoolExecutor(READERS_SOLO if sweep and sweep["settings"]["solo"] else READERS) as pool:
            list(pool.map(lambda run: read_one(run, reader, args.again), todo))
    if not args.run:
        show(args)


# ---- the table ------------------------------------------------------------------------------------


def seconds(run):
    """From the run's start (its folder's name) to its summary."""
    try:
        t0 = time.mktime(time.strptime(run[:15], "%Y%m%d-%H%M%S"))
    except ValueError:
        return None
    return (swarm_play.OUT / run / "summary.json").stat().st_mtime - t0


def nudges(run):
    f = swarm_play.OUT / run / "slack.jsonl"
    rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
    return sum(r["sender"] == HUMAN and r["body"] in (swarm_play.NUDGE, swarm_play.NUDGE_SOLO) for r in rows)


def show(args):
    sweep = load_sweep(sweep_name(args))
    if sweep is None:
        raise SystemExit(f"no sweep {sweep_name(args)} in {OUT.relative_to(ROOT)}")
    s = sweep["settings"]
    solo, copies = s["solo"], s["copies"]
    who = "agent" if solo else "team"
    cell = lambda x: str(x).replace("|", "\\|").replace("\n", " ")  # noqa: E731
    what = (f"{copies} lone agents a problem (no Slack, no partners, no shared workspace; otherwise a swarm's rules)" if solo
            else f"One swarm of {s['agents']} agents a problem" + (f", {copies} times" if copies > 1 else ""))  # fmt: skip
    head = [f"# {'The individual baseline' if solo else 'The not-told swarm'}: sweep {sweep['name']}", "",
            f"{what}, not told the answer, ${s['budget']:g} each. Solved: the verifier found a sound proof of a definite "
            f"answer with no gap the {who} acknowledged (stop), and the answer is right. An answer that restates the "
            "question as a computation left to be carried out is wrong (MathArena's judge alone counts it right).", ""]  # fmt: skip
    table = [f"| problem | run | ended | cost | min | nudges | the {who}'s answer | right | verifier | solved |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    tally = {p: {"ended": 0, "solved": 0, "right": 0, "stops": 0, "restated": 0, "cost": 0.0, "read": 0.0} for p in s["problems"]}
    for p in s["problems"]:
        runs, t = sweep["runs"].get(str(p), []), tally[p]
        if not runs:
            table.append(f"| p{p} | not started | | | | | | | | |")
        for i, run in enumerate(runs, 1):
            label = f"p{p}" if copies == 1 else f"p{p} #{i}"
            summary, f = summary_of(run), swarm_play.OUT / run / "reading.json"
            if not summary:
                table.append(f"| {label} | {run} | running, or interrupted | | | | | | | |")
                continue
            r = json.loads(f.read_text()) if f.exists() else None
            t["ended"] += 1
            t["cost"] += summary.get("cost", 0.0)
            row = [label, run, cell(summary.get("reason")), f"${summary.get('cost', 0):.2f}",
                   f"{seconds(run) / 60:.0f}" if seconds(run) is not None else "", nudges(run)]  # fmt: skip
            if r is None:
                row += ["not read", "", "", ""]
            else:
                v = r["verify"] or {}
                verdict = (v.get("verdict") or "no verdict") + (", gap acknowledged" if v.get("acknowledged") else "") if v \
                    else "not definite" if r["answer"] else "no answer"  # fmt: skip
                right = "no, the question restated" if r.get("restated") else {True: "yes", False: "no"}.get(r["correct"], "?")
                row += [f"`{cell(r['answer'])}`" if r["answer"] else "none", right,
                        verdict, "yes" if r["solved"] else "false stop" if r["stop"] else "no"]  # fmt: skip
                t["solved"], t["stops"], t["right"] = t["solved"] + r["solved"], t["stops"] + r["stop"], t["right"] + (r["correct"] is True)
                t["restated"] += bool(r.get("restated"))
                t["read"] += r["cost"]
            table.append("| " + " | ".join(str(x) for x in row) + " |")
    total = {k: sum(t[k] for t in tally.values()) for k in ("ended", "solved", "right", "stops", "restated", "cost", "read")}
    by_problem = []
    if copies > 1:  # a problem a row, before the runs
        by_problem = ["| problem | runs ended | solved | right answer | stops on a wrong answer | cost |", "|---|---|---|---|---|---|"]
        by_problem += [f"| p{p} | {t['ended']} of {copies} | {t['solved']} | {t['right']} | {t['stops'] - t['solved']} | ${t['cost']:.2f} |"
                       for p, t in tally.items()]  # fmt: skip
        by_problem += [f"| all | {total['ended']} of {copies * len(tally)} | {total['solved']} | {total['right']} | "
                       f"{total['stops'] - total['solved']} | ${total['cost']:.2f} |", ""]  # fmt: skip
    some = f"; {sum(t['solved'] > 0 for t in tally.values())} of {len(tally)} problems solved by at least one run" if copies > 1 else ""
    foot = ["", f"Solved {total['solved']} of {total['ended']} ended runs ({len(tally)} problems){some}: {total['right']} right "
                f"answers, {total['stops']} stops ({total['stops'] - total['solved']} on a wrong answer"
                + (f", {total['restated']} of them the question restated" if total["restated"] else "") + "). The "
                f"{'agents' if solo else 'swarms'} cost ${total['cost']:.2f}, reading them ${total['read']:.2f}."]  # fmt: skip
    text = "\n".join(head + by_problem + table + foot) + "\n"
    (OUT / sweep["name"] / "summary.md").write_text(text)
    print(text)


# ---- the prompts, told beside not told --------------------------------------------------------------


def beside(a, b, width):
    """Two texts in two columns, paragraph beside paragraph when they have as many."""
    w = (width - 3) // 2
    wrap = lambda s: [l for line in s.split("\n") for l in (textwrap.wrap(line, w) or [""])]  # noqa: E731
    pa, pb = a.split("\n\n"), b.split("\n\n")
    pairs = list(zip(pa, pb)) if len(pa) == len(pb) else [(a, b)]
    out = []
    for i, (x, y) in enumerate(pairs):
        lx, ly = wrap(x), wrap(y)
        n = max(len(lx), len(ly))
        out += [f"{l:<{w}} │ {r}".rstrip() for l, r in zip(lx + [""] * (n - len(lx)), ly + [""] * (n - len(ly)))]
        if i < len(pairs) - 1:
            out.append(f"{'':<{w}} │")
    return "\n".join(out)


def prompts(args):
    import prover_archive

    p = args.problem
    first = lambda told, solo: (swarm_play.first_message(p, told, solo) if p else {  # noqa: E731
        (True, False): swarm_play.PROMPT, (False, False): swarm_play.PROMPT_UNTOLD,
        (False, True): swarm_play.PROMPT_UNTOLD_SOLO}[told, solo])  # fmt: skip
    statement = swarm_play.problem_text(p).strip() if p and not args.statement else None  # the same on both sides
    short = lambda text: text.replace(statement, "{problem}") if statement else text  # noqa: E731
    log = "{the channel's last 15 messages}"
    width = args.width or shutil.get_terminal_size((160, 40)).columns
    w = (width - 3) // 2
    if args.solo:  # a team beside a lone agent, neither told the answer
        record = verifier.RECORD_SOLO
        left, right = "A TEAM, NOT TOLD", "ONE AGENT ALONE, NOT TOLD"
        pairs = [
            ("the system prompt (swarm_play.SYSTEM, SYSTEM_SOLO)", swarm_play.SYSTEM, swarm_play.SYSTEM_SOLO),
            ("the first message (swarm_play.PROMPT_UNTOLD, PROMPT_UNTOLD_SOLO)", short(first(False, False)), short(first(False, True))),
            ("the tools", "the scratchpad's (read, write, edit, run), slack_post, slack_read", "the scratchpad's (read, write, edit, run)"),
            ("the nudge (swarm_play.NUDGE, NUDGE_SOLO)", f"{swarm_play.NUDGE}\n\nPosted on #proof by the lead; each agent is woken and told "
             "it has an unread message that tags it.", f"{swarm_play.NUDGE_SOLO}\n\nA user message, which wakes the agent."),
            ("the nudge's judge, its system prompt (swarm_play.JUDGE_UNTOLD, JUDGE_UNTOLD_SOLO)", swarm_play.JUDGE_UNTOLD,
             swarm_play.JUDGE_UNTOLD_SOLO),
            ("the nudge's judge, its message", log, "{the agent's reply each time it stopped, and the lead's messages, in order}"),
            ("compaction, the handoff asked for (swarm_play.COMPACT_ASK, COMPACT_ASK_SOLO)", swarm_play.COMPACT_ASK, swarm_play.COMPACT_ASK_SOLO),
            ("compaction, what the conversation becomes (swarm_play.COMPACTED, COMPACTED_SOLO)", swarm_play.COMPACTED, swarm_play.COMPACTED_SOLO),
            ("reading the run: its answer (ANSWER_ASK, ANSWER_ASK_SOLO)", ANSWER_ASK, ANSWER_ASK_SOLO),
            ("the verifier's task, who was asked what (verifier.UNTOLD, UNTOLD_SOLO)", verifier.UNTOLD, verifier.UNTOLD_SOLO),
            ("the verifier's task, its record and tools (verifier.RECORD_SOLO; the steps and verdicts are the same)",
             "\n".join(a.strip() for a, _ in record), "\n".join(b.strip() or "(no workspace)" for _, b in record)),
        ]  # fmt: skip
        same = ("the same for both: the sandbox's limits, the budget, compaction at "
                f"{swarm_play.COMPACT_AT // 1000}k tokens, the nudge after {swarm_play.NUDGE_AFTER} s idle and at most "
                f"{swarm_play.MAX_NUDGES} a run, the end once no nudge is left, the answer contract and its gate "
                "(verifier.CONTRACT, DEFINITE), the verifier's steps and verdicts, the grader.")  # fmt: skip
    else:
        left, right = "TOLD THE ANSWER", "NOT TOLD"
        pairs = [
            ("the first message (swarm_play.PROMPT, PROMPT_UNTOLD)", short(first(True, False)), short(first(False, False))),
            ("the nudge's judge, its system prompt (swarm_play.JUDGE, JUDGE_UNTOLD)", swarm_play.JUDGE, swarm_play.JUDGE_UNTOLD),
            ("the nudge's judge, its message", "The answer they were told: {answer}\n\n" + log, log),
            ("the verifier's task, where it differs (verifier.TOLD, UNTOLD; the rest of VERIFY is the same)", verifier.TOLD, verifier.UNTOLD),
            ("reading the run: the archive's REPORT, and ANSWER_ASK here", prover_archive.REPORT, ANSWER_ASK),
        ]  # fmt: skip
        same = (f"the same for both: the system prompt (swarm_play.SYSTEM), the nudge ({swarm_play.NUDGE!r}, after "
                f"{swarm_play.NUDGE_AFTER} s idle, at most {swarm_play.MAX_NUDGES} a run), compaction, the sandbox's limits, the "
                "answer contract and its gate (verifier.CONTRACT, DEFINITE). No halves are written "
                "(prover_archive.HALVES_ASK): they would state the answer.")  # fmt: skip
    for title, a, b in pairs:
        print(f"\n{'=' * width}\n{title}\n{'=' * width}\n{left:<{w}} │ {right}\n{'-' * w}─┼─{'-' * w}")
        print(beside(a, b, width))
    print(f"\n{'=' * width}\n{same}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("start", "read", "show", "grade"):
        sp = sub.add_parser(name)
        sp.add_argument("--name", help="the sweep (runs/basin/untold/<name>/): v1 by default, solo-v1 with --solo")
        sp.add_argument("--solo", action="store_true", help="the individual baseline: lone agents (no Slack, no partners), "
                                                            f"{COPIES_SOLO} a problem")  # fmt: skip
        if name == "start":
            sp.add_argument("--problems", type=int, nargs="+", help="default: the nine, or the sweep's own when it goes on; "
                            "another edition's are month * 100 + number (1012: October's p12)")  # fmt: skip
            sp.add_argument("--october", action="store_true", help="the October list (benchmark.OCTOBER: the 14 "
                            "problems of October that are its counterpart of the nine), unless --problems names some")  # fmt: skip
            sp.add_argument("--edition", type=int, choices=sorted(benchmark.EDITIONS), help="every problem of another "
                            "ArXivMath edition, by its month (10: October, 1001-1047), unless --problems names some")  # fmt: skip
            sp.add_argument("--budget", type=float, default=swarm_play.BUDGET_UNTOLD, help="dollars a run")
            sp.add_argument("--agents", type=int, help=f"a swarm's (default {AGENTS}; 1 with --solo)")
            sp.add_argument("--copies", type=int, help=f"runs a problem (default 1; {COPIES_SOLO} with --solo); more than "
                                                       "an existing sweep has adds to it")  # fmt: skip
            sp.add_argument("--parallel", type=int, help=f"runs at once (default {PARALLEL}; {PARALLEL_SOLO} with --solo)")
            sp.add_argument("--readers", type=int, help=f"runs read at once (default {READERS}; {READERS_SOLO} with --solo)")
            sp.add_argument("--max-live", type=int, help="start a run only while fewer than this many run on the server "
                                                         "(any sweep's or page's), so it takes the place of one that ends")
            sp.add_argument("--again", type=int, nargs="+", help="problems whose interrupted runs to run again (a problem "
                                                                 "with none interrupted: all its runs once more)")  # fmt: skip
        if name == "read":
            sp.add_argument("--run", nargs="+", help="runs to read (folders of runs/basin/swarm/), not the sweep's")
            sp.add_argument("--again", action="store_true", help="read once more (the earlier reading is kept beside)")
    sp = sub.add_parser("prompts")
    sp.add_argument("--solo", action="store_true", help="a team's prompts beside a lone agent's (neither told), not told beside not told")
    sp.add_argument("--problem", type=int, choices=swarm_play.PROBLEMS, help="filled in for this problem (else the templates)")
    sp.add_argument("--statement", action="store_true", help="with --problem: show the problem's statement too")
    sp.add_argument("--width", type=int, help="columns (default: the terminal's)")
    args = ap.parse_args()
    {"start": start, "read": read_all, "show": show, "grade": grade_all, "prompts": prompts}[args.cmd](args)


if __name__ == "__main__":
    main()
