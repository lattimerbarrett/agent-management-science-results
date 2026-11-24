"""The server behind the swarm page (explorer/swarm.html, swarm_play.py) and the prover-archive page
(explorer/archive.html, prover_archive.py). It runs the swarms and the archives, in threads of this process, and
shows saved runs from disk.

    op-env uv run python explorer/serve.py        # then open http://127.0.0.1:8765/archive.html or swarm.html

The swarm page: a team of fresh agents on one problem, talking on a Slack channel and sharing a workspace, or one
agent alone, with the prompts you edit. The archive page: a prover archive, whose experiments are swarms that the
swarm page shows too. swarm_untold.py and archive_sweep.py start their runs through this server.

The page reaches the server only from 127.0.0.1; the API key stays in this process.

Pages follow a live run by polling /api/events (a request held at most HOLD seconds), not by a stream held open:
Chrome allows 6 connections to one host, and each live stream (an archive, each experiment it embeds, a swarm in
another tab) held one, so a page with a few of them open stopped loading anything until the server restarted. When a
Python file the server runs changes, it restarts itself (os.execv, same command and environment) as soon as nothing
is live, after checking that the new code imports; with runs live, the pages offer the restart (it stops them).
"""

import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from sandbox import Sandbox  # noqa: E402
import swarm_play  # noqa: E402
import prover_archive  # noqa: E402

PORT = int(os.environ.get("SERVE_PORT", 8765))  # SERVE_PORT: a second server beside one already running
OUTPUT_BYTES = 256 * 2**20  # the most a run may print
# the swarms' sandboxes: every swarm's runs share the machine (48 GB, 18 cores), so at most SWARM_PARALLEL run at once
# across all live swarms (SWARM_GATE; an agent whose run must wait just waits), each with SWARM_MEMORY_MB for all its
# processes and up to SWARM_PROCESSES of them (the run, multiprocessing's resource tracker and 2 workers); a file a
# run writes may be SWARM_FILE_BYTES (what it prints is still OUTPUT_BYTES). How long a run may take is the page's
# (swarm_play.RUN_MINUTES at most). 12 x 5 GB = 60 GB of caps on 48 GB, for three archives at once (up to 6 swarms):
# an overcommit, taken because none of the first 1,600 swarm runs reached 5 GB (and most took under a second).
SWARM_MEMORY_MB = 5 * 1024
SWARM_PARALLEL = 12
SWARM_PROCESSES = 4
SWARM_FILE_BYTES = 8 * 2**30
SWARM_GATE = threading.BoundedSemaphore(SWARM_PARALLEL)
# responses in flight at once, for everything the server runs: swarms, archives' rollouts and
# their judge, report, manager and halves calls (a call holds its place while it streams). An archive wants up to 2
# swarms x 4 agents + 2 rollouts + a side call = 11; three archives 33. It was 4 until 2026-11-04, so several swarms in
# one server took turns. OpenAI's rate limits (429) are retried (llm.retryable).
LLM_PARALLEL = 36
HOLD = 1.5  # seconds a poll of /api/events waits for a run's next event
LINGER = 0.15  # seconds a poll lasts at least while the run goes on: at most ~6 polls a second a page
BATCH = 20000  # most events one poll returns (a page catching up on a long run polls again at once)
KEEP_ENDED = 600  # seconds an ended run stays in memory (its events); after that a page shows it from disk
BOOT = f"{os.getpid()}-{time.time():.0f}"  # changes when the server restarts: pages reconnect
AUTO_RESTART = os.environ.get("SERVE_AUTORESTART", "1") != "0"
DELTAS = ("think", "say", "args")


def sources():
    """The files whose change means the server runs old code."""
    return sorted([*ROOT.glob("*.py"), *HERE.glob("*.py"), *ROOT.glob("*.yaml"), ROOT / "evs.md"])


def mtimes(paths):
    return {str(p): p.stat().st_mtime for p in paths if p.exists()}


