"""What a job is, and where it stands. A job is a folder on the controller's machine:

    ~/swarm_cloud/jobs/<name>/
        job.json          what to rent, what to send, what to run and what to bring back (`Job`): written once
        state.json        where it stands (`State`): the controller's, rewritten at every step
        controller.log    what the controller did, a line at a time
        payload/          what is sent to the machine: repos/<name>.bundle, and files/ (laid over ~/work there)
        mirror/           what came back: swarm/ (how far the job is, its logs, snapshots of its caches) and
                          work/ (the files under the job's `mirror` paths that it made or changed)
        code/             this code as it was when the job was handed in, if it was sent along: the job's own
                          controller runs from there, so that newer code does not change a job under way
        stop              is there once the job has been told to stop

and beside the jobs:

    ~/swarm_cloud/key, key.pub        the ssh key the rented machines accept (registered with Lambda by `setup`)
    ~/swarm_cloud/lambda_api_key      the API key, readable by its owner alone
    ~/swarm_cloud/id                  a few letters that are this controller's own: they go into the name of every
                                      machine it rents, so that it never takes another controller's machine for its own
    ~/swarm_cloud/cache/              what jobs keep for the jobs after them (their reply caches, merged)
    ~/swarm_cloud/incoming/           a job's folder while it is being handed in: it becomes a job when it is whole
    ~/swarm_cloud/notify              if there is such a program, it is run with a job's name, how it ended and a line
                                      about it, whenever a job ends or needs somebody
    ~/swarm_cloud/bin/                this code, as it was last sent here

On the rented machine a job has a folder of its own, ~/jobs/<name>/, with swarm/ (what the controller sent and
what the runner writes) and work/ (the repos and files), so that a machine that is used for one job after another
starts each from nothing of the last.

SWARM_CLOUD_HOME moves all of it (tests do).
"""
from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import time
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

PHASES = ("waiting", "booting", "connecting", "sending", "running", "finishing", "ending", "kept", "done", "failed", "stopped")
OVER = ("done", "failed", "stopped")            # nothing more will be done for the job
IMAGE = "gpu-base-24-04"                        # Ubuntu 24.04 with the NVIDIA driver and nothing else (Lambda's "GPU Base 24.04")
# a public ssh key as one line of ~/.ssh/authorized_keys: its kind, the key, and a few words about it
PUBLIC_KEY = r"(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(256|384|521)|sk-(ssh-ed25519|ecdsa-sha2-nistp256)@openssh\.com) [A-Za-z0-9+/=]+( [^\r\n]*)?"


def home() -> Path:
    return Path(os.environ.get("SWARM_CLOUD_HOME") or "~/swarm_cloud").expanduser()


