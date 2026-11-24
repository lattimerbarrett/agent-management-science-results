"""Takes a job from "wanted" to "given back": the one thing that rents a machine, and the one thing that returns it.

    python3 -m swarm_engine.cloud launch <job>     take in a job that was handed in, start its controller, and come back
    python3 -m swarm_engine.cloud tick             start a controller for every job that should have one and has none (cron)
    python3 -m swarm_engine.cloud status [<job>]   where each job stands, what it has cost, what its machine last said
    python3 -m swarm_engine.cloud logs <job>       the end of what it has printed
    python3 -m swarm_engine.cloud stop <job>       end it: copy back what there is, give the machine back
    python3 -m swarm_engine.cloud setup            once on this machine: an ssh key, registered with Lambda, and the cron line
    python3 -m swarm_engine.cloud machines         every machine the account is renting now, whoever started it

A job goes through these, and where it stands is written down after every step (state.json), so a controller that
dies, or whose machine is restarted, is started again and carries on:

    waiting       asks every 20 seconds whether one of the job's kinds of machine is free, and launches the first
    booting       until Lambda says the machine is up (one that is not after 25 minutes is given back, and it waits again)
    connecting    until it answers over ssh
    sending       the job's repos and files go over, and the job is started there under systemd
    running       every minute: what the job has made is copied back, and how far it is. A machine that is gone is
                  replaced, and the job carries on from the caches that were copied back (`relaunches`)
    finishing     the job has ended (or failed, or was told to stop): everything is copied back until nothing is left to copy
    ending        the machine is given back, and asked after until Lambda says it is gone; then the job's caches are
                  kept for the jobs after it
    kept          only for a job that says `keep_on_failure`, and failed: the machine is left up to be looked at,
                  until `stop`, for `keep_hours` (three, unless the job says otherwise), until the job has had its
                  `max_hours`, or until Lambda no longer has it: whichever comes first
    done | failed | stopped

The rules that keep a machine from being left to bill, and results from being lost with one:
  - A machine is given back when its job has ended and all of it is copied, when the job failed (unless the job says
    to keep it, to be looked at), and when it is told to stop. There is no limit on how long a job may run unless
    the job sets one (`max_hours`, counted over all its machines).
  - A machine is not given back while what it made has not been copied. If it cannot be reached, or it answers and
    the copy does not work (a full disk here), the controller keeps trying and says why: both show in `status` in
    capitals. That ends by itself in two ways only: Lambda says the machine is gone, or it has gone on for
    `silent_hours` (six, unless the job says otherwise), when the machine is given up. A job that was still running
    then gets another machine; one that had ended fails, with what did come. `stop --now` ends it at once.
  - Giving a machine back is one place in this file (`ending`). It asks Lambda to terminate the machine and does
    not let go until Lambda has said yes and no longer lists the machine as up. A machine that is given up on
    goes through there too before another is waited for. Nothing else that can go wrong (a cache that cannot be
    kept, a notice that cannot be sent) comes before it.
  - "Gone" is Lambda's word and nothing else's: its list of machines, asked and answered, without the machine or
    with it terminated. No error, and no answer from anything in between, is read as "gone".
  - A launch cannot be asked twice safely, so a job's machine carries a name that is this controller's and this
    job's alone. A launch that was not answered is looked for by that name for five minutes before another is
    made; and before a job ends, whatever carries its name is given back, known of or not.
  - Lambda saying no once does not end a job: from `running` on, never; before that, after five in a row.
  - Only a machine this job launched is given back. One that was there before (`instance` in the job) is left
    alone unless the job says otherwise. It is used under a folder and a unit of the job's own, and not at all
    while another job runs on it.
  - Whatever goes wrong in the controller itself is written down and tried again; `status` shows it, shows in
    capitals when nothing is looking after a job that is not over, and lists machines that carry this
    controller's name and belong to no job it knows.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import time
import traceback
from pathlib import Path

from .job import OVER, Job, State, home, ident, jobs, key_in, now
from .lambda_api import GONE, NO_CAPACITY, Lambda, Refused

POLL = 20.0               # seconds between asking whether a machine is free
MIRROR = 60.0             # seconds between copying a running job's results back
BOOT_LIMIT = 25 * 60      # seconds a machine may take to come up before it is given back and another is waited for
CONNECT_LIMIT = 15 * 60   # seconds a machine that is up may take to answer over ssh
SEND_LIMIT = 30 * 60      # seconds sending a job to a machine may take, however often it is tried
SEND_TRIES = 5            # and how often it is tried
SILENT = 10 * 60          # seconds a machine may be unreachable before Lambda is asked whether it is still there
QUIET = 3 * 60            # seconds a job may go without saying it is alive before the machine is asked whether it runs
UNHEARD = 5 * 60          # seconds an unanswered launch is looked for by its name before another is made
LIST_LAG = 3 * 60         # seconds after a launch in which Lambda's list may not show the machine yet
TERMINATING = 10 * 60     # seconds Lambda may call a machine "terminating", after its yes, before it is let go of
CHANGING = 15 * 60        # seconds an ended job's files may go on changing before they are taken as they are
WORRY = 30 * 60           # seconds something may go on before whoever wants to be told is told
REFUSALS = 5              # how often in a row Lambda may say no before a job that has no machine at work fails
IN_USE = 8                # what the rented machine's side exits with when another job is running on it
NEVER = ("unknown-instance-type",)       # of what Lambda may say no with: what asking again cannot change
REMOTE = Path(__file__).with_name("remote")


class NoKey(Exception):
    """There is no API key here, and the job needs one."""


def api_key() -> str:
    """This machine's Lambda API key: what its file holds, or LAMBDA_API_KEY where there is no file. The file comes
    first, so that every controller here asks with the one key, whoever started it and from where. Only the key
    is taken out of what is kept (`key_in`), and nothing of it is quoted when there is none to take: a key with
    a second line under it once went, with the error it caused, into a job's log and its notice (a review,
    2026-10-11)."""
    stored = home() / "lambda_api_key"
    held = stored.read_text(errors="replace") if stored.exists() else ""
    kept = held if held.strip() else os.environ.get("LAMBDA_API_KEY") or ""
    if not kept.strip():
        raise NoKey(f"no Lambda API key: put it in {stored} (readable by you alone), or in LAMBDA_API_KEY")
    try:
        return key_in(kept)
    except ValueError:
        raise NoKey(f"what is kept as the Lambda API key is not one: a key is one word, alone on a line ({stored}, or LAMBDA_API_KEY)") from None


def key_name() -> str:
    """The name the ssh key of this machine has at Lambda (`setup` gives it one)."""
    named = home() / "key_name"
    return named.read_text().strip() if named.exists() else "swarm-cloud"


class Remote:
    """ssh and rsync to a job's machine. Nothing of this machine's own ssh settings changes how it is reached."""

    def __init__(self, ip: str, user: str, key: Path, known_hosts: Path):
        self.at = f"{user}@{ip}"
        self.options = ["-F", "/dev/null", "-i", str(key), "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
                        "-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={known_hosts}", "-o", "ConnectTimeout=15",
                        "-o", "ServerAliveInterval=15", "-o", "ServerAliveCountMax=4", "-o", "LogLevel=ERROR"]

    def ssh(self, command: str, timeout: float = 120.0) -> subprocess.CompletedProcess:
        """A command there. ssh's own code for not getting through is 255."""
        return subprocess.run(["ssh", *self.options, self.at, command], capture_output=True, text=True, timeout=timeout)

    def push(self, local: Path, remote: str, timeout: float = 3600.0) -> subprocess.CompletedProcess:
        """Lay the contents of a folder here over a folder there. What was half way when a connection went is
        taken up from there the next time."""
        return subprocess.run(["rsync", "-az", "--timeout=120", "--partial-dir=.rsync-partial", "-e", shlex.join(["ssh", *self.options]),
                               f"{local}/", f"{self.at}:{remote}/"], capture_output=True, text=True, timeout=timeout)

    def pull(self, names: list[str], local: Path, root: str, timeout: float = 3600.0) -> subprocess.CompletedProcess:
        """Copy the named files (paths from the folder `root` there) to the same paths under a folder here. It
        prints a line beginning `>f` for every file it had to bring. A file that is half way here when the
        connection goes is kept aside, not in the place of the whole one that was there. Only files come: a
        link made on the rented machine could point at anything on this one, and is left there."""
        local.mkdir(parents=True, exist_ok=True)
        return subprocess.run(["rsync", "-rptz", "--timeout=120", "--partial-dir=.rsync-partial", "--itemize-changes", "--files-from=-",
                               "-e", shlex.join(["ssh", *self.options]), f"{self.at}:{root}/", f"{local}/"],
                              input="\n".join(names) + "\n", capture_output=True, text=True, timeout=timeout)