def static_version():
    """What a page loaded: a page whose version differs offers to reload."""
    m = mtimes([*HERE.glob("*.html"), *HERE.glob("*.css"), *HERE.glob("*.js")])
    return hashlib.sha1(json.dumps(m, sort_keys=True).encode()).hexdigest()[:10]


def coalesce(events):
    """Consecutive deltas of one agent's block joined into one event: a page catching up on a long run gets its text
    in a few events, not one per token. Order within each agent's stream is kept."""
    out, open_ = [], {}  # agent -> (key, index in out) of the delta it is in
    for e in events:
        a = e.get("a")
        if e["k"] in DELTAS:
            key = (e["k"], e.get("id"))
            cur = open_.get(a)
            if cur and cur[0] == key:
                j = cur[1]
                out[j] = {**out[j], "text": out[j]["text"] + e["text"]}
                continue
            open_[a] = (key, len(out))
        else:
            open_.pop(a, None)
        out.append(e)
    return out


def swarm_sandbox(stop):
    """A swarm's sandbox (and a prover archive's, for its agents): see SWARM_MEMORY_MB."""
    return Sandbox(memory_mb=SWARM_MEMORY_MB, max_output_bytes=OUTPUT_BYTES, max_file_bytes=SWARM_FILE_BYTES,
                   processes=SWARM_PROCESSES, gate=SWARM_GATE, stop=stop)


def live(registry):
    return [r for r in list(registry.values()) if not r.ended]


