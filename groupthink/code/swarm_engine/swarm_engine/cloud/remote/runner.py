#!/usr/bin/env python3
"""Runs a job on the rented machine: sets it up, starts what the job needs, runs its commands, and says how far it is.

    python3 ~/jobs/<name>/swarm/runner.py job.json          (systemd starts it: start.sh)

It is the only thing on the machine that decides anything, and it needs nothing but the machine's own Python. The
controller, somewhere else, reads what this writes and does the rest: this never rents, copies off or terminates.
A job has a folder of its own, ~/jobs/<name>/, and this file lies in its swarm/ folder: everything is found from
there, so that a machine used for one job after another keeps them apart.

    swarm/status.json    where the job is: {"phase": "setup" | "starting" | "running" | "finished", "step", "steps",
                         "command", "exit", "failed", "updated", ...}. Rewritten whole at every change, and its
                         "updated" every half minute while this is alive.
    swarm/logs/          setup.log, job.log, a log for each service, and runner.log (what this itself printed)
    swarm/snap/          the job's sqlite files, each copied whole while nobody is half way through writing it
    swarm/done/          a mark for each setup step that is done, so that a machine that was restarted does not
                         do it again
    work/                the job's repos and files; its commands run in `workdir` under it

A command that fails is run again (`retries`), after the services are stopped and started: a run of the lab carries
on from its cache, so a server that hung costs the calls that were in flight and nothing else. Told to stop (systemd
sends SIGTERM), it stops the command, takes a last copy of the sqlite files and says it has finished. Whatever goes
wrong in here is a job that failed, and is said as that: the controller gives the machine back on "finished" and on
nothing else this writes.

Before anything else it adds the public ssh keys the job carries (`keys`: of whoever handed it in) to the ones the
machine accepts, so that they can get in and look.

It is run by the machine's own python3, whichever that is: nothing here needs more than Python 3.8.
"""
from __future__ import annotations

import json
import os
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
from pathlib import Path

HOME = Path.home()
SWARM = Path(__file__).resolve().parent  # what the controller sent, and what this writes
WORK = SWARM.parent / "work"             # the job's repos and files
STATUS = SWARM / "status.json"
status_lock, snapshot_lock, state = threading.Lock(), threading.Lock(), {}
stopping = threading.Event()             # told to stop
over = threading.Event()                 # the job has ended: what is left is the last copy and saying so
current: list = []                       # the command that is running, if one is


def say(**changes):
    """Write where the job is. Written to a new file that then takes the old one's place, so a reader never
    finds half of one."""
    with status_lock:
        state.update(changes, updated=time.strftime("%Y-%m-%d %H:%M:%S"), updated_at=time.time())
        new = STATUS.with_suffix(".new")
        new.write_text(json.dumps(state, indent=2) + "\n")
        os.replace(new, STATUS)


# A public ssh key as one line of authorized_keys: its kind, the key, a few words. The same as job.py's PUBLIC_KEY
# (a test holds the two equal): this file is sent alone, and what it is handed is checked here as well.
PUBLIC_KEY = r"(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(256|384|521)|sk-(ssh-ed25519|ecdsa-sha2-nistp256)@openssh\.com) [A-Za-z0-9+/=]+( [^\r\n]*)?"


def let_in(job: dict):
    """Whoever handed the job in may get into its machine: their public ssh keys (`keys` in the job) are added to
    the ones it accepts. Only what is a public key and nothing else is added (no options before it), a key that
    is there already is not added again, and the file is read and written as the bytes it is. Never in the way
    of the job: whatever is wrong with the file, the job runs."""
    try:
        given = job.get("keys")
        keys = [key for key in given if isinstance(key, str) and re.fullmatch(PUBLIC_KEY, key)] if isinstance(given, list) else []
        if not keys:
            return
        folder = HOME / ".ssh"
        folder.mkdir(mode=0o700, exist_ok=True)
        accepted = folder / "authorized_keys"
        if accepted.exists() and not accepted.is_file():        # a pipe, a folder: nothing to add a line to
            print("the ssh keys of whoever handed the job in were not added: ~/.ssh/authorized_keys is not a file", flush=True)
            return
        have = accepted.read_bytes() if accepted.exists() else b""
        there = {tuple(line.split()[:2]) for line in have.decode("utf-8", "replace").replace("\r", "\n").split("\n")}
        new = [key for key in keys if tuple(key.split()[:2]) not in there]
        if new:
            with open(accepted, "ab") as f:                     # on a line of its own, whatever the file ends with
                f.write((b"" if not have or have.endswith(b"\n") else b"\n") + "\n".join(new).encode() + b"\n")
            accepted.chmod(0o600)
            print(f"the machine now accepts {len(new)} more ssh key{'s' if len(new) > 1 else ''}: of whoever handed the job in", flush=True)
    except Exception as problem:
        print(f"the ssh keys of whoever handed the job in could not be added ({type(problem).__name__}: {problem})", flush=True)


