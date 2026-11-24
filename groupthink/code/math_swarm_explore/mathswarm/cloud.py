"""`lab cloud`: a run of this lab on a rented GPU, from handing it in to having its run folder back here.

    lab cloud setup --controller myserver             once: where jobs are looked after (an ssh host that is always on)
    lab cloud run "lab run every_step --name gpu_main --agents 20" --gpu h100 a100
    lab cloud status                                  where every job stands, and what it has cost
    lab cloud logs <job>                              the end of what it has printed
    lab cloud pull <job>                              its run folders into experiments/, and the standings written again
    lab cloud stop <job>                              copy back what there is, give the machine back
    lab cloud check --gpu a10 --model 4B-bf16         a first job on a kind of GPU: is the machine ready, does the engine
                                                      hold against its server, how fast is it

What rents the machine, looks after the job and gives the machine back is ../swarm_engine/swarm_engine/cloud, and
it does so from the controller's machine: once `lab cloud run` has handed a job over, this laptop can be closed.
This file only says what a job of this lab is:

    what is sent        this repo and ../swarm_engine, each as the commit it stands at (so commit first: a run's
                        config.json keeps the commit it was made at), the benchmark's problems, and the run folder
                        the command names, if there is one here, so that a run can be carried on there
    how it is set up    bubblewrap for agents' Python and the setting Ubuntu 24.04 needs for it, uv, this lab's
                        environment from its lock file, vLLM in an environment of its own, the model, `lab doctor`
    what runs beside    a vLLM server for the model, started once for all the job's commands
    what comes back     the files the job made or changed under experiments/ (and ../swarm_engine/results), every
                        minute while it runs; and its caches of replies and of file runs, which the controller's
                        machine keeps and gives to the next job, so that a later run recalls what an earlier one drew

`--model` is the model the job's `lab run` commands are given when they name none: on a GPU that is "9B-bf16", the
weights as Qwen released them, not "9B", the Mac's 4-bit build. They are two models, and the standings keep them
apart.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .current import GPU_MODEL
from .paths import BENCHMARKS, EXPERIMENTS, ROOT

SETTINGS = Path("~/.swarm/cloud.json").expanduser()      # on this machine: {"controller": "myserver", "gpu": ["h100", "a100"]}
HOME = "swarm_cloud"                                     # the controller's folder, in its home folder on its machine
REPO, ENGINE = "math_swarm_explore", "swarm_engine"      # what the two repos are called on the rented machine
GPUS = {"a10": ["gpu_1x_a10"], "a100": ["gpu_1x_a100_sxm4", "gpu_1x_a100"], "h100": ["gpu_1x_h100_pcie", "gpu_1x_h100_sxm5"]}
PORT = 8000
CACHES = ("replies.sqlite", "python.sqlite")
UV = "0.11.32"                                           # the uv this repo's lock file was written by


def settings() -> dict:
    return json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}


def key_in(text: str) -> str:
    """The Lambda API key a file holds: the key alone on a line, or what a line `LAMBDA_API_KEY=...` gives it as
    (a .env file). The launcher's own reader of one (`swarm_engine.cloud.job.key_in`), so that what is taken here
    is what would be taken there. Nothing of the file is ever printed, whatever is wrong with it."""
    from swarm_engine.cloud.job import key_in as taken
    try:
        return taken(text)
    except ValueError:
        raise SystemExit("that file does not hold a Lambda API key: it is the key alone on a line, or a line LAMBDA_API_KEY=<the key>") from None


IDENTITIES = ("id_ed25519", "id_ecdsa", "id_rsa", "id_ed25519_sk", "id_ecdsa_sk")       # the keys ssh offers as this machine's own


def public_keys(folder: Path | None = None) -> list[str]:
    """This machine's own public ssh keys: those ssh itself offers from ~/.ssh (id_ed25519.pub and its like), and
    no other .pub that lies there (a colleague's, a deploy key's). A job carries them, and its rented machine
    accepts them: whoever hands a job in can get into its machine to look."""
    from swarm_engine.cloud.job import PUBLIC_KEY
    found = []
    for name in IDENTITIES:
        try:
            line = ((folder or Path("~/.ssh").expanduser()) / f"{name}.pub").read_text().strip()
        except (OSError, ValueError):                           # not there, or not text
            continue
        if re.fullmatch(PUBLIC_KEY, line) and line not in found:
            found.append(line)
    return found


class Where:
    """The controller's machine: this one ("here"), or an ssh host."""

    def __init__(self, host: str | None = None):
        self.host = host or settings().get("controller")
        if not self.host:
            raise SystemExit("where are jobs looked after? Say it once: lab cloud setup --controller <an ssh host that is always on, or `here`>")
        self.here = self.host == "here"

    @property
    def home(self) -> str:
        """Its folder, as rsync and a shell there take it."""
        if self.here:
            from swarm_engine.cloud.job import home
            return str(home())
        return HOME

    def shell(self, command: str, capture: bool = True) -> subprocess.CompletedProcess:
        argv = ["bash", "-c", command] if self.here else ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", self.host, command]
        return subprocess.run(argv, capture_output=capture, text=True)

    def cloud(self, *args: str, capture: bool = False) -> subprocess.CompletedProcess:
        """`python3 -m swarm_engine.cloud ...` there."""
        if self.here:
            return subprocess.run([sys.executable, "-m", "swarm_engine.cloud", *args], capture_output=capture, text=True)
        return self.shell(f"cd {HOME}/bin && python3 -m swarm_engine.cloud {shlex.join(args)}", capture=capture)

    def put(self, local: Path, to: str, fresh: bool = False) -> None:
        """Lay a folder here over a folder under its home. `fresh`: in the place of whatever is there."""
        target = f"{self.home}/{to}/" if self.here else f"{self.host}:{HOME}/{to}/"
        there = shlex.quote(f"{self.home}/{to}")
        made = self.shell((f"rm -rf {there} && " if fresh else "") + f"mkdir -p {there}")
        if made.returncode:
            raise SystemExit(f"could not make {target}: {made.stderr.strip()[-300:]}")
        done = subprocess.run(["rsync", "-az", f"{local}/", target], capture_output=True, text=True)
        if done.returncode:
            raise SystemExit(f"could not copy to {target}: {done.stderr.strip()[-300:]}")

    def get(self, of: str, local: Path) -> bool:
        """Copy a folder under its home to a folder here: its files and folders, and no links (what a job copied
        back is not trusted to point anywhere on this machine), nor what a copy that was cut short left aside.
        False if there is no such folder there."""
        source = f"{self.home}/{of}/" if self.here else f"{self.host}:{HOME}/{of}/"
        local.mkdir(parents=True, exist_ok=True)
        return subprocess.run(["rsync", "-rptz", "--exclude=.rsync-partial", "--exclude=__pycache__", source, f"{local}/"],
                              capture_output=True, text=True).returncode == 0

    def send_code(self) -> None:
        """The controller's code, as this repo's engine has it now: what answers `status` there and starts
        controllers. (A job is looked after by the copy it is handed in with: `code_into`.)"""
        if self.here:
            return
        with tempfile.TemporaryDirectory() as folder:
            code_into(Path(folder))
            self.put(Path(folder), "bin")