class Handler(SimpleHTTPRequestHandler):
    llm = swarm_llm = None
    swarms, archives = {}, {}
    stale = None  # None, or why the server runs old code: "pending" (waiting for live runs) or the new code's error
    restarting = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def log_message(self, *args):
        pass

    def end_headers(self):  # the pages always load as they are on disk
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    @classmethod
    def registries(cls):
        return {"swarm": cls.swarms, "archive": cls.archives}

    @classmethod
    def live_count(cls):
        return sum(len(live(r)) for r in cls.registries().values())

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/health":
            return self.send_json({"boot": BOOT, "static": static_version(), "stale": self.stale,
                                   "live": self.live_count(), "restarting": self.restarting})  # fmt: skip
        if url.path == "/api/events":
            q = {k: v[0] for k, v in parse_qs(url.query).items()}
            registry = self.registries().get(q.get("of", ""), {})
            try:
                since = max(0, int(q.get("since", 0)))
            except ValueError:
                since = 0
            return self.poll(registry.get(q.get("id", "")), since)
        if url.path.startswith("/api/swarm/"):
            return self.swarm_get(url.path.removeprefix("/api/swarm/"), {k: v[0] for k, v in parse_qs(url.query).items()})
        if url.path.startswith("/api/archive/"):
            return self.archive_get(url.path.removeprefix("/api/archive/"), {k: v[0] for k, v in parse_qs(url.query).items()})
        return super().do_GET()

    def archive_get(self, what, q):
        if what == "defaults":
            return self.send_json({"problems": prover_archive.PROBLEMS, "defaults": prover_archive.DEFAULTS,
                                   "prompts": prover_archive.prompts()})  # fmt: skip
        if what == "runs":
            on = {a.id: a for a in live(self.archives)}
            out = []
            for r in prover_archive.saved_runs():
                a = on.get(r["id"])
                if a is not None:
                    r = {**r, "spent": round(a.spent, 4), "nodes": len(a.nodes), "experiments": len(a.exps),
                         "budget": float(a.s["budget"]), "reason": None}  # fmt: skip
                elif not r.get("ended"):
                    r = {**r, "reason": "interrupted (the server restarted)"}
                out.append({**r, "live": a is not None})
            return self.send_json(out)
        folder = prover_archive.run_folder(q.get("run", ""))
        if folder is None:
            return self.send_json({"error": "no such run"}, 404)
        if what == "saved":
            return self.send_json(prover_archive.replay(q["run"]))
        if what == "prompts":
            return self.send_json({"prompts": json.loads((folder / "prompts.json").read_text()),
                                   "settings": json.loads((folder / "settings.json").read_text())})  # fmt: skip
        if what == "files":
            return self.send_json(prover_archive.files(folder, q.get("node", "")))
        if what == "file":
            text = prover_archive.read(folder, q.get("node", ""), q.get("path", ""))
            return self.send_json({"text": text} if text is not None else {"error": "no such file"}, 200 if text is not None else 404)
        if what == "prompt":  # what an agent's step was sent, and the experiments' times beside it
            got = prover_archive.prompt(folder, q.get("node", ""), q.get("which", "step"))
            return self.send_json(got if got is not None else {"error": "no such agent"}, 200 if got is not None else 404)
        self.send_json({"error": "not found"}, 404)

    def archive_post(self, what, body):
        if what == "run":
            p = body.get("problem")
            if p not in prover_archive.PROBLEMS:
                return self.send_json({"error": "unknown problem"}, 400)
            settings = {}
            for k, v in (body.get("settings") or {}).items():
                if k in prover_archive.DEFAULTS:
                    try:
                        settings[k] = type(prover_archive.DEFAULTS[k])(v)
                    except (TypeError, ValueError):
                        return self.send_json({"error": f"{k} must be a number"}, 400)
            if not 1 <= settings.get("agents", 4) <= swarm_play.MAX_AGENTS:
                return self.send_json({"error": f"1 to {swarm_play.MAX_AGENTS} agents a swarm"}, 400)
            if not 0 < settings.get("run_minutes", 10) <= swarm_play.RUN_MINUTES:
                return self.send_json({"error": f"runs of at most {swarm_play.RUN_MINUTES} minutes"}, 400)
            if settings.get("stop_rule", "verify") not in ("verify", "manager"):
                return self.send_json({"error": "stop_rule is verify or manager"}, 400)
            if settings.get("gate", "definite") not in ("definite", "claim"):
                return self.send_json({"error": "gate is definite or claim"}, 400)
            if settings.get("experiments", "run") not in ("run", "list") or settings.get("max_rollouts", 0) < 0:
                return self.send_json({"error": "experiments is run or list; max_rollouts is 0 or more"}, 400)
            register = lambda swarm: self.swarms.__setitem__(swarm.id, swarm)
            archive = prover_archive.Archive(self.llm, self.swarm_llm, swarm_sandbox, p, settings, register)
            self.archives[archive.id] = archive
            return self.send_json({"id": archive.id})
        archive = self.archives.get(body.get("id"))
        if archive is None:
            return self.send_json({"error": "no such archive run"}, 404)
        if what == "stop":
            archive.end("stopped")
            return self.send_json({})
        if what == "rollout":
            try:
                archive.enqueue(str(body.get("node")), str(body.get("branch")))
            except ValueError as e:
                return self.send_json({"error": str(e)}, 400)
            return self.send_json({})
        self.send_json({"error": "not found"}, 404)

    def swarm_get(self, what, q):
        if what == "defaults":
            return self.send_json([swarm_play.defaults(p) for p in swarm_play.PROBLEMS])
        if what == "runs":  # every saved run, the live ones with their id and what they have spent
            on = {f"swarm/{w.folder.name}": w for w in live(self.swarms)}
            out = []
            for r in swarm_play.saved_runs():
                w = on.get(r["key"])
                if w is not None:
                    r = {**r, "cost": round(w.cost, 4), "live": w.id, "budget": w.budget}
                else:
                    r = {**r, "live": None, "reason": r["reason"] or "interrupted (the server restarted)"}
                out.append(r)
            return self.send_json(out)
        if what in ("saved", "info", "verifier") or (what in ("files", "file") and "run" in q):
            folder = swarm_play.run_folder(q.get("run", ""))
            if folder is None:
                return self.send_json({"error": "no such run"}, 404)
            if what == "saved":
                return self.send_json(swarm_play.replay(q["run"]))
            if what == "info":
                return self.send_json(swarm_play.info(q["run"]))
            if what == "verifier":  # a not-told run's reading and the verifier's review (swarm_untold.py)
                return self.send_json(swarm_play.verifier(q["run"]))
            if what == "files":
                return self.send_json(swarm_play.files(folder))
            text = swarm_play.read(folder, q.get("path", ""))
            return self.send_json({"text": text} if text is not None else {"error": "no such file"}, 200 if text is not None else 404)
        swarm = self.swarms.get(q.get("id", ""))
        if swarm is None:
            return self.send_json({"error": "no such swarm run (runs are kept in memory until the server restarts)"}, 404)
        if what == "files":
            return self.send_json(swarm.files())
        if what == "file":
            text = swarm.read(q.get("path", ""))
            return self.send_json({"text": text} if text is not None else {"error": "no such file"}, 200 if text is not None else 404)
        self.send_json({"error": "not found"}, 404)

    def swarm_post(self, what, body):
        if what == "run":
            p, n = body.get("problem"), body.get("n")
            told = body.get("told") is not False  # false: the first message states no answer (swarm_play.PROMPT_UNTOLD)
            if not swarm_play.offered(p, told) or not isinstance(n, int) or not 1 <= n <= swarm_play.MAX_AGENTS:
                return self.send_json({"error": "unknown problem (another edition's only when not told the answer), "
                                                "or not 1 to MAX_AGENTS agents"}, 400)  # fmt: skip
            if not str(body.get("prompt", "")).strip() or not str(body.get("system", "")).strip():
                return self.send_json({"error": "an empty prompt"}, 400)
            try:
                budget = float(body.get("budget") or swarm_play.BUDGET)
                responses = int(body.get("max_responses") or swarm_play.MAX_RESPONSES)
                minutes = float(body.get("run_minutes") or swarm_play.RUN_MINUTES)
            except (TypeError, ValueError):
                return self.send_json({"error": "the budget, responses and run time must be numbers"}, 400)
            if not (budget > 0 and 1 <= responses <= swarm_play.MAX_RESPONSES and 1 <= minutes <= swarm_play.RUN_MINUTES):
                return self.send_json({"error": f"a budget above $0, 1 to {swarm_play.MAX_RESPONSES} responses and "
                                                f"1 to {swarm_play.RUN_MINUTES} minutes a run"}, 400)  # fmt: skip
            solo = body.get("solo") is True  # a lone agent: no Slack, no shared workspace (swarm_play.SYSTEM_SOLO)
            if solo and n != 1:
                return self.send_json({"error": "a lone agent is one agent (n: 1)"}, 400)
            try:  # `lemmas`: a set of an earlier team's results to hand the team (swarm_play.LEMMA_SETS)
                swarm = swarm_play.Swarm(self.swarm_llm, swarm_sandbox, p, str(body["system"]), str(body["prompt"]),
                                         list(body.get("notes") or []), n, budget, responses, minutes,
                                         answer=body.get("answer") if told else None, told=told, solo=solo,
                                         lemmas=body.get("lemmas") or None)  # fmt: skip
            except ValueError as e:
                return self.send_json({"error": str(e)}, 400)
            self.swarms[swarm.id] = swarm
            return self.send_json({"id": swarm.id, "key": f"swarm/{swarm.folder.name}"})
        swarm = self.swarms.get(body.get("id"))
        if swarm is None:
            return self.send_json({"error": "no such swarm run"}, 404)
        if what == "stop":
            swarm.end("stopped")
            return self.send_json({})
        if what == "post":
            thread = body.get("thread")
            try:
                row, tagged, unknown = swarm.post(str(body.get("text", "")), int(thread) if thread not in (None, "") else None)
            except (ValueError, TypeError) as e:
                return self.send_json({"error": str(e)}, 400)
            return self.send_json({"id": row["id"], "tagged": tagged, "unknown": unknown})
        self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or "{}")
        if self.path == "/api/restart":
            threading.Thread(target=restart, args=("asked from the page",), daemon=True).start()
            return self.send_json({"live": self.live_count()})
        if self.path.startswith("/api/swarm/"):
            return self.swarm_post(self.path.removeprefix("/api/swarm/"), body)
        if self.path.startswith("/api/archive/"):
            return self.archive_post(self.path.removeprefix("/api/archive/"), body)
        self.send_json({"error": "not found"}, 404)

    def poll(self, run, since):
        """A run's events from `since` on (a Swarm's or an Archive's), waiting up to HOLD seconds
        for one: {events, next, done}. 404 when the server doesn't hold the run (it ended a while ago, or the server
        restarted): the page then shows it from disk."""
        if run is None or since > len(run.events):
            return self.send_json({"error": "no such live run"}, 404)
        t0 = time.time()
        deadline = t0 + HOLD
        with run.cond:
            while len(run.events) <= since and not run.ended and time.time() < deadline:
                run.cond.wait(max(0.0, deadline - time.time()))
            while not run.ended and time.time() < t0 + LINGER:  # a few more tokens in this answer, not a poll each
                run.cond.wait(t0 + LINGER - time.time())
            new = run.events[since:since + BATCH]
            total = len(run.events)
        nxt = since + len(new)
        self.send_json({"events": coalesce(new), "next": nxt, "done": run.ended and nxt >= total})