class Controller:
    def __init__(self, folder: Path, api: Lambda | None = None, remote=None, sleep=time.sleep, clock=time.time):
        """`api`, `remote` (a function from a machine to a `Remote`) and the clock stand in for the world in tests."""
        self.folder = Path(folder)
        self.job, self.state = Job.load(self.folder), State.load(self.folder)
        self._api, self._remote, self.sleep, self.clock = api, remote, sleep, clock
        self.last_asked = self.last_said = 0.0
        self.wrong = 0                                           # how often in a row the controller itself has gone wrong

    # ---------------------------------------------------------------- what it works with
    @property
    def api(self) -> Lambda:
        if self._api is None:
            self._api = Lambda(api_key())
        return self._api

    @property
    def ours(self) -> bool:
        """Whether the machine is this job's to give back."""
        return bool(self.state.machine.get("ours") and self.state.machine.get("id"))

    def remote(self) -> Remote:
        machine = self.state.machine
        if self._remote is not None:
            return self._remote(machine)
        key = Path(machine["key"]).expanduser() if machine.get("key") else home() / "key"      # a machine that was there may take another
        return Remote(machine["ip"], machine.get("user", "ubuntu"), key, self.folder / "known_hosts")

    def clean(self, line: str) -> str:
        """A line as it may be written down or told: without the API key, whatever put it there."""
        key = getattr(self._api, "key", None)
        return line.replace(key, "<the API key>") if isinstance(key, str) and key else line

    def log(self, line: str):
        line = self.clean(line)
        self.state.note = line
        with open(self.folder / "controller.log", "a") as f:
            f.write(f"{now()}  [{self.state.phase}] {line}\n")

    def said_once(self, line: str):
        """Log something that goes on being true when it changes and every ten minutes, not at every try."""
        if line != self.state.note or self.clock() - self.last_said > 600:
            self.last_said = self.clock()
            self.log(line)

    def to(self, phase: str, line: str) -> float:
        self.state.phase = phase
        self.log(line)
        self.state.save(self.folder)
        return 0.0

    def told_to_stop(self) -> str | None:
        """"now" if the job is to be ended without copying anything more, "" if it is to be ended, None if not."""
        flag = self.folder / "stop"
        return flag.read_text().strip() if flag.exists() else None

    def notify(self, line: str):
        """Tell whoever wants to be told, if this machine has a program for that. Never in the way of anything."""
        program = home() / "notify"
        try:
            if os.access(program, os.X_OK):
                subprocess.run([str(program), self.job.name, self.state.phase, self.clean(line)], timeout=60, capture_output=True,
                               stdin=subprocess.DEVNULL)
        except Exception:
            pass

    def worry(self, about: str, seconds: float, line: str):
        """Tell of something that has gone on for half an hour, once for a machine."""
        if seconds > WORRY and not self.state.machine.get(f"told_{about}"):
            self.state.machine[f"told_{about}"] = True
            self.notify(line)

    # ---------------------------------------------------------------- the whole way
    def run(self):
        """Carry the job on from where it stands until nothing more is to be done for it."""
        while self.state.phase not in OVER:
            before = self.state.phase
            try:
                pause = self.step()
                self.state.refusals = self.wrong = 0
            except (Refused, NoKey) as refused:
                # Lambda said no, or there is no key to ask it with. A job that has a machine at work is never
                # ended for that, and a machine is never let go of for it: it is asked again. A job that has
                # none at work yet is ended when it goes on, or at once when asking again cannot change it.
                self.state.refusals += 1
                early = before in ("waiting", "booting", "connecting", "sending")
                hopeless = isinstance(refused, NoKey) or refused.code in NEVER
                if early and (hopeless or self.state.refusals >= REFUSALS):
                    pause = self.fail(f"{'Lambda refused' if isinstance(refused, Refused) else 'cannot go on'}: {refused}")
                else:
                    held = before == "ending" and self.ours
                    self.log((f"THE MACHINE COULD NOT BE GIVEN BACK ({refused}): it is still billed" if held else f"Lambda said no ({refused})")
                             + ". Asking again in a minute")
                    if held and self.state.refusals == 3:
                        self.notify(self.state.note)
                    pause = 60.0
            except (OSError, subprocess.SubprocessError, ConnectionError) as problem:      # the network, for a moment: try again
                self.log(f"{type(problem).__name__}: {problem}")
                pause = POLL
            except Exception:                                    # a mistake in here: written down, and tried again
                self.wrong += 1
                self.log("the controller went wrong, and tries again in a minute:\n" + traceback.format_exc())
                if self.wrong == 5:
                    self.notify("the controller keeps going wrong: " + traceback.format_exc().strip().splitlines()[-1])
                pause = 60.0
            self.state.save(self.folder)
            if pause:
                self.sleep(pause)

    def step(self) -> float:
        """One step from where the job stands. Returns how long to wait before the next."""
        stop, phase = self.told_to_stop(), self.state.phase
        if stop is not None and phase in ("waiting", "booting", "connecting", "sending", "kept"):
            return self.give_up("stopped", "told to stop" + ("" if phase == "kept" else " before the job had begun"))
        if stop == "now" and phase in ("running", "finishing"):
            return self.give_up("stopped", "told to stop now: what was not copied back is lost")
        return getattr(self, phase)()

    # ---------------------------------------------------------------- getting a machine
    def waiting(self) -> float:
        job, state = self.job, self.state
        if job.instance:                                         # a machine that is already there
            state.machine = {"ip": job.instance["ip"], "user": job.instance.get("user", "ubuntu"), "id": job.instance.get("id"),
                             "kind": job.instance.get("kind", "given"), "region": job.instance.get("region", ""),
                             "cents": job.instance.get("cents", 0), "ours": bool(job.instance.get("terminate") and job.instance.get("id")),
                             "key": job.instance.get("key"), "active_at": self.clock()}
            return self.to("connecting", f"using the machine at {job.instance['ip']}" + ("" if self.ours else ": it is not this job's to give back"))
        there = self.api.named(job.machine_name)
        if there:                                                # a launch of this job's went through, though nobody heard of it
            kind = there[0].get("instance_type", {})
            return self.took(there[0]["id"], kind.get("name", "?"), there[0].get("region", {}).get("name", "?"),
                             kind.get("price_cents_per_hour", 0), "found")
        if state.unheard and self.clock() - state.unheard < UNHEARD:
            return POLL                                          # a launch was sent and not answered: it may yet show under its name
        state.unheard = None
        state.polls += 1
        free = self.api.free(job.kinds, job.regions)
        if not free:
            if state.polls == 1 or state.polls % 90 == 0:
                self.log(f"none of {', '.join(job.kinds)} is free" + (f" in {', '.join(job.regions)}" if job.regions else "")
                         + f" (asked {state.polls} times)")
            return POLL
        kind, region, cents = free[0]
        try:
            machine = self.api.launch(kind, region, ssh_key=key_name(), name=job.machine_name, image=job.image)
        except Refused as refused:
            if refused.code == NO_CAPACITY:                      # somebody else was quicker
                return POLL
            raise
        except ConnectionError:                                  # it may have gone through: the name will show
            state.unheard = self.clock()
            self.log(f"the launch was not answered: looking for a machine called {job.machine_name} before launching another")
            return POLL
        self.took(machine, kind, region, cents, "launched")
        return 5.0

    def took(self, machine: str, kind: str, region: str, cents: int, how: str) -> float:
        self.state.unheard = None
        self.state.machine = {"id": machine, "kind": kind, "region": region, "cents": cents, "ours": True, "user": "ubuntu",
                              "launched_at": self.clock(), "launched": now()}
        return self.to("booting", f"{how} {kind} in {region} at ${cents / 100:.2f} an hour ({machine})")

    def booting(self) -> float:
        machine = self.state.machine
        seen = next((i for i in self.api.instances() if i.get("id") == machine["id"]), None)
        if seen is None and self.clock() - machine["launched_at"] < LIST_LAG:      # just launched: Lambda may not show it yet
            return 10.0
        if seen is None or seen.get("status") in GONE:
            return self.lose(f"the machine was gone before it came up ({(seen or {}).get('status', 'unknown to Lambda')})")
        if seen.get("status") == "active" and seen.get("ip"):
            machine.update(ip=seen["ip"], active_at=self.clock(), active=now())
            return self.to("connecting", f"the machine is up at {seen['ip']} after {(self.clock() - machine['launched_at']) / 60:.0f} minutes")
        if self.clock() - machine["launched_at"] > BOOT_LIMIT:
            return self.lose(f"the machine was not up after {BOOT_LIMIT // 60} minutes ({seen.get('status')})")
        return 10.0

    def connecting(self) -> float:
        machine = self.state.machine
        try:
            if self.remote().ssh("true", timeout=45).returncode == 0:
                return self.to("sending", "the machine answers over ssh")
        except subprocess.TimeoutExpired:
            pass
        machine.setdefault("connect_since", self.clock())
        if self.clock() - machine["connect_since"] > CONNECT_LIMIT:
            return self.lose(f"the machine did not answer over ssh in {CONNECT_LIMIT // 60} minutes")
        return 10.0

    # ---------------------------------------------------------------- sending the job and starting it
    def pack(self) -> tuple[Path, list[str]]:
        """Everything that goes into the job's swarm/ folder on the machine, in a folder here; and which caches
        it begins with."""
        job, machine, parcel = self.job, self.state.machine, self.folder / "parcel"
        shutil.rmtree(parcel, ignore_errors=True)
        (parcel / "files").mkdir(parents=True)
        for name in ("repos", "files"):
            if (self.folder / "payload" / name).is_dir():
                shutil.copytree(self.folder / "payload" / name, parcel / name, dirs_exist_ok=True)
        seeded = []
        for to, kept in job.seeds.items():
            # after a machine was lost: what was copied back from it, which is newer. Otherwise what earlier jobs
            # kept for this one, and not while a job that has ended is being merged into that.
            copied, kept = self.folder / "mirror/swarm/snap" / to, home() / "cache" / kept
            if not copied.exists() and not kept.exists():
                continue
            (parcel / "files" / to).parent.mkdir(parents=True, exist_ok=True)
            if copied.exists():
                shutil.copy2(copied, parcel / "files" / to)
            else:
                with locked(kept.parent):
                    shutil.copy2(kept, parcel / "files" / to)
            seeded.append(f"{to} ({(parcel / 'files' / to).stat().st_size / 2**20:.0f} MB)")
        for script in ("runner.py", "start.sh"):
            shutil.copy2(REMOTE / script, parcel / script)
        sent = json.loads((self.folder / "job.json").read_text())
        sent["env"] = {**job.env, "SWARM_CLOUD_JOB": job.name, "SWARM_CLOUD_INSTANCE_TYPE": machine.get("kind", ""),
                       "SWARM_CLOUD_REGION": machine.get("region", "")}
        (parcel / "job.json").write_text(json.dumps(sent, indent=2) + "\n")
        return parcel, seeded

    def sending(self) -> float:
        """Every try is counted before it is made, so that one that goes wrong in here counts too: a machine is
        not held, billed, by a job that cannot be sent to it."""
        job, machine, remote = self.job, self.state.machine, self.remote()
        machine.setdefault("send_since", self.clock())
        if machine.get("send_tries", 0) >= SEND_TRIES or self.clock() - machine["send_since"] > SEND_LIMIT:
            return self.lose(f"the job could not be sent to the machine ({machine.get('send_wrong') or 'the controller went wrong: see its log'})")
        machine["send_tries"], machine["send_wrong"] = machine.get("send_tries", 0) + 1, None
        parcel, seeded = self.pack()
        # The job's folder there is this job's alone: one left by another job of the same name (on a machine that
        # is used again) is moved aside, and nothing is done while another job runs on the machine.
        root, token = shlex.quote(job.root), re.sub(r"\W", "", f"{ident()}{self.state.began}")
        ready = (f'have=$(cat {root}/swarm/token 2>/dev/null || true)\nif [ "$have" != {token} ]; then\n'
                 "    busy=$(systemctl list-units --type=service --state=active,activating,deactivating --no-legend --plain 'swarm-job-*' "
                 "2>/dev/null | awk '{print $1}' | head -n 1)\n"
                 f'    if [ -n "$busy" ]; then echo "another job is running on this machine ($busy)" >&2; exit {IN_USE}; fi\n'
                 f"    if [ -e {root} ]; then mv {root} {root}.before-$(date +%s) || exit 1; fi\nfi\n"
                 f"mkdir -p {root}/swarm {root}/work && echo {token} > {root}/swarm/token")
        for what, step in (("making the job's folder there", lambda: remote.ssh(ready)),
                           ("sending the job", lambda: remote.push(parcel, f"{job.root}/swarm")),
                           ("starting the job", lambda: remote.ssh(f"bash {root}/swarm/start.sh {shlex.quote(job.name)}", timeout=900))):
            try:
                done = step()
                wrong = None if done.returncode == 0 else (done.stderr or done.stdout).strip()[-300:] or f"code {done.returncode}"
                in_use = done.returncode == IN_USE
            except subprocess.TimeoutExpired:
                wrong, in_use = "it took too long", False
            if wrong is not None:
                machine["send_wrong"] = f"{what}: {wrong}"
                self.log(f"{what} did not work (try {machine['send_tries']} of {SEND_TRIES}): {wrong}")
                return self.lose(f"the machine is in use: {wrong}") if in_use else 30.0
        shutil.rmtree(parcel, ignore_errors=True)
        machine["started_at"] = self.clock()
        self.to("running", "the job is started" + (f"; it begins with {', '.join(seeded)}" if seeded else ""))
        return 15.0

    # ---------------------------------------------------------------- while it runs
    def deaf(self, why: str) -> str:
        self.state.unreachable = self.state.unreachable or self.clock()
        self.said_once(f"the machine does not answer ({why.strip()[-200:] or 'no reason given'}): still trying")
        return "deaf"

    def troubled(self, why: str) -> str:
        self.state.trouble = why.strip()[-300:] or "no reason given"
        self.state.machine.setdefault("trouble_at", self.clock())
        self.said_once(f"the machine answers, and the copy does not work: {self.state.trouble}")
        return "trouble"

    def copy_back(self) -> str:
        """Read how far the job is, and copy back its logs, its snapshots, and the files it made or changed under
        its `mirror` folders. How the job stands is read over ssh before its files are listed, so it is known
        even when nothing can be copied, and a job that says it has finished has all its files in that list.
        Says how it went:

            "clean"      there was nothing left to bring
            "came"       something was brought (so there may be more)
            "deaf"       the machine could not be reached (`state.unreachable` says since when)
            "trouble"    it answered, and the copy did not work (`state.trouble` says why)

        Whether the machine can be reached is what ssh says of the first command, and nothing else: a copy that
        fails after that, for whatever reason, is trouble with the copy, which is said and looked into, and is
        never taken for a machine that is merely slow to answer."""
        job, state, remote = self.job, self.state, self.remote()
        made = " ".join(shlex.quote(f"work/{path}") for path in job.mirror)
        look = (f"cd {shlex.quote(job.root)} || exit 9; cat swarm/status.json 2>/dev/null; echo; echo '==== files'; "
                "find swarm/status.json swarm/started swarm/logs swarm/snap -type f ! -name '*.new' 2>/dev/null; "
                + (f"find {made} -type f -newer swarm/started ! -path '*/__pycache__/*' 2>/dev/null; " if made else "") + "true")
        try:
            listed = remote.ssh(look, timeout=300)
        except subprocess.TimeoutExpired:
            return self.deaf("it did not answer in five minutes")
        if listed.returncode == 255:
            return self.deaf(listed.stderr)
        state.unreachable = None
        if listed.returncode:
            return self.troubled(f"the job's folder there could not be looked at (code {listed.returncode}): {listed.stderr}")
        said, _, names = listed.stdout.partition("==== files")
        try:
            if said.strip():
                state.remote = json.loads(said)
        except ValueError:
            pass
        names = [line for line in names.splitlines() if line.strip()]
        came = None
        if names:
            try:
                came = remote.pull(names, self.folder / "mirror", job.root)
            except subprocess.TimeoutExpired:
                return self.troubled("the copy did not finish in an hour")
            if came.returncode == 24:                            # a file that was listed had gone again: the next copy has it right
                return "came"
            if came.returncode:                                  # some file could not be read there, or written here, or the copy broke
                return self.troubled(f"rsync gave code {came.returncode}: {came.stderr}")
            state.mirrored = now()
        state.trouble = None
        state.machine.pop("trouble_at", None)
        return "came" if came is not None and any(line.startswith(">f") for line in came.stdout.splitlines()) else "clean"

    def stop_if_due(self):
        """Tell the job to stop, when it was told to or has had its hours, and go on telling it until the machine
        has taken that."""
        job, state = self.job, self.state
        why = "was told to stop" if self.told_to_stop() is not None else (
            f"has had its {job.max_hours:g} hours" if job.max_hours and state.all_hours(self.clock()) > job.max_hours else None)
        if why and not state.stopping:
            state.stopping = why
            self.log(f"the job {why}: telling it to stop")
        if state.stopping and not state.stop_sent:
            try:                                                 # it stops its command, copies its caches, says it has finished
                taken = self.remote().ssh(f"sudo systemctl stop {shlex.quote(job.unit)}", timeout=400).returncode == 0
            except subprocess.TimeoutExpired:
                taken = False
            if taken:
                state.stop_sent = True
                self.log("the machine has taken that: the job is stopping")

    def running(self) -> float:
        job, state = self.job, self.state
        self.stop_if_due()
        reached = self.copy_back()
        if reached == "deaf":
            silent = self.clock() - state.unreachable
            if job.silent_hours and silent > job.silent_hours * 3600:
                return self.lose(f"the machine has not answered for {job.silent_hours:g} hours: it is given up")
            if silent > SILENT and self.ours and self.clock() - self.last_asked > 300:
                self.last_asked = self.clock()
                status = self.api.status(state.machine["id"])
                if status is None or status in GONE:
                    return self.lose(f"Lambda says the machine is {status or 'not there'}")
                self.log(f"the machine has not answered for {silent / 60:.0f} minutes; Lambda says it is {status}. Still trying")
            self.worry("silent", silent, f"the machine has not answered for {silent / 60:.0f} minutes")
            return 30.0
        if reached == "trouble":
            self.worry("trouble", self.clock() - state.machine["trouble_at"], f"what the job makes cannot be copied back: {state.trouble}")
        said = state.remote
        if said.get("phase") == "finished":
            return self.to("finishing", "the job has ended" + (f": {said.get('failed')}" if said.get("failed") else " with nothing wrong"))
        # The runner says it is alive every half minute (by its machine's clock, which may be a little off from this
        # one). One that has said nothing for a while, or never has, is asked after: a runner that is not running
        # will never say it has finished, and nothing else would end the job.
        heard = said.get("updated_at") or state.machine.get("started_at") or self.clock()
        if self.clock() - heard > QUIET:
            if self.remote().ssh(f"systemctl is-active {shlex.quote(job.unit)}", timeout=60).stdout.strip() in ("inactive", "failed"):
                return self.to("finishing", "the job's runner has stopped without saying that it had finished")
        return MIRROR

    def finishing(self) -> float:
        """The job has ended: copy until nothing is left to copy. Then the machine goes."""
        job, state = self.job, self.state
        state.machine.setdefault("ended_at", self.clock())
        hold = job.silent_hours * 3600 if job.silent_hours else None
        for _ in range(20):
            reached = self.copy_back()
            if reached == "clean":
                return self.settle("everything is copied back")
            if reached == "deaf":
                silent = self.clock() - state.unreachable
                if self.ours and silent > SILENT:
                    status = self.api.status(state.machine["id"])
                    if status is None or status in GONE:
                        return self.settle(f"the machine is gone ({status or 'Lambda no longer lists it'})",
                                           "the machine was gone before everything was copied back")
                if hold and silent > hold:
                    return self.settle(f"the machine has not answered for {job.silent_hours:g} hours: it is given up",
                                       "the machine could not be reached to copy the rest back")
                self.worry("silent", silent, f"the job has ended, and its machine has not answered for {silent / 60:.0f} minutes")
                return 60.0
            if reached == "trouble":
                lasted = self.clock() - state.machine["trouble_at"]
                if hold and lasted > hold:
                    return self.settle(f"the copy has not worked for {job.silent_hours:g} hours: taking what did come",
                                       f"not everything could be copied back ({state.trouble})")
                self.worry("trouble", lasted, f"the job has ended, and what it made cannot be copied back: {state.trouble}")
                return 60.0
        if self.clock() - state.machine["ended_at"] > CHANGING:
            return self.settle("the job's files were still changing a quarter of an hour after it ended: taking them as they are",
                               "its files were still changing when they were copied back")
        return 30.0

    def settle(self, line: str, missing: str | None = None) -> float:
        """Everything that can be copied is. What is left is to say how the job ended, and to give the machine back.
        `missing` says what did not come, when something did not: the job has failed then, whatever it said."""
        said, state = self.state.remote, self.state
        finished = said.get("phase") == "finished"
        failed = said.get("failed") if finished else "the job did not say that it had finished"
        # A job that was being stopped has not failed by being stopped. One that failed by itself before the stop
        # reached it has, and that is said (it ends `stopped` all the same: it was told to).
        own = failed if not state.stopping else failed if finished and failed != "told to stop" else None
        state.error = "; ".join(part for part in (own, missing) if part) or None
        job = self.job
        if state.error and job.keep_on_failure and self.ours and missing is None and not state.stopping:
            if job.max_hours and state.all_hours(self.clock()) > job.max_hours:
                return self.to("ending", f"{line}. {failed}. The job has had its {job.max_hours:g} hours: its machine is not kept")
            state.machine["kept_at"] = self.clock()
            until = (f", and is given back by itself after {job.keep_hours:g} hours" if job.keep_hours else "") + (
                f", or when the job has had its {job.max_hours:g} hours" if job.max_hours else "")
            self.to("kept", f"{line}. {failed}. The machine is LEFT UP to be looked at: it is billed until `stop`{until}")
            self.notify(state.note)
            return 0.0
        return self.to("ending", line + (f". {missing[0].upper()}{missing[1:]}" if missing else ""))

    def kept(self) -> float:
        """A machine left up after a failure, at the job's wish. It is billed like any other and does nothing, so
        it is given back when the job is told to stop, after `keep_hours`, when the job has had its `max_hours`,
        and when Lambda no longer has it (somebody gave it back by hand): whichever comes first."""
        job, state, machine = self.job, self.state, self.state.machine
        since = self.clock() - machine.setdefault("kept_at", self.clock())
        if job.keep_hours and since > job.keep_hours * 3600:
            return self.give_up("failed", f"the machine was kept for {job.keep_hours:g} hours to be looked at: giving it back")
        if job.max_hours and state.all_hours(self.clock()) > job.max_hours:
            return self.give_up("failed", f"the machine was kept to be looked at, and the job has had its {job.max_hours:g} hours: giving it back")
        if self.clock() - self.last_asked > 300:
            self.last_asked = self.clock()
            status = self.api.status(machine["id"])
            if status is None or status in GONE:
                return self.give_up("failed", f"the machine that was kept is {status or 'no longer listed'} at Lambda: it was given back by hand")
        return 30.0

    def keep_caches(self) -> list[str]:
        """Merge what the job's sqlite files hold into the caches kept for later jobs: a row that is already there
        stays as it is (the first reply kept for a call is the one that is recalled). What is merged is no longer
        kept twice. A cache that cannot be merged is said, and stays where it was copied to: nothing here stops
        a job from ending."""
        kept = []
        for snapshot, to in self.job.keep.items():
            source, target = self.folder / "mirror/swarm/snap" / snapshot, home() / "cache" / to
            if not source.exists():
                continue
            try:
                with locked(target.parent):                      # two jobs may end at once
                    if target.exists():
                        merge(source, target)
                    else:                                        # whole, or not there
                        shutil.copy2(source, target.with_name(target.name + ".new"))
                        os.replace(target.with_name(target.name + ".new"), target)
                source.unlink()
                kept.append(to)
            except Exception as problem:
                self.log(f"{to} could not be kept for later jobs ({type(problem).__name__}: {problem}): it is still at {source}")
        return kept

    # ---------------------------------------------------------------- giving the machine back
    def ending(self) -> float:
        """Give the machine back, if it is this job's, and do not let go of it until Lambda has said yes and no
        longer lists it as up. Then whatever else carries the job's name; then the job is over, or (a machine
        that was given up on) waits for another. An error from Lambda leaves all of this as it is, to be tried
        again: `run` sees to that."""
        machine, state, job = self.state.machine, self.state, self.job
        if self.ours:
            status = self.api.status(machine["id"])
            if status is None and self.clock() - machine.get("launched_at", 0) < LIST_LAG:
                return 15.0                                      # just launched: not being listed yet is not being gone
            if status not in ("terminated", "preempted"):
                asked = machine.get("terminate_ok_at")
                if asked is None:
                    self.api.terminate(machine["id"])            # an error unless Lambda said yes, or that it has no such machine
                    machine["terminate_ok_at"] = self.clock()
                    self.log(f"asked Lambda to terminate {machine['id']}, and it said yes")
                    return 15.0
                if status == "terminating" and self.clock() - asked < TERMINATING:
                    return 15.0
                if status not in (None, "terminating"):          # it said yes, and the machine is still up: ask again
                    if self.clock() - asked > 60:
                        del machine["terminate_ok_at"]
                    return 15.0
                if status == "terminating":
                    self.log("Lambda said yes ten minutes ago and still calls the machine terminating: `machines` shows what is up")
            hours = state.hours(self.clock())
            state.spent_cents, state.spent_hours = state.spent_cents + hours * machine.get("cents", 0), state.spent_hours + hours
            machine.update(ours=False, gone=now(), active_at=None)
            self.log(f"the machine is given back. The job has cost about ${state.dollars(self.clock()):.2f}")
        elif machine.get("ip") and not machine.get("gone") and not machine.get("said_not_ours"):
            machine["said_not_ours"] = True
            self.log(f"the machine at {machine['ip']} is not this job's to give back: it is still up, and whoever started it is billed for it")
        if not job.instance:                                     # a launch may have made a machine nobody heard of
            try:
                others = self.api.named(job.machine_name)
            except NoKey:                                        # with no key, nothing was ever launched
                others = []
            if others:
                found, kind = others[0], others[0].get("instance_type", {})
                state.machine = {"id": found["id"], "kind": kind.get("name", "?"), "region": found.get("region", {}).get("name", "?"),
                                 "cents": kind.get("price_cents_per_hour", 0), "ours": True, "user": "ubuntu",
                                 "active_at": self.clock() if found.get("status") == "active" else None}
                self.log(f"another machine carries this job's name ({found['id']}): giving it back too")
                return 5.0
            if state.unheard and self.clock() - state.unheard < UNHEARD:
                return 15.0                                      # a launch was not answered: its machine may yet show under the name
        if state.after == "waiting":                             # the machine was given up on, not the job
            state.after, state.machine, state.remote, state.unreachable, state.trouble = None, {}, {}, None, None
            (self.folder / "known_hosts").unlink(missing_ok=True)
            return self.to("waiting", f"waiting for another machine ({state.lost} of {job.relaunches} it may replace)") or POLL
        kept = self.keep_caches()                                # only now: no machine is waiting on it
        if kept:
            self.log(f"kept for later jobs: {', '.join(kept)}")
        last = state.after or ("stopped" if state.stopping else "failed" if state.error else "done")
        self.to(last, last + (f": {state.error}" if state.error and last != "done" else ""))
        self.notify(state.note)
        return 0.0

    def give_up(self, last: str, line: str) -> float:
        """End the job from wherever it is, giving back any machine that is its own."""
        self.state.after = last
        return self.to("ending", line)

    def lose(self, why: str) -> float:
        """The machine is no use (it never came up, it is gone, it cannot be reached): it is given back, and
        another is waited for, as long as the job may replace it and is not being stopped. What it copied back
        is where the next one starts from. A machine that was there before the job cannot be replaced."""
        state = self.state
        state.lost += 1
        if self.job.instance or not state.machine.get("id"):
            return self.fail(why)
        if state.stopping:
            return self.give_up("stopped", f"{why}. The job {state.stopping}: its machine is not replaced")
        if state.lost > self.job.relaunches:
            return self.fail(f"{why}. {state.lost} machines were no use: not trying another")
        state.after = "waiting"
        return self.to("ending", why)

    def fail(self, why: str) -> float:
        self.state.error, self.state.after = why, "failed"
        return self.to("ending", why)