def code_into(folder: Path) -> None:
    """The controller's code as this repo's engine has it now, laid into a folder. It needs nothing but Python:
    the few files of the engine that load without a model library, and its `cloud` folder."""
    import swarm_engine
    package, staged = Path(swarm_engine.__file__).parent, folder / "swarm_engine"
    staged.mkdir(parents=True)
    for name in ("__init__.py", "machine.py", "models.py", "settings.py"):
        shutil.copy2(package / name, staged / name)
    shutil.copytree(package / "cloud", staged / "cloud", ignore=shutil.ignore_patterns("__pycache__"))


# ---------------------------------------------------------------- what a job of this lab is

def kinds(gpus: list[str]) -> list[str]:
    """Lambda's names for the machines wanted, the one wanted most first: "h100", "a100", "a10", or its own names."""
    out: list[str] = []
    for gpu in gpus:
        out += [kind for kind in GPUS.get(gpu.lower(), [gpu]) if kind not in out]
    return out


def commit_of(repo: Path, allow_dirty: bool) -> str:
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()
    changed = git("status", "--porcelain")
    if changed and not allow_dirty:
        raise SystemExit(f"{repo} has changes that are not committed, and a job is sent as a commit:\n{changed[:600]}\n"
                         "Commit them, or say --allow-dirty to send the last commit as it is.")
    return git("rev-parse", "HEAD")


def parts(command: str) -> list[list[str]]:
    """A command as a shell would read it: the words of each of the commands it is made of (`a && b`, `a; b`,
    `a | b` are two). One this cannot read (a quote left open) is one command of no words."""
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        words = list(lexer)
    except ValueError:
        return [[]]
    out: list[list[str]] = [[]]
    for word in words:
        if word and set(word) <= set("();<>|&"):                # what stands between two commands, or sends one's output somewhere
            out.append([])
        else:
            out[-1].append(word)
    return [part for part in out if part] or [[]]


def lab_run(words: list[str]) -> int | None:
    """Where `lab run` stands among the words of a command, if it is one."""
    return next((n for n, word in enumerate(words) if word == "lab" and words[n + 1:n + 2] == ["run"]), None)


def option(words: list[str], name: str) -> str | None:
    """What a command gives an option as, written `--name value` or `--name=value`; the last, as the lab reads them."""
    found = None
    for n, word in enumerate(words):
        if word == name and n + 1 < len(words):
            found = words[n + 1]
        elif word.startswith(name + "="):
            found = word.split("=", 1)[1]
    return found


def with_model(command: str, model: str) -> str:
    """A `lab run` command, given the job's model if it names none. Any other command is left as it is. A command
    made of several, with a `lab run` among them that names no model, is refused: where the model would go in it
    is not this code's to guess, and on a GPU a run that names none is the Mac's model, which does not run there."""
    made_of = parts(command)
    bare = [words for words in made_of if lab_run(words) is not None and option(words, "--model") is None and "--dry-run" not in words]
    if not bare:
        return command
    if len(made_of) > 1:
        raise SystemExit(f"this command is several, and a `lab run` among them names no model:\n    {command}\n"
                         f"Give each `lab run` as a command of its own (the job runs them in order), or its own --model {model}.")
    return f"{command} --model {shlex.quote(model)}"


def runs_named(commands: list[str]) -> list[tuple[str, str]]:
    """The (experiment, run) each `lab run` of a job names."""
    out = []
    for command in commands:
        for words in parts(command):
            at = lab_run(words)
            if at is not None and len(words) > at + 2 and not words[at + 2].startswith("-"):
                out.append((words[at + 2], option(words, "--name") or "main"))
    return out


def setup_commands(model: str) -> list[str]:
    """What makes a fresh Ubuntu 24.04 with a GPU ready for a run, each step from this repo's folder there."""
    apt = "sudo DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=900 -q"
    return [
        # a machine that has just come up may still be busy with its own packages, and a mirror may hiccup: three tries
        f"for n in 1 2 3; do {apt} update && {apt} install -y bubblewrap rsync git curl && exit 0; sleep 30; done; exit 1",
        # Ubuntu 24.04 keeps bubblewrap from making the sandbox agents' Python runs in until this is set (mathswarm/linux.py);
        # it is written down as well, so that a machine that restarts comes up with it
        "if [ -e /proc/sys/kernel/apparmor_restrict_unprivileged_userns ]; then "
        "echo 'kernel.apparmor_restrict_unprivileged_userns = 0' | sudo tee /etc/sysctl.d/60-swarm-userns.conf >/dev/null && "
        "sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0; fi",
        f"command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/{UV}/install.sh | sh",
        # the Python of .python-version, as uv provides it: the one this Mac runs, and the only thing of it a file's sandbox is shown
        "uv sync --locked --managed-python",
        "uv run swarm-vllm install",
        "uv run python -c \"import sys; from swarm_engine.vllm_server import resolve; print(resolve(sys.argv[1])[0])\" "
        + shlex.quote(model),                                    # the model's files
        "uv run lab doctor",
    ]