def key_in(text: str) -> str:
    """The API key a text holds: the key alone on a line, or what a line `LAMBDA_API_KEY=...` gives it as (a .env
    file; the last such line, as a shell that read the file would have it). Lines that begin with # are notes. A
    key is one word of plain characters. What holds no such key raises ValueError, which quotes none of it: a
    key is never to be read out of an error."""
    lines = [line.strip() for line in text.lstrip("\ufeff").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    found = None
    for line in lines:
        named = re.fullmatch(r"(?:export\s+)?LAMBDA_API_KEY\s*=\s*(.*)", line)
        if named:
            value = named[1].strip()
            found = value[1:].split(value[0])[0] if value[:1] in ("'", '"') else (value.split() or [""])[0]
    if found is None and len(lines) == 1 and re.fullmatch(r"[A-Za-z0-9_.+/-]+", lines[0]):
        found = lines[0]
    if not found or not re.fullmatch(r"[\x21-\x7e]+", found) or found.startswith("$"):
        raise ValueError("no API key in it: a key is alone on a line, or given by a line LAMBDA_API_KEY=<the key>")
    return found


def now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def ident() -> str:
    """This controller's own few letters (made once, kept in its folder)."""
    kept = home() / "id"
    if not kept.exists() or not re.fullmatch(r"[0-9a-z]{3,12}", kept.read_text().strip()):
        if kept.exists() and kept.read_text().strip():          # letters that are in machines' names are not thrown away
            raise ValueError(f"{kept} does not hold this controller's letters (a few of 0-9 and a-z)")
        kept.parent.mkdir(parents=True, exist_ok=True)
        kept.write_text(secrets.token_hex(3) + "\n")
    return kept.read_text().strip()


@dataclass
class Job:
    name: str                                   # lower case letters, digits and dashes: its folder, and its machine's name
    kinds: list[str]                            # the kinds of machine that will do, the one wanted most first
    commands: list[str]                         # the job: shell commands, in order; it stops at the first that fails
    workdir: str = ""                           # where they run, under ~/work on the machine (a repo's folder)
    setup: list[str] = field(default_factory=list)       # run once before them, in order, each from `workdir`
    services: list[dict] = field(default_factory=list)   # started before the commands and stopped after: {"name", "command",
                                                # "ready": a URL that answers once it is up, "timeout": seconds to wait for it}
    env: dict = field(default_factory=dict)     # for the commands and the services
    mirror: list[str] = field(default_factory=list)      # folders under ~/work: files in them that the job made or changed
                                                # are copied back every minute, and when it ends
    snapshots: list[str] = field(default_factory=list)   # sqlite files under ~/work, copied back whole and consistent
    seeds: dict = field(default_factory=dict)   # {a path under ~/work: a path under the controller's cache/}: laid there
                                                # before the job starts, if the controller has it
    keep: dict = field(default_factory=dict)    # {one of `snapshots`: a path under the controller's cache/}: merged into it
                                                # when the job has ended, for the jobs after this one
    regions: list[str] | None = None            # only these regions (None: wherever one is free)
    image: str = IMAGE
    instance: dict | None = None                # a machine that is already there: {"ip", "user", "id", "key": the ssh key it
                                                # accepts, if not the controller's}. It is not launched, and is given back
                                                # only if it has an "id" and says "terminate": true
    retries: int = 2                            # how often a command that failed is run again (after its services are restarted)
    relaunches: int = 2                         # how often a machine that was lost is replaced, the job carrying on from its caches
    max_hours: float | None = None              # stop the job and give the machine back after this long on rented machines, all
                                                # of them together (None: no limit)
    silent_hours: float | None = 6.0            # a machine that has not answered for this long is given up, whatever Lambda says
                                                # of it, and replaced (None: it is held for as long as it does not answer)
    keep_on_failure: bool = False               # leave the machine up when the job fails, to be looked at: it bills until
                                                # `stop`, and is given back by itself after `keep_hours`, or when the job
                                                # has had its `max_hours` if that comes first
    keep_hours: float | None = 3.0              # how long a machine is kept after a failure, looked at or not (None: until
                                                # `stop`, or the job's `max_hours`). A kept machine is billed and does nothing
    keys: list[str] = field(default_factory=list)        # public ssh keys of whoever handed the job in: the machine accepts
                                                # them too, so that they can get into it (`ssh ubuntu@<its address>`)

    def __post_init__(self):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", self.name):
            raise ValueError(f"a job's name is lower case letters, digits and dashes, at most 41 of them: {self.name!r}")
        if not self.commands:
            raise ValueError("a job needs something to run")
        if not self.kinds and not self.instance:
            raise ValueError("a job needs a kind of machine to rent, or a machine that is already there")
        if not isinstance(self.keys, list):
            raise ValueError("a job's `keys` are a list of public ssh keys")
        for key in self.keys:
            if not isinstance(key, str) or not re.fullmatch(PUBLIC_KEY, key):
                raise ValueError("a job's `keys` are public ssh keys, each as the one line of its .pub file")
        for name in ("max_hours", "keep_hours", "silent_hours"):               # none, or a time: 0 is neither, and was
            hours = getattr(self, name)                                        # read as "no limit" where it was meant as one
            if hours is not None and (isinstance(hours, bool) or not isinstance(hours, (int, float)) or not hours > 0):
                raise ValueError(f"a job's `{name}` is a number of hours above 0, or not given: {hours!r}")
        for path in [*self.mirror, *self.snapshots, *self.seeds, *self.seeds.values(), *self.keep, *self.keep.values(), self.workdir]:
            if not isinstance(path, str) or path.startswith(("/", "~")) or ".." in Path(path).parts:
                raise ValueError(f"paths are given from the job's work folder, or from the controller's cache: {path!r}")

    @property
    def machine_name(self) -> str:
        """What this job's machine is called at Lambda: this controller's letters and the job's name. A machine
        with this name is this job's, and no other controller's."""
        return f"swarm-{ident()}-{self.name}"

    @property
    def unit(self) -> str:
        """The job's unit under systemd on the machine."""
        return f"swarm-job-{self.name}"

    @property
    def root(self) -> str:
        """The job's folder on the machine, from its home folder."""
        return f"jobs/{self.name}"

    def save(self, folder: Path) -> None:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "job.json").write_text(json.dumps(asdict(self), indent=2) + "\n")

    @classmethod
    def load(cls, folder: Path) -> "Job":
        saved = json.loads((folder / "job.json").read_text())
        return cls(**{f.name: saved[f.name] for f in fields(cls) if f.name in saved})


