"""Experiment tracking: one run = one folder, written so that a person can read it and a script can resume it.

    experiments/<experiment>/runs/<run>/
        config.json        every setting of every arm, the command, the git commit, the machine, start and finish, status
        log.txt            what the run printed, with timestamps
        episodes.jsonl     one line per (arm, problem): the answer every agent held after each step, and the scores
        posts.jsonl        one line per step of an agent: its tools, its answer, and its Python file when it ran it
        looks.jsonl        one line per look: who read whose file after which step, and what it wrote of it
        transcripts.jsonl  one line per model call: what it was shown, the thought, the reply (git-ignored)
        engine.jsonl       one line per engine call: seeds, batches, tokens, seconds (git-ignored)
        summary.json/.md   the run's numbers and tables

Everything is appended as it happens, so a run that is interrupted loses at most the step in flight. Starting
the same run again resumes it: the settings must match what is in config.json, and finished (arm, problem)
pairs are skipped. `lab show` reads a run.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from .paths import ROOT


def git_state() -> dict:
    def ask(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""
    return {"commit": ask("rev-parse", "HEAD"), "uncommitted_changes": bool(ask("status", "--porcelain"))}


def machine_state() -> dict:
    """The machine a run is made on, as far as it tells a run made on the laptop from one made on a rented GPU:
    the system, the Python that runs agents' files, the GPU if there is one, and the job that rented it."""
    import platform
    out = {"system": platform.system(), "machine": platform.machine(), "python": platform.python_version()}
    if sys.platform.startswith("linux"):
        from . import linux
        out["sandbox"] = f"linux {linux.VERSION}"         # what runs agents' files there, which the harness's version does not cover
        try:
            from swarm_engine.vllm import gpu
            out["gpu"] = gpu() or None
        except Exception:                                  # a record, not something a run should stop for
            out["gpu"] = None
    out |= {name.removeprefix("SWARM_CLOUD_").lower(): os.environ[name] for name in ("SWARM_CLOUD_JOB", "SWARM_CLOUD_INSTANCE_TYPE",
                                                                                   "SWARM_CLOUD_REGION") if os.environ.get(name)}
    return out


def now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


class Run:
    def __init__(self, folder: str | Path, settings: dict | None = None, may_change: tuple[str, ...] = (),
                 may_add: tuple[str, ...] = ()):
        """Start the run stored in `folder`, or resume it if it exists.

        `settings` is everything that defines the run. On resume they must equal the saved ones, except for the
        keys in `may_change` (things it is safe to extend, like how many problems to play). Keys that start
        with one of `may_add` may be new or left out this time, but not different: a run can gain an arm, and
        an arm that is not being run now stays in its settings.
        With `settings=None` the run is opened just for reading.
        """
        self.folder = Path(folder)
        self.config_path = self.folder / "config.json"
        self.resumed = self.config_path.exists()
        if settings is None:
            if not self.resumed:
                raise FileNotFoundError(f"no run at {self.folder}")
            self.config = json.loads(self.config_path.read_text())
            return
        settings = json.loads(json.dumps(settings, default=str))   # exactly what will be on disk
        if self.resumed:
            self.config = json.loads(self.config_path.read_text())
            saved = self.config["settings"]
            def allowed(k: str) -> bool:
                return k in may_change or (k.startswith(may_add) and (k not in saved or k not in settings))
            changed = {k: (saved.get(k), settings.get(k)) for k in sorted(set(saved) | set(settings))
                       if saved.get(k) != settings.get(k) and not allowed(k)}
            if changed:
                lines = "\n".join(f"  {k}: saved {a!r}, now {b!r}" for k, (a, b) in changed.items())
                raise SystemExit(f"{self.folder} already holds a run with different settings:\n{lines}\n"
                                 "Give this run a new --name, or delete that folder to start it over.")
            added = (lambda k: k.startswith(may_add)) if may_add else (lambda k: False)
            arms = {**{k: v for k, v in saved.items() if added(k)}, **{k: v for k, v in settings.items() if added(k)}}
            self.config.update(settings={**{k: v for k, v in settings.items() if not added(k)}, **arms}, status="running")   # arms stay in the order they were first run
            here, been = machine_state(), self.config.setdefault("machines", [])
            if not been or been[-1] != here:                   # carried on somewhere else than it was last at work
                been.append(here)
            self._write_config()
            self.say(f"resuming ({' '.join(sys.argv)})")
        else:
            self.folder.mkdir(parents=True, exist_ok=True)
            self.config = {"run": self.folder.name, "experiment": self.folder.parent.parent.name, "status": "running",
                           "started": now(), "finished": None, "command": " ".join(sys.argv), "git": git_state(),
                           "machines": [machine_state()], "settings": settings}
            self._write_config()
            self.say(f"started ({' '.join(sys.argv)})")

    # ---- writing
    def _write_config(self):
        self.config_path.write_text(json.dumps(self.config, indent=2) + "\n")

    def say(self, message: str):
        """Print a line and keep it in log.txt."""
        print(message, flush=True)
        with open(self.folder / "log.txt", "a") as f:
            f.write(f"{now()}  {message}\n")

    def write(self, stream: str, row: dict):
        """Append one JSON line to <stream>.jsonl. If an interruption left the file ending mid-line, the new
        row starts on a line of its own (the cut-off line is skipped by `read`)."""
        line = (json.dumps(row, ensure_ascii=False) + "\n").encode()
        with open(self.folder / f"{stream}.jsonl", "ab+") as f:
            size = f.seek(0, os.SEEK_END)
            if size:
                f.seek(size - 1)
                if f.read(1) != b"\n":
                    line = b"\n" + line
            f.write(line)

    def keep(self, stream: str, wanted) -> int:
        """Rewrite <stream>.jsonl keeping only the rows `wanted(row)` accepts. Used on resume to drop what a
        half-finished step had written, so that redoing the step does not log it twice. Returns rows dropped."""
        rows = self.read(stream)
        kept = [row for row in rows if wanted(row)]
        if len(kept) != len(rows):
            path = self.folder / f"{stream}.jsonl"
            path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept))
        return len(rows) - len(kept)

    def save(self, name: str, content: dict):
        (self.folder / f"{name}.json").write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n")

    def finish(self):
        self.config.update(status="done", finished=now())
        self._write_config()
        self.say("done")

    # ---- reading
    def read(self, stream: str) -> list[dict]:
        path = self.folder / f"{stream}.jsonl"
        if not path.exists():
            return []
        rows = []
        for line in path.read_text().splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:   # a line cut short by an interruption; whatever it held is redone
                continue
        return rows

    def load(self, name: str) -> dict | None:
        path = self.folder / f"{name}.json"
        return json.loads(path.read_text()) if path.exists() else None

    def path(self, *parts: str) -> Path:
        return self.folder.joinpath(*parts)