def build(commands: list[str], name: str, gpus: list[str], model: str, folder: Path, allow_dirty: bool = False, **more) -> dict:
    """Write a job's folder: job.json, and payload/ with the two repos and the files the run needs. Returns the job."""
    import swarm_engine
    from swarm_engine.cloud.job import Job
    engine = Path(swarm_engine.__file__).resolve().parents[1]
    commands = [with_model(command, model) for command in commands]
    caches = {f"{REPO}/data/cache/{cache}": f"{REPO}/{cache}" for cache in CACHES}
    job = Job(name=name, kinds=kinds(gpus) if not more.get("instance") else [], commands=commands, workdir=REPO,
              setup=setup_commands(model),
              services=[{"name": "vllm", "command": f"exec uv run swarm-vllm serve --model {shlex.quote(model)} --port {PORT}",
                         "ready": f"http://127.0.0.1:{PORT}/health", "timeout": 1800}],
              env={"SWARM_VLLM_URL": f"http://127.0.0.1:{PORT}", "HF_HUB_DISABLE_TELEMETRY": "1", "UV_MANAGED_PYTHON": "1"},
              mirror=[f"{REPO}/experiments", f"{ENGINE}/results"], snapshots=list(caches), seeds=caches, keep=caches,
              **{key: value for key, value in more.items() if value is not None})
    job.save(folder)
    repos = folder / "payload/repos"
    repos.mkdir(parents=True)
    for called, repo in ((REPO, ROOT), (ENGINE, engine)):
        (repos / f"{called}.commit").write_text(commit_of(repo, allow_dirty) + "\n")
        subprocess.run(["git", "-C", str(repo), "bundle", "create", str(repos / f"{called}.bundle"), "HEAD"], capture_output=True, check=True)
    files = folder / "payload/files" / REPO
    problems = BENCHMARKS / "problems"
    if not problems.is_dir():
        raise SystemExit("the benchmarks are not built here, and the run needs them there: uv run lab data")
    shutil.copytree(problems, files / "data/benchmarks/problems")
    shutil.copy2(BENCHMARKS / "splits.json", files / "data/benchmarks/splits.json")
    for experiment, run in runs_named(commands):                 # a run that is here already is carried on there
        here = EXPERIMENTS / experiment / "runs" / run
        if (here / "config.json").exists():
            shutil.copytree(here, files / "experiments" / experiment / "runs" / run)
    return json.loads((folder / "job.json").read_text())


# ---------------------------------------------------------------- the commands

def cmd_setup(args):
    # the key is read first: a file that does not hold one changes nothing, here or there
    key = key_in(Path(args.api_key_file).expanduser().read_text(encoding="utf-8-sig", errors="replace")) if args.api_key_file else None
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    kept = settings() | {"controller": args.controller} | ({"gpu": args.gpu} if args.gpu else {})
    SETTINGS.write_text(json.dumps(kept, indent=2) + "\n")
    where = Where(args.controller)
    where.send_code()
    if key:                                                      # the key goes as a file over ssh, and is never on a command line
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "lambda_api_key").touch(mode=0o600)
            (Path(folder) / "lambda_api_key").write_text(key + "\n")
            where.put(Path(folder), ".")
        where.shell(f"chmod 700 {HOME} && chmod 600 {HOME}/lambda_api_key" if not where.here else "true")
    done = where.cloud("setup", *(["--no-cron"] if where.here else []))
    print(f"jobs are looked after on {args.controller} ({SETTINGS} says so)")
    if done.returncode:
        sys.exit(done.returncode)


PART = r"-(\d+)of(\d+)"        # how the jobs of a run that was shared out over machines end: <name>-2of3. No other job is called so


def in_commit(repo: Path, file: str) -> bool:
    """Is this file in the commit the repo stands at? (That commit is what a machine is sent.)"""
    return subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"HEAD:{file}"], capture_output=True).returncode == 0