@dataclass
class State:
    phase: str = "waiting"
    machine: dict = field(default_factory=dict)          # id, ip, user, kind, region, cents (an hour), launched, active, ours
    began: str = field(default_factory=now)     # when the job was handed in
    polls: int = 0                              # how often it has asked whether a machine is free
    lost: int = 0                               # machines that were lost and replaced
    mirrored: str | None = None                 # when results were last copied back
    unreachable: float | None = None            # since when (seconds) the machine has not answered, if it does not
    remote: dict = field(default_factory=dict)  # what the machine last said of the job (its status.json)
    spent_cents: float = 0.0                    # of machines that are gone: what they cost
    spent_hours: float = 0.0                    # of machines that are gone: how long they were billed
    refusals: int = 0                           # how often in a row Lambda has said no to something
    unheard: float | None = None                # when a launch was sent and not answered: the machine may be there all the same
    trouble: str | None = None                  # why the last copy did not work, when the machine did answer
    error: str | None = None                    # why it failed, if it did
    stopping: str | None = None                 # why the job was told to stop, once it has been
    stop_sent: bool = False                     # and whether the machine has taken that
    after: str | None = None                    # what follows once the machine is given back: "waiting" (for another), or
                                                # how the job ends; None: as the job itself ended
    note: str = ""                              # the last thing worth telling whoever asks

    def save(self, folder: Path) -> None:
        """Written whole to a new file, which is on the disk before it takes the old one's place; the one before
        is kept beside it. Where a job stands is the only record of which machine is its own."""
        path, temporary = folder / "state.json", folder / "state.json.new"
        with open(temporary, "w") as f:
            f.write(json.dumps(asdict(self), indent=2) + "\n")
            f.flush()
            os.fsync(f.fileno())
        if path.exists():
            shutil.copy2(path, folder / "state.json.before")
        os.replace(temporary, path)

    @classmethod
    def load(cls, folder: Path) -> "State":
        """Where a job stands; a job that has not begun stands at the beginning. A file that cannot be read (the
        machine went down as it was written) gives way to the one before it."""
        if not (folder / "state.json").exists() and not (folder / "state.json.before").exists():
            return cls()
        for name in ("state.json", "state.json.before"):
            try:
                saved = json.loads((folder / name).read_text())
                return cls(**{f.name: saved[f.name] for f in fields(cls) if f.name in saved})
            except (OSError, ValueError, TypeError):
                continue
        raise ValueError(f"where the job at {folder} stands cannot be read (state.json and the one before it)")

    def hours(self, at: float | None = None) -> float:
        """How long the machine it has now has been billed for: from when it was first up."""
        since = self.machine.get("active_at")
        return max(((at or time.time()) - since) / 3600, 0.0) if since else 0.0

    def all_hours(self, at: float | None = None) -> float:
        """How long the job has been billed for, machines that are gone included."""
        return self.spent_hours + self.hours(at)

    def dollars(self, at: float | None = None) -> float:
        """What the job has cost so far, machines that are gone included."""
        return (self.spent_cents + self.hours(at) * self.machine.get("cents", 0)) / 100


def jobs() -> list[Path]:
    """Every job's folder, the newest first."""
    folder = home() / "jobs"
    found = [p.parent for p in folder.glob("*/job.json")] if folder.is_dir() else []
    return sorted(found, key=lambda p: (p / "job.json").stat().st_mtime, reverse=True)