def reap():
    """Ended runs leave memory KEEP_ENDED seconds after they end (a swarm's events can be hundreds of MB of deltas);
    pages then read them from disk."""
    seen = {}
    while True:
        time.sleep(30)
        now = time.time()
        for registry in Handler.registries().values():
            for k, r in list(registry.items()):
                if not r.ended:
                    continue
                if now - seen.setdefault(id(r), now) > KEEP_ENDED:
                    registry.pop(k, None)
                    seen.pop(id(r), None)
                    with r.cond:
                        r.events = []  # an archive still holds its swarms


def restart(why):
    """End every live run (each saves its state and says why), wait for them, and run this server again: the same
    command, environment and port."""
    if Handler.restarting:
        return
    Handler.restarting = True
    print(f"restarting: {why}", flush=True)
    for registry in Handler.registries().values():
        for r in live(registry):
            r.end("the server restarted")
    deadline = time.time() + 60
    while Handler.live_count() and time.time() < deadline:
        time.sleep(0.5)
    time.sleep(0.5)  # the last polls get their end event
    os.environ["SERVE_CAFFEINATED"] = "1"  # caffeinate -w waits on this pid, which execv keeps
    os.execv(sys.executable, [sys.executable, *sys.argv])


def imports_cleanly():
    """None if the code on disk imports (serve and all it imports), else its error's last line."""
    r = subprocess.run([sys.executable, "-c", f"import sys; sys.path[:0] = [{str(ROOT)!r}, {str(HERE)!r}]; import serve"],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)  # fmt: skip
    return None if r.returncode == 0 else (r.stderr.strip().splitlines() or ["exit " + str(r.returncode)])[-1]