def shared_out(commands: list[str], machines: int) -> list[list[str]]:
    """A job's commands for each of `machines` machines: every one a `lab run`, given `--only` and its share of
    that run's problems. What is shared out is problems and never a problem's arms: an arm recalls what its
    agents share with an earlier one from the cache of the machine both are played on. So a problem has one
    machine, whichever of the commands plays it; problems are dealt out one at a time in the order they first
    come, so that each machine has early and late ones. A machine that has none of a run's problems does not
    play that run.

    Everything that would fail on every machine, or bring back what cannot be put together, is refused here,
    before any is rented: a command that is not one `lab run` on one line, an arm there is not, `--only`, a run
    with no problems, two commands for one run, and a run that is here or in the commit already (it would go
    to every machine, and every part would bring all of it back)."""
    from . import cli, experiment
    read, named = [], set()
    for command in commands:
        made_of = parts(command)
        at = lab_run(made_of[0]) if len(made_of) == 1 and "\n" not in command and "\r" not in command else None
        if at is None:
            raise SystemExit(f"with --machines every command is one `lab run`, on one line, and this is not:\n    {command}")
        args = cli.parser().parse_args(made_of[0][at + 1:])     # as `lab run` itself reads it
        if args.only:
            raise SystemExit(f"--machines shares a run's problems out itself: leave --only out of\n    {command}")
        if args.dry_run:
            raise SystemExit(f"a dry run needs no machine:\n    {command}")
        for said in (args.experiment, args.name or "main"):      # a name is a name: what a shell would make of `$`, `~` or a `/`
            if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", said):       # on each machine is not this code's to guess
                raise SystemExit(f"with --machines an experiment and a run are called by plain names (letters, digits, _ . -), not {said!r}")
        exp = experiment.load(args.experiment)
        changed = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", f"experiments/{args.experiment}/experiment.py"],
                                 capture_output=True, text=True).stdout.strip()
        if changed:                                              # problems are dealt out from this file as it is here,
            raise SystemExit(f"experiments/{args.experiment}/experiment.py here is not what is committed, and a machine plays what is "
                             "committed: commit it first")
        if (unknown := [name for name in args.arms or [] if name not in exp.arms]):
            raise SystemExit(f"no arm {', '.join(unknown)} in {exp.name} (arms: {', '.join(exp.arms)})")
        run = (args.experiment, args.name or "main")
        if run in named:
            raise SystemExit(f"two commands for one run ({run[0]}/{run[1]}): with --machines a run is one command, with all its arms")
        named.add(run)
        here = EXPERIMENTS / run[0] / "runs" / run[1]
        if (here / "config.json").exists() or in_commit(ROOT, f"experiments/{run[0]}/runs/{run[1]}/config.json"):
            raise SystemExit(f"{here.relative_to(ROOT)} is here already (in this folder, or in the commit that would be sent), and a run that is "
                             "here is carried on by one machine.\nWith --machines hand in a run that is not here: give it another --name "
                             "(what was played is recalled from the controller's cache, and its parts come back whole).")
        problems = cli.problems_of(args)
        if not problems:
            raise SystemExit(f"this command has no problems to play:\n    {command}")
        if len({problem.id for problem in problems}) != len(problems):
            raise SystemExit(f"two problems of this run have one id, and --only goes by id: it cannot be shared out\n    {command}")
        read.append((command, problems))
    machine_of: dict = {}
    for _, problems in read:
        for problem in problems:
            machine_of.setdefault((problem.benchmark, problem.id), len(machine_of) % machines)
    if len(machine_of) < machines:
        raise SystemExit(f"{len(machine_of)} problems cannot be shared out over {machines} machines")
    out: list[list[str]] = [[] for _ in range(machines)]
    for command, problems in read:
        for k in range(machines):
            share = [problem.id for problem in problems if machine_of[problem.benchmark, problem.id] == k]
            if not share:                                        # none of this run's problems are this machine's
                continue
            words = parts(command)[0]                            # the command is sent as the words it was read as here, each
            shared = shlex.join([*words, "--only", *share])      # one quoted: a shell there makes nothing else of them
            back = parts(shared)                                 # and read back as the machine will read it: a command that hid
            at = lab_run(back[0]) if len(back) == 1 else None    # what was added (behind a `#`, say) would play every problem
            if at is None or cli.parser().parse_args(back[0][at + 1:]).only != share or back[0][:len(words)] != words:
                raise SystemExit(f"--only cannot be added to this command so that it is read:\n    {command}")
            out[k].append(shared)
    return out


def jobs_there(where: Where) -> list[dict]:
    """Every job the controller's machine has, as its `status --json` gives them. Not being able to ask is an
    error and not "none": what is decided by this (is a name taken? which jobs are a run's parts?) must not be
    decided blind."""
    said = where.cloud("status", "--json", capture=True)
    try:
        if said.returncode:
            raise ValueError
        return json.loads(said.stdout) if said.stdout.strip() else []
    except ValueError:
        raise SystemExit(f"could not ask {where.host} which jobs it has, so nothing was done:\n{(said.stdout + said.stderr).strip()[-300:]}") from None


def stage(where: Where, args, commands: list[str], name: str) -> dict:
    """Pack one job and lay it on the controller's machine beside the jobs, not yet among them. Returns the job."""
    gpus = args.gpu or settings().get("gpu") or ["h100", "a100"]
    instance = {"ip": args.instance, **({"key": args.instance_key} if args.instance_key else {})} if args.instance else None
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary) / name
        job = build(commands, name, gpus, args.model, folder, args.allow_dirty, instance=instance, max_hours=args.max_hours,
                    keep_on_failure=args.keep_on_failure or None, keep_hours=args.keep_hours, regions=args.regions,
                    retries=getattr(args, "retries", None),
                    keys=public_keys() or None)
        if where.shell(f"test -e {shlex.quote(f'{where.home}/jobs/{name}')}").returncode == 0:
            raise SystemExit(f"there is a job called {name} already: give this one another --name")
        where.send_code()
        code_into(folder / "code")                               # the job is looked after by the code it is handed in with
        # handed in beside the jobs, and taken in among them by `launch` once all of it is there: what looks after
        # jobs on that machine never finds half of one
        where.put(folder, f"incoming/{name}", fresh=True)
    return job


def start(where: Where, args, job: dict, name: str) -> None:
    """Take a job that was laid there in among the jobs, and have its controller started."""
    done = where.cloud("launch", name, capture=True)
    if done.returncode:
        raise SystemExit(f"the job was handed over, but its controller did not start:\n{done.stdout}{done.stderr}")
    wanted = f"the machine at {args.instance}" if args.instance else f"the first of {', '.join(job['kinds'])} that is free"
    print(f"job {name}: handed to {where.host}, which waits for {wanted}, runs\n" + "".join(f"    {command}\n" for command in job["commands"])
          + f"on it with {args.model}, copies back what it makes, and gives the machine back when it has ended.")


def say(line: str) -> None:
    """Print, and never fail for it: what is said while something is being undone must not stop the undoing
    (the terminal may be gone, or a pipe closed)."""
    try:
        print(line, flush=True)
    except Exception:
        pass