class locked:
    """Hold a folder for the time of one thing done to what is in it (controllers share the caches that are kept)."""

    def __init__(self, folder: Path):
        self.folder = folder

    def __enter__(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        self.file = open(self.folder / ".lock", "w")
        fcntl.flock(self.file, fcntl.LOCK_EX)

    def __exit__(self, *_):
        self.file.close()


def merge(source: Path, target: Path) -> None:
    """Every row of every table of one sqlite file that the other does not have yet (by its key)."""
    into = sqlite3.connect(target, timeout=120)
    try:
        into.execute("attach database ? as other", (str(source),))
        for table, made in into.execute("select name, sql from other.sqlite_master where type = 'table'").fetchall():
            into.execute(made.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1))
            into.execute(f'insert or ignore into main."{table}" select * from other."{table}"')
        into.commit()
        into.execute("detach database other")
    finally:
        into.close()


# ---------------------------------------------------------------- one controller for each job

def alive(folder: Path) -> bool:
    """Whether a controller holds the job now."""
    with open(folder / "lock", "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        return False


def control(folder: Path) -> None:
    """Be the job's controller until the job is over. A second one for the same job stops at once. (Whoever asks
    whether a job has one holds the job for an instant to find out, so this tries for a few seconds.)"""
    lock = open(folder / "lock", "a")
    for _ in range(30):
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            time.sleep(0.1)
    else:
        return
    Controller(folder).run()


def start(folder: Path) -> bool:
    """Start a controller for a job in a process of its own, which goes on when this one ends. False if the job
    is over or has one. A job is looked after by the code it was handed in with (its `code` folder), whoever
    starts its controller and whatever this machine has been sent since: what a job's machine was sent, and where
    its files lie there, do not change under it half way."""
    if State.load(folder).phase in OVER or alive(folder):
        return False
    code = folder / "code" if (folder / "code/swarm_engine/cloud/controller.py").exists() else Path(__file__).parents[2]
    with open(folder / "controller.out", "ab") as out:
        subprocess.Popen([sys.executable, "-m", "swarm_engine.cloud", "control", folder.name], cwd=code, stdin=subprocess.DEVNULL,
                         stdout=out, stderr=subprocess.STDOUT, start_new_session=True, env={**os.environ, "PYTHONPATH": str(code)})
    return True


def take_in(name: str) -> None:
    """A job is handed in as a folder under incoming/, and is a job once all of it is there: only then does it
    get its place among the jobs, where a controller is started for whatever is found."""
    arrived, folder = home() / "incoming" / name, home() / "jobs" / name
    if arrived.is_dir() and not folder.exists():
        try:
            Job.load(arrived)                                    # it is a job, and whole
        except (OSError, ValueError, TypeError) as problem:
            sys.exit(f"the job {name} was not handed in whole ({type(problem).__name__}: {problem}): hand it in again")
        folder.parent.mkdir(parents=True, exist_ok=True)
        os.replace(arrived, folder)


def summary(folder: Path) -> dict:
    """Where a job stands, for whoever asks."""
    job, state = Job.load(folder), State.load(folder)
    machine, said, over = state.machine, state.remote, state.phase in OVER
    until = [machine["kept_at"] + job.keep_hours * 3600] if job.keep_hours and machine.get("kept_at") else []
    until += [time.time() + (job.max_hours - state.all_hours()) * 3600] if job.max_hours else []
    return {"job": job.name, "phase": state.phase, "controller": "not needed" if over else "at work" if alive(folder) else "NOT RUNNING",
            "kept_until": (min(until) if until else 0) if state.phase == "kept" else None,     # 0: until it is told to stop
            "machine": {k: machine.get(k) for k in ("kind", "region", "ip", "id") if machine.get(k)},
            "billing": bool(machine.get("ours") and machine.get("active_at")), "hours": round(state.all_hours(), 2),
            "dollars": round(state.dollars(), 2), "began": state.began, "copied_back": state.mirrored, "stopping": state.stopping,
            "unreachable_minutes": round((time.time() - state.unreachable) / 60) if state.unreachable else None, "trouble": state.trouble,
            "says": {k: said.get(k) for k in ("phase", "step", "steps", "command", "attempt", "failed", "updated") if said.get(k) is not None},
            "note": state.note.splitlines()[0] if state.note else "", "error": state.error, "commands": job.commands, "lost": state.lost}


def told(found: dict) -> str:
    machine = found["machine"]
    where = (machine.get("kind", "none yet") + (f" in {machine['region']}" if machine.get("region") else "")
             + (f" at {machine['ip']}" if machine.get("ip") else ""))
    lines = [f"{found['job']}: {found['phase']}" + (f" ({found['controller']})" if found["controller"] != "not needed" else ""),
             f"  machine     {where}" + ("; it is being billed" if found["billing"] else ""),
             f"  cost        about ${found['dollars']:.2f} for {found['hours']:.1f} hours", f"  last        {found['note']}"]
    if found["says"]:
        said = found["says"]
        step = f", command {said['step']} of {said.get('steps')}" if said.get("step") else ""
        lines.append(f"  the job     {said.get('phase')}{step}" + (f", try {said['attempt']}" if (said.get("attempt") or 1) > 1 else "")
                     + (f": {said['command'][:100]}" if said.get("command") else "") + f" (it said so at {said.get('updated')})")
    if found["copied_back"]:
        lines.append(f"  copied back {found['copied_back']}")
    if found["unreachable_minutes"]:
        lines.append(f"  THE MACHINE HAS NOT ANSWERED FOR {found['unreachable_minutes']} MINUTES")
    if found["trouble"]:
        lines.append(f"  THE COPY DOES NOT WORK: {found['trouble']}")
    if found["error"]:
        lines.append(f"  error       {found['error']}")
    if found.get("kept_until") is not None:
        lines.append("  THE MACHINE IS KEPT TO BE LOOKED AT, AND BILLED: " + (
            f"it is given back by itself at {time.strftime('%H:%M on %Y-%m-%d', time.localtime(found['kept_until']))}, or at `stop`"
            if found["kept_until"] else "until `stop`, however long that is"))
    if found["controller"] == "NOT RUNNING":
        lines.append("  NOTHING IS LOOKING AFTER THIS JOB: python3 -m swarm_engine.cloud tick")
    return "\n".join(lines)


def strays(listed: list[dict] | None = None) -> list[str]:
    """Machines that carry this controller's name and that no job here will see to: a line for each. A job that is
    not over sees to whatever carries its own name. Empty when there is none, and when Lambda cannot be asked."""
    try:
        listed = Lambda(api_key()).instances() if listed is None else listed
    except (NoKey, Refused, ConnectionError, OSError, ValueError):
        return []
    ids, names = set(), set()
    for each in jobs():
        try:
            state = State.load(each)
            ids.add(state.machine.get("id"))
            if state.phase not in OVER:
                names.add(Job.load(each).machine_name)
        except Exception:
            pass
    return [f"{m.get('id')} {m.get('name')} ({m.get('status')}, {m.get('instance_type', {}).get('name', '?')})" for m in listed
            if str(m.get("name", "")).startswith(f"swarm-{ident()}-") and m.get("status") not in GONE
            and m.get("id") not in ids and m.get("name") not in names]


CRON = "*/2 * * * * cd {bin} && {python} -m swarm_engine.cloud tick >> {home}/tick.log 2>&1   # swarm_cloud"


def setup(args) -> None:
    """An ssh key for the rented machines, registered with Lambda, and a crontab line that looks after jobs."""
    base = home()
    for folder in ("jobs", "cache", "incoming"):
        (base / folder).mkdir(parents=True, exist_ok=True)
    base.chmod(0o700)
    if not (base / "key").exists():
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", args.key_name, "-f", str(base / "key")], check=True)
        print(f"made an ssh key at {base / 'key'}")
    (base / "key_name").write_text(args.key_name + "\n")
    print(f"the machines this controller rents are called swarm-{ident()}-<job>")
    stored = base / "lambda_api_key"
    if os.environ.get("LAMBDA_API_KEY") and not stored.exists():
        stored.touch(mode=0o600)
        stored.write_text(os.environ["LAMBDA_API_KEY"].strip() + "\n")
        print(f"kept the API key at {stored} (readable by you alone)")
    if stored.exists():
        stored.chmod(0o600)
        try:
            key = api_key()
        except NoKey as problem:
            sys.exit(str(problem))
        Lambda(key).add_ssh_key(args.key_name, (base / "key.pub").read_text())
        print(f"Lambda has the ssh key as {args.key_name}")
    else:
        print(f"no API key yet: put it in {stored} (chmod 600) and run this again, to register the ssh key with Lambda")
    if not args.no_cron:
        line = CRON.format(bin=Path(__file__).parents[2], python=sys.executable, home=base)
        have = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
        if "# swarm_cloud" not in have:
            subprocess.run(["crontab", "-"], input=have.rstrip("\n") + ("\n" if have.strip() else "") + line + "\n", text=True, check=True)
            print("added a crontab line that starts a controller for any job that has lost its own")


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(prog="python3 -m swarm_engine.cloud", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("launch", "control"):
        commands.add_parser(name).add_argument("job")
    status = commands.add_parser("status")
    status.add_argument("job", nargs="?")
    status.add_argument("--json", action="store_true")
    logs = commands.add_parser("logs")
    logs.add_argument("job")
    logs.add_argument("-n", type=int, default=40)
    stop = commands.add_parser("stop")
    stop.add_argument("job")
    stop.add_argument("--now", action="store_true", help="give the machine back without copying anything more")
    commands.add_parser("tick")
    commands.add_parser("machines")
    made = commands.add_parser("setup")
    made.add_argument("--key-name", default=f"swarm-{os.uname().nodename.split('.')[0].lower()}"[:60])
    made.add_argument("--no-cron", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "launch":
        take_in(args.job)
    folder = home() / "jobs" / args.job if getattr(args, "job", None) else None
    if folder is not None and not (folder / "job.json").exists():
        sys.exit(f"no job {args.job} at {folder}")
    if args.command == "setup":
        setup(args)
    elif args.command == "control":
        control(folder)
    elif args.command == "launch":
        phase = State.load(folder).phase
        print(f"{args.job}: a controller is started" if start(folder) else
              f"{args.job} is over ({phase})" if phase in OVER else f"{args.job}: {phase}, and it has a controller")
    elif args.command == "tick":
        for each in jobs():
            try:                                                 # one job that cannot be read does not leave the others alone
                if start(each):
                    print(f"{now()}  started a controller for {each.name}")
            except Exception as problem:
                print(f"{now()}  {each.name} COULD NOT BE LOOKED AFTER ({type(problem).__name__}: {problem})")
        for stray in strays():
            print(f"{now()}  A MACHINE IS UP THAT NO JOB HERE WILL GIVE BACK: {stray}")
    elif args.command == "status":
        found = []
        for each in ([folder] if folder else jobs()):
            try:
                found.append(summary(each))
            except Exception as problem:
                found.append({"job": each.name, "phase": "unreadable", "error": f"{type(problem).__name__}: {problem}"})
        if args.json:
            print(json.dumps(found, indent=2))
        else:
            print("\n\n".join(told(each) if "machine" in each else f"{each['job']}: WHERE IT STANDS CANNOT BE READ ({each['error']})"
                              for each in found) or "no jobs")
            for stray in ([] if folder else strays()):
                print(f"\nA MACHINE IS UP THAT NO JOB HERE WILL GIVE BACK: {stray}\n  it is billed until it is terminated in Lambda's console")
    elif args.command == "logs":
        for name, title in (("controller.log", "the controller"), ("mirror/swarm/logs/setup.log", "setting the machine up"),
                            ("mirror/swarm/logs/job.log", "the job")):
            path = folder / name
            if path.exists():
                print(f"---- {title} ({name})\n" + "\n".join(path.read_text(errors="replace").splitlines()[-args.n:]))
    elif args.command == "stop":
        (folder / "stop").write_text("now\n" if args.now else "\n")
        start(folder)
        print(f"{args.job} is told to stop" + (" now" if args.now else ": what it has made is copied back first")
              + ". `status` says when its machine is gone")
    elif args.command == "machines":
        known, taking, using = {}, {}, {}                        # by a machine's id, by its name, by its address
        for each in jobs():
            try:
                state = State.load(each)
                if state.machine.get("id"):
                    known[state.machine["id"]] = each.name
                if state.phase not in OVER:                      # a launch that was not answered yet is its job's by its name
                    job = Job.load(each)
                    taking[job.machine_name] = each.name
                    if job.instance and state.machine.get("ip"):
                        using[state.machine["ip"]] = each.name
            except Exception:
                pass
        try:
            listed = Lambda(api_key()).instances()
        except NoKey as problem:
            sys.exit(str(problem))
        # An account may be shared: a machine that does not carry this controller's name is somebody else's, and
        # is said as that. Only one that carries it, and that no job here knows or is taking up, is shouted.
        mine = f"swarm-{ident()}-"
        for machine in listed:
            kind, region, name = machine.get("instance_type") or {}, machine.get("region") or {}, str(machine.get("name") or "")
            if machine.get("id") in known:
                whose = f"job {known[machine['id']]}"
            elif name in taking:
                whose = f"job {taking[name]}, which is taking it up"
            elif not name.startswith(mine):
                whose = "not this controller's" + (f": job {using[machine['ip']]} is run on it" if machine.get("ip") in using else "")
            else:
                whose = "this controller's, and gone" if machine.get("status") in GONE else "THIS CONTROLLER'S NAME, AND NO JOB HERE KNOWS IT"
            print(f"{machine.get('id') or '?'}  {machine.get('status') or '?':12} {kind.get('name') or '?':22} "
                  f"${(kind.get('price_cents_per_hour') or 0) / 100:.2f}/h  {region.get('name') or '?':14} {machine.get('ip') or '-':16} "
                  f"{name or '-'}  ({whose})")


if __name__ == "__main__":
    main()