def watch_code():
    """Restart when the code changes: at once if nothing is live, else when the page asks (Handler.stale)."""
    boot, checked = mtimes(sources()), None
    while True:
        time.sleep(2)
        now = mtimes(sources())
        if now == boot:
            Handler.stale = None
            continue
        time.sleep(2)  # an editor's several writes
        if mtimes(sources()) != now:
            continue
        if now != checked:
            checked, error = now, imports_cleanly()
        if error:
            Handler.stale = f"error: {error}"
        elif Handler.live_count() or not AUTO_RESTART:
            Handler.stale = "pending"
        else:
            return restart("the code changed")


def main():
    if sys.platform == "darwin" and not os.environ.get("SERVE_CAFFEINATED"):  # keep the Mac awake (not the display): swarms take hours
        subprocess.Popen(["caffeinate", "-i", "-s", "-w", str(os.getpid())])
    if why := Sandbox().ready():
        raise SystemExit(f"the sandbox isn't ready: {why}")
    # one model for the archives' agents and the swarms': each sets its own system prompt and tools
    Handler.llm = Handler.swarm_llm = swarm_play.agent_llm(threading.BoundedSemaphore(LLM_PARALLEL))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=reap, daemon=True).start()
    threading.Thread(target=watch_code, daemon=True).start()
    print(f"swarm: http://127.0.0.1:{PORT}/swarm.html  ·  archive: http://127.0.0.1:{PORT}/archive.html", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