def taken_back(where: Where, name: str, names: list[str]) -> None:
    """A run that could not all be handed in is no run. Every part of this hand-in is seen to: what was laid on
    the controller's machine and not taken in is removed first (so that a launch still on its way finds
    nothing), and a part that has become a job is told to stop, started or not as far as this machine knows.
    Says which parts it could not be sure of: those may be renting."""
    say(f"NOT handed in: {name} was to be {len(names)} jobs, and they could not all be handed over. Stopping whatever was started:")
    unsure = []
    for part in names:
        try:
            where.shell(f"rm -rf {shlex.quote(f'{where.home}/incoming/{part}')}")
            there = where.shell(f"test -e {shlex.quote(f'{where.home}/jobs/{part}')}").returncode
            if there == 0 and where.cloud("stop", part, "--now", capture=True).returncode:
                unsure.append(part)
            elif there not in (0, 1):                            # it could not be asked whether the job is there
                unsure.append(part)
            say(f"    {part}: " + ("told to stop" if there == 0 and part not in unsure else "was not started" if there == 1 else "NOT KNOWN"))
        except BaseException:                                    # interrupted again: the others are still seen to
            unsure.append(part)
            say(f"    {part}: NOT KNOWN")
    if unsure:
        say(f"THESE MAY BE RENTING A MACHINE: {', '.join(unsure)}. See `uv run lab cloud status`, and stop each: `uv run lab cloud stop <its name> --now`.")
    else:
        say("None is left: `uv run lab cloud status` says when a machine that was rented is given back.")


def cmd_run(args):
    where = Where(args.controller)
    machines = getattr(args, "machines", None) or 1
    experiments = runs_named([with_model(command, args.model) for command in args.commands])
    stamp = time.strftime("%m%d-%H%M")
    name = args.name or re.sub(r"[^a-z0-9]+", "-", "-".join(experiments[0]) if experiments else "job").strip("-")[:28 if machines == 1 else 22] + f"-{stamp}"
    if re.fullmatch(".+" + PART, name):
        raise SystemExit(f"a name that ends like {name} is how the parts of a run shared out over machines are called: give this job another --name")
    there = jobs_there(where)
    if (taken := [row["job"] for row in there if re.fullmatch(re.escape(name) + PART, row.get("job", "")) or (machines > 1 and row.get("job") == name)]):
        raise SystemExit(f"there is a job called {taken[0]} already: {name} would then mean two runs. Give this one another --name")
    if machines == 1:
        jobs, names = [stage(where, args, args.commands, name)], [name]
        start(where, args, jobs[0], name)
    else:
        if args.instance:
            raise SystemExit("--machines rents the machines itself: it does not go with --instance")
        shares = shared_out([with_model(command, args.model) for command in args.commands], machines)
        names = [a_job(f"{name}-{k}of{machines}") for k in range(1, machines + 1)]
        import swarm_engine
        repos = (ROOT, Path(swarm_engine.__file__).resolve().parents[1])

        def commits() -> list[str]:
            return [subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() for repo in repos]

        def told_to_stop(signum, frame):                         # a timeout or a closed terminal ends this as an error does:
            raise SystemExit(f"this was told to stop (signal {signum}) while the jobs were being handed in")       # what was started is stopped
        # one hand-in of a name at a time: a second, begun before the first is all there, would lay its parts over
        # the first's and undo the first's jobs when it found them
        marker = shlex.quote(f"{where.home}/incoming/.handing-{name}")
        if where.shell(f"mkdir {marker}").returncode:
            raise SystemExit(f"{name} is being handed in already (or a hand-in of it was killed: then `rmdir {where.home}/incoming/.handing-{name}` "
                             f"on {where.host}, after `uv run lab cloud status` shows none of its parts)")
        import signal
        handlers = {sig: signal.signal(sig, told_to_stop) for sig in (signal.SIGTERM, signal.SIGHUP)}
        try:                                                     # all of them packed and laid there before any is started
            before = commits()
            jobs = [stage(where, args, commands, part) for commands, part in zip(shares, names, strict=True)]
            if commits() != before:
                raise SystemExit("a commit was made while the jobs were being packed: they would not all be the same code")
            for job, part in zip(jobs, names, strict=True):
                start(where, args, job, part)
        except BaseException:
            taken_back(where, name, names)
            raise
        finally:
            for sig, handler in handlers.items():
                signal.signal(sig, handler)
            where.shell(f"rmdir {marker}")
        print(f"{machines} jobs, each with a share of every run's problems and a machine of its own. They are one run: `pull {name}` brings them back "
              f"together." + (f" Each has its own {args.max_hours:g} hours at most: {machines * args.max_hours:g} machine-hours in all." if args.max_hours else
                              " None has a limit on its hours (--max-hours)."))
    print(("This machine has to stay awake until then: the job is looked after here.\n" if where.here else "This machine can be closed now.\n")
          + "".join(f"    uv run lab cloud status {part}\n    uv run lab cloud logs {part}\n" for part in names)
          + f"    uv run lab cloud pull {name}      # when it is done, or to look before"
          + ("\nTo get into its machine while it is up: ssh ubuntu@<the address `status` gives> (it accepts this machine's ssh key)"
             if jobs[0].get("keys") else ""))


def cmd_check(args):
    """A first job on a kind of GPU: the machine is set up, the engine is held against its server and timed, and
    this repo's tests are run there. What it finds comes back under ../swarm_engine/results."""
    day = time.strftime("%Y-%m-%d")
    engine = f"uv run --project ../{REPO}"                       # the engine's own folder, with this lab's environment
    called = re.sub(r"[^A-Za-z0-9._-]+", "-", args.model).strip("-")      # the model, as part of a file's name
    checks = [f"(cd ../{ENGINE} && {engine} swarm-vllm check --model {shlex.quote(args.model)} "
              f"--out \"results/{day}-gpu/check-{called}-$SWARM_CLOUD_INSTANCE_TYPE.json\")",
              "uv run pytest -q", f"(cd ../{ENGINE} && {engine} pytest -q)"]
    # one command, so that each part is run whatever the one before it found; it fails if any of them did
    args.commands = ["failed=0; " + " ".join(f"{check} || failed=1;" for check in checks) + " exit $failed"]
    args.name = args.name or re.sub(r"[^a-z0-9]+", "-", f"check-{args.model.lower()}").strip("-")[:28] + f"-{time.strftime('%m%d-%H%M')}"
    args.retries = 0                                             # what a check finds is not made better by asking again
    cmd_run(args)