def environment(job: dict) -> dict:
    return {**os.environ, "PATH": f"{HOME}/.local/bin:{HOME}/.cargo/bin:{os.environ.get('PATH', '/usr/bin:/bin')}",
            "PYTHONUNBUFFERED": "1", "SWARM_LOGS": str(SWARM / "logs"), **{key: str(value) for key, value in job.get("env", {}).items()}}


def run(command: str, log: Path, job: dict) -> int:
    """One shell command, in the job's folder, its output added to a log. Returns its exit code."""
    where = WORK / job.get("workdir", "")
    with open(log, "ab") as out:
        out.write(f"\n==== {time.strftime('%Y-%m-%d %H:%M:%S')} $ {command}\n".encode())
        out.flush()
        process = subprocess.Popen(["bash", "-c", command], cwd=where if where.is_dir() else WORK, env=environment(job),
                                   stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
        current.append(process)
        try:
            while process.poll() is None:
                if stopping.wait(0.5):
                    end(process)
            return process.returncode
        finally:
            current.remove(process)
            out.write(f"==== exit {process.returncode}\n".encode())


def end(process: subprocess.Popen, grace: float = 60.0):
    """Stop a command and everything it started: asked first (as ctrl-c would), then made to."""
    for sig, wait in ((signal.SIGINT, grace), (signal.SIGTERM, 15.0), (signal.SIGKILL, 15.0)):
        try:
            os.killpg(process.pid, sig)
        except OSError:
            return
        try:
            process.wait(timeout=wait)
            return
        except subprocess.TimeoutExpired:
            continue


class Service:
    """Something the commands need running beside them (a model server)."""

    def __init__(self, spec: dict, job: dict):
        self.spec, self.job, self.process = spec, job, None
        self.log = SWARM / "logs" / f"{spec['name']}.log"

    def start(self) -> str | None:
        """Start it and wait until it answers. Returns what went wrong, if something did."""
        where = WORK / self.job.get("workdir", "")
        out = open(self.log, "ab")
        out.write(f"\n==== {time.strftime('%Y-%m-%d %H:%M:%S')} $ {self.spec['command']}\n".encode())
        out.flush()
        self.process = subprocess.Popen(["bash", "-c", self.spec["command"]], cwd=where if where.is_dir() else WORK,
                                        env=environment(self.job), stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT,
                                        start_new_session=True)
        ready, limit = self.spec.get("ready"), time.time() + float(self.spec.get("timeout", 1800))
        while ready and time.time() < limit:
            if self.process.poll() is not None:
                return f"{self.spec['name']} stopped while starting (code {self.process.returncode}): see logs/{self.log.name}"
            if stopping.is_set():
                return "told to stop"
            try:
                with urllib.request.urlopen(ready, timeout=5) as answer:
                    if answer.status == 200:
                        return None
            except OSError:
                pass
            time.sleep(2.0)
        return f"{self.spec['name']} did not answer at {ready} in time" if ready else None

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            end(self.process, grace=45.0)
        self.process = None


def snapshot(job: dict):
    """A whole copy of each of the job's sqlite files, taken while no writer is half way through one. One at a
    time: the copy taken every few minutes and the last one write to the same file."""
    with snapshot_lock:
        for name in job.get("snapshots", []):
            source, target = WORK / name, SWARM / "snap" / name
            if not source.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            new = target.with_name(target.name + ".new")
            try:
                if new.exists():
                    new.unlink()
                read, write = sqlite3.connect(f"file:{source}?mode=ro", uri=True, timeout=120), sqlite3.connect(str(new))
                try:
                    read.backup(write)
                finally:
                    write.close()
                    read.close()
                os.replace(new, target)
            except (sqlite3.Error, OSError) as problem:
                say(snapshot_problem=f"{name}: {problem}")


def beside(job: dict):
    """While the job runs: say that this is alive every half minute, and copy its sqlite files every few. It goes
    on saying so while the job is being stopped, which can take minutes; it takes no copy once the job has ended."""
    every, last = float(job.get("snapshot_every", 300)), time.time()
    while True:
        time.sleep(30.0) if over.is_set() else over.wait(30.0)
        say()
        if time.time() - last >= every and not over.is_set():
            snapshot(job)
            last = time.time()


def main() -> int:
    job = json.loads(Path(sys.argv[1]).read_text())
    for folder in ("logs", "snap", "done"):
        (SWARM / folder).mkdir(parents=True, exist_ok=True)
    signal.signal(signal.SIGTERM, lambda *_: stopping.set())
    signal.signal(signal.SIGINT, lambda *_: stopping.set())
    if STATUS.exists():                                  # the machine was restarted: carry on, and say so
        try:
            state.update(json.loads(STATUS.read_text()))
        except ValueError:
            pass
    if state.get("phase") == "finished":                 # a job that is over does nothing more, at any restart of its
        return int(state.get("exit") or 0)               # machine: it lets nobody in again who was taken out since
    let_in(job)                                          # before the set-up: a job that fails early is the one to look at
    say(phase="setup", started=state.get("started") or time.strftime("%Y-%m-%d %H:%M:%S"), restarts=state.get("restarts", -1) + 1,
        steps=len(job["commands"]), step=0, exit=None, failed=None)
    threading.Thread(target=beside, args=(job,), daemon=True).start()
    services, code, failed = [], 0, None
    try:
        services = [Service(spec, job) for spec in job.get("services", [])]
        for number, command in enumerate(job.get("setup", []), 1):
            mark = SWARM / "done" / f"setup-{number}"
            if mark.exists():
                continue
            say(phase="setup", command=command, setup_step=number, setup_steps=len(job["setup"]))
            code = run(command, SWARM / "logs/setup.log", job)
            if code or stopping.is_set():
                failed = f"setup step {number} of {len(job['setup'])}: {command[:200]}"
                break
            mark.write_text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        def serve() -> str | None:
            say(phase="starting", command=", ".join(spec["name"] for spec in job.get("services", [])))
            for service in services:
                problem = service.start()
                if problem is not None:
                    return problem
            return None

        if failed is None:
            failed = serve()
        for number, command in enumerate(job["commands"], 1):
            if failed is not None or stopping.is_set():
                break
            for attempt in range(1, int(job.get("retries", 2)) + 2):
                say(phase="running", step=number, command=command, attempt=attempt)
                code = run(command, SWARM / "logs/job.log", job)
                if code == 0 or stopping.is_set() or attempt > int(job.get("retries", 2)):
                    break
                for service in reversed(services):       # what it leaned on may be what failed: start that afresh
                    service.stop()
                failed = serve()
                if failed is not None:
                    break
            if code and failed is None:
                failed = f"command {number} of {len(job['commands'])} ended with code {code}: {command[:200]}"
    except Exception as problem:                         # a mistake in here, or something of the machine's: the job has failed
        failed = f"the runner went wrong ({type(problem).__name__}: {problem})"
        traceback.print_exc()
    finally:
        over.set()
        for service in reversed(services):
            try:
                service.stop()
            except Exception:
                traceback.print_exc()
        try:
            snapshot(job)
        except Exception:
            traceback.print_exc()
        stopped = stopping.is_set()
        code = (code or 1) if failed else 0
        say(phase="finished", exit=code, failed="told to stop" if stopped and not failed else failed,
            stopped=stopped, finished=time.strftime("%Y-%m-%d %H:%M:%S"))
    return code


if __name__ == "__main__":
    sys.exit(main())