def a_job(name: str) -> str:
    """A job's name, which is also a folder's and part of a command line somewhere else: nothing but what a name may be."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", name):
        raise SystemExit(f"a job's name is lower case letters, digits and dashes: {name!r}")
    return name


def cmd_pass(args):
    """`status`, `logs`, `stop`, `machines`: asked of the controller's machine as they are. Asked of a run that was
    shared out over machines by the name it was handed in under, each of its parts is asked in turn."""
    where = Where(args.controller)
    more = (["--now"] if getattr(args, "now", False) else []) + (["-n", str(args.n)] if getattr(args, "n", None) else [])
    wanted = [a_job(args.job)] if getattr(args, "job", None) else []
    if wanted:
        try:
            there = jobs_there(where)
        except SystemExit:                                       # the list cannot be read: the name is asked as it was given,
            there = [{"job": wanted[0]}]                         # as a plain job's always was. A stop is not held up for a list
        if not any(row.get("job") == wanted[0] for row in there):
            wanted = [row["job"] for row in parts_of(wanted[0], there)] or wanted
    worst = 0
    for job in wanted or [None]:
        if len(wanted) > 1:
            print(f"---- {job}", flush=True)
        worst = where.cloud(args.cloud, *([job] if job else []), *more).returncode or worst
    if worst:
        sys.exit(worst if len(wanted) < 2 else 1)


STREAMS = ("episodes", "posts", "looks", "transcripts", "engine")


def lines_of(file: Path) -> list[tuple[bytes, dict]]:
    """A stream's lines as they are written, each with the row it holds: without a last line that a copy of a
    file still being written cut short. (Lines end on a newline and on nothing else: a row may hold any
    character.)"""
    out = []
    for line in file.read_bytes().split(b"\n") if file.exists() else []:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict):
            out.append((line, row))
    return out


def pairs_of(folder: Path) -> set:
    return {(row["arm"], row["benchmark"], row["problem"]) for _, row in lines_of(folder / "episodes.jsonl") if "arm" in row and "problem" in row}


def joined(pieces: list[tuple[str, Path]], here: Path, of: int, force: bool = False, all_over: bool = True) -> str:
    """Make one run folder at `here` of the parts of a run that was shared out over machines (`pieces`: a job's
    name and its copy of the run folder, in the jobs' order; `of`: how many jobs the hand-in was; `all_over`:
    every one of those jobs is there and has ended and been copied). Returns a line that says what came of it,
    beginning "NOT brought" if nothing was changed here.

    The parts must be one run (the same settings) and have no (arm, problem) in common. What each wrote down is
    put end to end, as it was written, and the tables are worked out again over all of it. The run is `done`
    only when every job has ended, every part of it says done, and every arm has every problem. A folder that
    is here already is written over only if it is this same run's and holds nothing the parts do not (a copy
    that was cut short, or a job that added to it, is not undone), or with `force`; what was added to it by
    hand stays. Nothing here is changed before all of that is known."""
    from . import report
    from .problems import select
    from .tracking import Run
    what = here.relative_to(ROOT)
    try:
        configs = [json.loads((folder / "config.json").read_text()) for _, folder in pieces]
    except ValueError:
        return f"NOT brought: {what}: a part's config.json did not come whole (ask again in a minute)"
    for (job, _), config in zip(pieces[1:], configs[1:], strict=True):
        if config.get("settings") != configs[0].get("settings"):
            differ = sorted(key for key in {*config.get("settings", {}), *configs[0].get("settings", {})}
                            if config.get("settings", {}).get(key) != configs[0].get("settings", {}).get(key))
            return f"NOT brought: {what}: {job} and {pieces[0][0]} are not one run (they differ in {', '.join(differ)})"
    seen: set = set()
    for job, folder in pieces:
        mine = pairs_of(folder)
        if seen & mine:
            return f"NOT brought: {what}: {job} has played a problem under an arm that another part has played"
        seen |= mine
    started = {config.get("started") for config in configs}
    ours = None
    if (here / "config.json").exists():
        there = json.loads((here / "config.json").read_text())
        ours = there.get("started") in started
        if not ours and not force:
            return f"NOT brought: {what} is another run here (begun {there.get('started')}): --force puts the job's in its place"
        if ours and (more := pairs_of(here) - seen) and not force:
            return (f"NOT brought: {what} holds {len(more)} pairs of an arm and a problem that the parts do not: a copy may have been cut short, or "
                    "another job added to it. Nothing was changed (--force puts the parts' in its place)")
    settings_ = configs[0].get("settings", {})
    try:
        wanted = len([key for key in settings_ if key.startswith("arm:")]) * len(select(settings_["benchmarks"], settings_["split"], settings_["problems"]))
    except (Exception, SystemExit):                              # the problems are not on this machine: the parts' word is taken
        wanted = len(seen)
    streams = {stream: b"".join(line + b"\n" for _, folder in pieces for line, _ in lines_of(folder / f"{stream}.jsonl"))
               for stream in STREAMS if any((folder / f"{stream}.jsonl").exists() for _, folder in pieces)}
    log = b"".join((folder / "log.txt").read_bytes() for _, folder in pieces if (folder / "log.txt").exists())
    whole = all_over and all(config.get("status") == "done" for config in configs) and len(seen) == wanted
    finished = max((config.get("finished") or "" for config in configs), default="") if whole else None
    command = re.sub(r"\s--only(\s+\S+)+\s*$", "", str(configs[0].get("command", "")))         # the run's, without the first part's share
    record = [{"job": job} | {key: config.get(key) for key in ("started", "finished", "status", "command", "machines", "git")}
              for (job, _), config in zip(pieces, configs, strict=True)]
    config = configs[0] | {"status": "done" if whole else "running", "finished": finished, "command": command, "parts": record, "parts_in_all": of}

    episodes = [row for _, folder in pieces for _, row in lines_of(folder / "episodes.jsonl")]
    summary = report.summary_of(episodes, report.baseline_of(settings_))     # the tables, of the rows as they are joined
    tables = report.tables(summary) + "\n\n" + report.NOTES + " " + report.DESK_NOTES + "\n"

    if ours is False:
        shutil.rmtree(here)
    here.mkdir(parents=True, exist_ok=True)

    def put(name: str, data: bytes):                             # whole or not at all: a file here is never half written
        (here / f".{name}.coming").write_bytes(data)
        (here / f".{name}.coming").replace(here / name)
    try:
        for stream, data in streams.items():
            put(f"{stream}.jsonl", data)
        put("log.txt", log)
        put("summary.json", (json.dumps(summary, indent=2, ensure_ascii=False) + "\n").encode())      # as `Run.save` writes it
        put("summary.md", tables.encode())
        put("config.json", (json.dumps(config, indent=2) + "\n").encode())      # last: what says the run is done
    finally:
        for left in here.glob(".*.coming"):
            left.unlink()
    Run(here)                                                    # and it is a run as any other is
    return f"{what} (from {len(pieces)} of the {of} jobs; {'done' if whole else 'not whole yet'}; {len(seen)} of {wanted} pairs of an arm and a problem)"


def parts_of(name: str, there: list[dict]) -> list[dict]:
    """The jobs that are the parts of a run shared out over machines under `name` (`<name>-1of3`, ...), in order."""
    found = [(int(m[1]), int(m[2]), row) for row in there if (m := re.fullmatch(re.escape(name) + PART, row.get("job", "")))]
    if len({n for _, n, _ in found}) > 1:
        raise SystemExit(f"{name} names more than one run on the controller's machine ({', '.join(sorted(row['job'] for _, _, row in found))}): "
                         "that should not be. Bring each back by hand from its jobs' folders there")
    return [row | {"part": k, "of": n} for k, n, row in sorted(found, key=lambda item: item[0])]


def cmd_pull(args):
    """Bring a job's run folders into experiments/ here, and write the standings again. A run that was shared out
    over machines (`lab cloud run --machines`) is asked for by the name it was handed in under, or by a part's:
    its parts are brought together as one run."""
    import swarm_engine
    where = Where(args.controller)
    if (one := re.fullmatch("(.+)" + PART, a_job(args.job))):       # a part asked for by its own name: its run is all of its parts,
        print(f"{args.job} is one part of a run that was shared out over machines: bringing all of {one[1]}.")      # and a part laid
        args.job = one[1]                                         # over the run folder would leave that folder with one part of it
    said = where.cloud("status", a_job(args.job), "--json", capture=True)
    found = json.loads(said.stdout) if said.returncode == 0 and said.stdout.strip() else []
    parts_found = [] if found else parts_of(args.job, jobs_there(where))
    if not found and not parts_found:
        raise SystemExit(said.stdout + said.stderr or f"no job called {args.job}, and no parts of one ({args.job}-1of2, ...)")
    brought, refused = [], []
    with tempfile.TemporaryDirectory() as temporary:
        came = Path(temporary)
        if parts_found:
            of = parts_found[0]["of"]
            phases = ", ".join(f"{part['job']} is {part['phase']}" for part in parts_found)
            missing = of - len(parts_found)
            print(f"{args.job} was shared out over {of} machines: {phases}" + (f"; {missing} of its parts are not on the controller's machine" if missing > 0 else "") + ".")
            for part in parts_found:
                if not where.get(f"jobs/{part['job']}/mirror/work/{REPO}/experiments", came / part["job"] / "experiments"):
                    there = where.shell(f"test -e {shlex.quote(f'{where.home}/jobs/' + part['job'] + f'/mirror/work/{REPO}/experiments')}").returncode
                    if there != 1:                                # it has made something (or that could not be asked), and it did not come:
                        raise SystemExit(f"could not copy what {part['job']} made from {where.host}: nothing was changed here. Ask again.")      # a run of the rest would be short of it
            runs = sorted({(config.parent.parent.parent.name, config.parent.name)
                           for part in parts_found for config in (came / part["job"] / "experiments").glob("*/runs/*/config.json")})
            all_over = missing <= 0 and all(part["phase"] == "done" for part in parts_found)
            for experiment, run in runs:
                pieces = [(part["job"], came / part["job"] / "experiments" / experiment / "runs" / run) for part in parts_found
                          if (came / part["job"] / "experiments" / experiment / "runs" / run / "config.json").exists()]
                line = joined(pieces, EXPERIMENTS / experiment / "runs" / run, of, args.force, all_over)
                (refused if line.startswith("NOT brought") else brought).append(line)
            results_of = [part["job"] for part in parts_found]
        else:
            where.get(f"jobs/{args.job}/mirror/work/{REPO}/experiments", came / "experiments")
            for config in sorted((came / "experiments").glob("*/runs/*/config.json")):
                run = config.parent
                here = EXPERIMENTS / run.parent.parent.name / "runs" / run.name
                mine = json.loads((here / "config.json").read_text()) if (here / "config.json").exists() else None
                if mine is not None and mine.get("started") != json.loads(config.read_text()).get("started") and not args.force:
                    print(f"NOT brought: {here.relative_to(ROOT)} is another run here (begun {mine.get('started')}): --force puts the job's in its place")
                    continue
                if mine is not None and mine.get("started") != json.loads(config.read_text()).get("started"):
                    shutil.rmtree(here)
                shutil.copytree(run, here, dirs_exist_ok=True, symlinks=True)
                status = json.loads(config.read_text()).get("status")
                brought.append(f"{here.relative_to(ROOT)} ({status})")
            results_of = [args.job]
        results = Path(swarm_engine.__file__).resolve().parents[1] / "results"
        for job in results_of:
            if where.get(f"jobs/{job}/mirror/work/{ENGINE}/results", came / "results" / job):
                for file in sorted(p for p in (came / "results" / job).rglob("*") if p.is_file()):
                    (results / file.relative_to(came / "results" / job)).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, results / file.relative_to(came / "results" / job))
                    brought.append(f"../{ENGINE}/results/{file.relative_to(came / 'results' / job)}")
    if not parts_found:
        print(f"job {args.job} is {found[0]['phase']}" + ("" if found[0]["phase"] in ("done", "failed", "stopped") else ": what it has made so far") + ".")
    for line in refused:
        print(line)
    print("\n".join(f"  brought {line}" for line in brought) or "  nothing to bring yet")
    if any("runs/" in line for line in brought):
        from . import standings
        print("  " + standings.write(strict=False))
        print("Read a run before believing it (uv run lab show <experiment>/<run>), then commit its folder with its write-up.")


def add_commands(commands) -> None:
    """`lab cloud ...` on the lab's command line."""
    cloud = commands.add_parser("cloud", help="a run on a rented GPU: hand it in, look at it, bring it back",
                                description=__doc__, formatter_class=__import__("argparse").RawDescriptionHelpFormatter)
    cloud.add_argument("--controller", help="where jobs are looked after: an ssh host, or `here` (default: what `lab cloud setup` was told)")
    sub = cloud.add_subparsers(dest="cloud", required=True)

    setup = sub.add_parser("setup", help="once: say where jobs are looked after, and make that machine ready")
    setup.add_argument("--controller", required=True, help="an ssh host that is always on (`myserver`), or `here`")
    setup.add_argument("--api-key-file", help="a file that holds the Lambda API key, alone or as a line LAMBDA_API_KEY=... (a .env): "
                                              "the key is copied to the controller's machine")
    setup.add_argument("--gpu", nargs="+", help="the GPUs a job asks for when it does not say (default: h100 a100)")
    setup.set_defaults(go=cmd_setup)

    def job_options(parser):
        parser.add_argument("--gpu", nargs="+", help="what to rent, the one wanted most first: h100, a100, a10, or Lambda's own names")
        parser.add_argument("--model", default=GPU_MODEL, help="the model served there, and given to `lab run` commands that name none")
        parser.add_argument("--name", help="the job's name (default: from the run it makes, and the time)")
        parser.add_argument("--regions", nargs="+", help="only these regions (default: wherever a machine is free)")
        parser.add_argument("--max-hours", type=hours, help="stop the job and give the machine back after this long (default: no limit)")
        parser.add_argument("--keep-on-failure", action="store_true",
                            help="leave the machine up if the job fails, to look at it: it bills until `stop`, and is given back "
                                 "by itself after --keep-hours, or at --max-hours if that comes first")
        parser.add_argument("--keep-hours", type=hours, help="with --keep-on-failure: how long a failed job's machine is kept (default: 3)")
        parser.add_argument("--allow-dirty", action="store_true", help="send the last commit though there are uncommitted changes")
        parser.add_argument("--instance", metavar="IP", help="use this machine, which is already up; it is not given back")
        parser.add_argument("--instance-key", help="with --instance: the ssh key that machine accepts, if not the controller's own")

    run = sub.add_parser("run", help="hand a job in: one or more commands, run in order on a rented GPU")
    run.add_argument("commands", nargs="+", metavar="COMMAND", help='a command as it is typed here, without `uv run`: "lab run every_step --name gpu_main"')
    job_options(run)
    run.add_argument("--machines", type=machines, metavar="N", help="share every run's problems out over N machines, a job each with its own "
                     "--max-hours: much the same machine-hours in all, and done the sooner. Every command is then a `lab run` of a run that "
                     "is not here yet. `lab cloud pull <name>` brings the parts back as one run; status, logs and stop take <name> too")
    run.set_defaults(go=lambda args: cmd_run(prepared(args)))

    check = sub.add_parser("check", help="a first job on a kind of GPU: is it ready, does the engine hold, how fast is it")
    job_options(check)
    check.set_defaults(go=cmd_check)

    for name, about in (("status", "where jobs stand"), ("logs", "the end of what a job has printed"), ("stop", "end a job and give its machine back"),
                        ("machines", "every machine the account rents now")):
        passed = sub.add_parser(name, help=about)
        if name != "machines":
            passed.add_argument("job", **({"nargs": "?"} if name == "status" else {}))
        if name == "stop":
            passed.add_argument("--now", action="store_true", help="without copying anything more back")
        if name == "logs":
            passed.add_argument("-n", type=int, default=40)
        passed.set_defaults(go=cmd_pass)

    pull = sub.add_parser("pull", help="bring a job's run folders into experiments/, and write the standings again")
    pull.add_argument("job", help="a job, or the name a run was handed in under with --machines: its parts come back as one run")
    pull.add_argument("--force", action="store_true", help="put a job's run folder in the place of another run of the same name here")
    pull.set_defaults(go=cmd_pull)


def machines(text: str) -> int:
    """How many machines, as an option gives it: 1 to 8."""
    try:
        value = int(text)
    except ValueError:
        value = 0
    if not 1 <= value <= 8:
        raise argparse.ArgumentTypeError(f"a number of machines from 1 to 8, not {text!r}")
    return value


def hours(text: str) -> float:
    """A number of hours, as an option gives one: above 0. (0 was once read as "no limit" where a limit was meant.)"""
    try:
        value = float(text)
    except ValueError:
        value = 0.0
    if not 0 < value < float("inf"):
        raise argparse.ArgumentTypeError(f"a number of hours above 0, not {text!r}")
    return value


def prepared(args):
    """A job's commands as they are run there: under `uv run`, from this repo's folder."""
    args.commands = [command if command.startswith(("uv ", "cd ", "bash ", "sudo ")) else f"uv run {command}" for command in args.commands]
    return args
