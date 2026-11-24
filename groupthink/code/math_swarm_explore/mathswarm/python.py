"""Run a Python file that an agent wrote, and say what happened.

    python = Python()
    python.check("from fractions import Fraction\\nprint(Fraction(3, 4) + Fraction(1, 6))")   ->  Ran("ok", "11/12\\n")

The file is run by the Python this repo runs on, with what is installed beside it: the standard library, sympy
and numpy. What comes back is one of:

    ok            it ran to the end; `output` is what it printed (`error` holds any warnings)
    error         it stopped: an exception, an `assert` that was false, bad syntax; `error` is the traceback
    timeout       it ran past the time limit; `error` says which line of the file it was in
    memory        it held more memory than it may
    unavailable   there is no sandbox to run it in here

"ok" means the file ran and every `assert` in it held. It does not mean the file says what the problem says: an
agent can assert `2 + 2 == 4` beside a wrong answer, or print a number it typed in. Whether a run is evidence
for an answer is for the reader, agent or human, to judge.

The code is a model's, so it is not trusted, and unlike Lean it is not screened first: no list of words keeps
Python harmless, so the sandbox is all there is. It is a macOS sandbox (`sandbox-exec`) with no network, no
other programs, no signals to other processes and no system services. The file can write only inside a scratch
folder of its own, and can read only that folder, Python and its libraries, and the system's own libraries:
nothing in the home directory, this repo included, and nothing of another agent's run. It can still see that a
file exists (its size and dates).
macOS enforces no memory limit on a process, so each run is watched from outside and killed if it goes over,
as it is when it runs out of time. `Python.leaks()` tries the ways out; `lab doctor` and a test call it.

A run that reaches its time limit stops itself, a moment before it would be killed, so that it can say which
line it was in (`WATCH`). That is a courtesy the file could switch off; the limit is the watch from outside.

What a file did is kept in data/cache/python.sqlite, so a replayed run runs nothing twice and is told the same
thing again: without that, a file that just beat the clock once could change the conversation the second time.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import sysconfig
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path

from .paths import CACHE, ROOT

FILE = "work.py"          # what an agent's file is called where it runs, and so in its tracebacks
TIMEOUT = 30              # seconds a run may take
SANDBOX = "/usr/bin/sandbox-exec"
MAX_PRINTED = 2**20       # bytes a run may print before it is stopped
GRACE = 1.0               # seconds past its time limit that a run has to say where it was, before it is killed
KEPT = 4000               # what is kept of what it printed, and of an error: the start and the end, in characters
ENV = {
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",                # sets come out in the same order every run, so a rerun prints the same
    "PYTHONINTMAXSTRDIGITS": "0",         # a whole number of any length can be printed
    "PYTHONIOENCODING": "utf-8",
    "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1",     # one core for each run
    "MPLBACKEND": "Agg",                  # a plot is drawn nowhere, instead of asking for a window
}

# What Python reads as it starts a run (a `sitecustomize`): when the run's time is up, say where it is and stop.
WATCH = """import faulthandler, os
faulthandler.dump_traceback_later(float(os.environ["MATHSWARM_TIMEOUT"]), exit=True)
"""

# A file that tries each way out of the sandbox and prints the ones that worked.
PROBE = """import os, socket, subprocess

def way_out(name, attempt):
    try:
        attempt()
    except BaseException:
        return
    print(name)

way_out("read a file of this repo", lambda: open({secret!r}).read())
way_out("read /etc/hosts", lambda: open("/etc/hosts").read())
way_out("list the home directory", lambda: os.listdir({home!r}))
way_out("write outside its folder", lambda: (open({outside!r}, "w").close(), os.remove({outside!r})))
way_out("list the folder above its own", lambda: os.listdir(".."))
way_out("open a socket", lambda: socket.socket().bind(("127.0.0.1", 0)))
way_out("start a program", lambda: subprocess.run(["/bin/echo"], stdout=subprocess.DEVNULL))
way_out("fork", lambda: os.fork() or os._exit(0))
way_out("signal another process", lambda: os.kill(os.getppid(), 0))
"""

_LIBRARY = re.compile(r'/[^\s"\'()]*/(?:site-packages|lib/python[\d.]+)/')      # where this machine keeps Python's libraries
_FRAME = re.compile(rf'File "{re.escape(FILE)}", line (\d+) in (\S+)')      # a line of the agent's file, where Python says it was
_TIME_UP = re.compile(r"^Timeout \(\d+:\d\d:\d\d(?:\.\d+)?\)!$", re.M)          # what `WATCH` makes Python say first
_ANSWER = re.compile(r"^[ \t]*ANSWER[ \t]*[:=][ \t]*(\S.*?)[ \t]*$", re.M | re.I)


def answered(printed: str) -> str | None:
    """The answer a run printed: what follows its last `ANSWER:`."""
    found = _ANSWER.findall(printed)
    return found[-1] if found else None


@dataclass(frozen=True)
class Ran:
    status: str
    output: str = ""                 # what it printed
    error: str = ""                  # the traceback, or why it was stopped or not run; after an `ok`, its warnings
    seconds: float = 0.0
    answer: str | None = None        # last ANSWER from the full output of a successful run, before truncation

    @property
    def ok(self) -> bool:
        return self.status == "ok"

    def told(self, limit: int = 3000) -> str:
        """What an agent is told when it runs its file: a sentence, then what Python printed and said."""
        error = middle(self.error, limit // 2)
        printed = middle(self.output.rstrip("\n"), limit - len(error))
        before = f"\nBefore that it printed:\n{printed}" if printed else "\nIt had printed nothing."
        if self.status == "ok":
            took = f" in {self.seconds:.0f} seconds" if self.seconds >= 5 else ""
            return (f"It ran with no errors{took}. It printed:\n{printed}" if printed else
                    f"It ran with no errors{took} and printed nothing: `print` shows a value.") + (f"\nIt also warned:\n{error}" if error else "")
        if self.status == "error":
            return f"It stopped with an error:\n{error}" + before
        if self.status == "timeout":
            return f"It was stopped: {error}. Make what it computes smaller." + before
        if self.status == "memory":
            return f"It was stopped: {error}. Make what it holds smaller." + before
        return f"Python could not be run on it: {error}."


def middle(text: str, limit: int) -> str:
    """A long text with its middle left out: the start says what was being done, the end how it came out."""
    if len(text) <= limit:
        return text
    head = limit // 3
    return f"{text[:head].rstrip()}\n… (the middle is left out) …\n{text[len(text) - (limit - head):].lstrip()}"


def where(said: str) -> str:
    """Where in the agent's file a run was when it was stopped, from what Python said as it went: "at line 5
    (in f), called from line 8 (in g), called from line 11". Empty if Python did not say."""
    lines = [f"line {line}" + ("" if name == "<module>" else f" (in {name})") for line, name in _FRAME.findall(said)]
    return "at " + ", called from ".join(lines[:4]) if lines else ""


def tidy(text: str, desk: Path) -> str:
    """What Python said, without this machine's folders: the agent's file is `work.py`, and a library's file is
    its path inside the library, wherever Python names it. The same run then reads the same every time, and an
    agent is not told where on this machine it runs."""
    return _LIBRARY.sub("", text.replace(f"{desk}/", ""))


class Python:
    def __init__(self, timeout: float = TIMEOUT, workers: int = 4, memory_mb: int = 1000, cache: Path | None = CACHE / "python.sqlite"):
        """`timeout` seconds and `memory_mb` are per file; `workers` is how many files of one `check_many` run
        at once. `cache=None` keeps nothing. There is no way to run a file outside the sandbox."""
        self.timeout, self.workers, self.memory_mb = timeout, workers, memory_mb
        self._lock = threading.Lock()
        self._setup: str | None = None                         # what the cache is keyed on, once the sandbox is ready
        self._work: Path | None = None
        self._watch: Path | None = None                        # the folder that holds `WATCH`, for every run to read
        self._usage = None
        self._db = None
        if cache is not None:
            cache.parent.mkdir(parents=True, exist_ok=True)
            self._db = sqlite3.connect(cache, check_same_thread=False)
            self._db.execute("create table if not exists runs (key text primary key, code text, ran text, at text)")
        self.asked = self.recalled = 0

    # ---- the sandbox
    def ready(self) -> str | None:
        """None if files can be run here, otherwise why not."""
        try:
            self._resolve()
        except RuntimeError as problem:
            return str(problem)
        return None

    def _resolve(self) -> str:
        with self._lock:
            if self._setup is None:
                if not os.access(SANDBOX, os.X_OK):
                    raise RuntimeError(f"no {SANDBOX} to run agents' Python in")
                try:
                    self._usage = ctypes.CDLL("/usr/lib/libproc.dylib").proc_pid_rusage
                except (OSError, AttributeError):
                    raise RuntimeError("no libproc to watch the memory of agents' Python with") from None
                self._work = Path(os.path.realpath(tempfile.mkdtemp(prefix="mathswarm-python-")))
                self._watch = Path(os.path.realpath(tempfile.mkdtemp(prefix="mathswarm-watch-")))
                (self._watch / "sitecustomize.py").write_text(WATCH, encoding="utf-8")
                self._setup = f"{sys.version}\nsympy {version('sympy')}\nnumpy {version('numpy')}"
            return self._setup

    def _rules(self, desk: Path) -> str:
        """The sandbox of one run: what Python needs to start and to import its libraries, the folder the file
        runs in, and nothing else of this machine. Reading is refused everywhere and then allowed place by
        place. The rules are handed to the sandbox as text: there is no file of them for a run to rewrite."""
        python = os.path.realpath(sys.base_prefix)
        libraries = sorted({os.path.realpath(sysconfig.get_path(name)) for name in ("purelib", "platlib")})
        config = os.path.realpath(os.path.join(sys.prefix, "pyvenv.cfg"))       # how a virtual environment finds its libraries
        readable = " ".join(f'(subpath "{place}")' for place in ["/usr/lib", "/usr/share", "/System", "/dev", python, *libraries, self._watch, desk])
        return "\n".join([
            "(version 1)", "(allow default)",
            "(deny network*)",
            "(deny process-fork)", "(deny process-exec*)", f'(allow process-exec (subpath "{python}"))',
            "(deny signal)", "(allow signal (target self))",
            "(deny mach-lookup)",
            "(deny file-write*)",
            f'(allow file-write* (subpath "{desk}") (literal "/dev/null"))',
            "(deny file-read-data)",
            f'(allow file-read-data (literal "/") (literal "{config}") {readable})',
        ]) + "\n"

    def _footprint(self, pid: int) -> int:
        """The memory a process holds, in bytes, as Activity Monitor counts it; 0 once it is gone."""
        usage = (ctypes.c_uint64 * 64)()                       # a rusage_info_v2, whose tenth field is ri_phys_footprint
        return usage[9] if self._usage(pid, 2, ctypes.byref(usage)) == 0 else 0

    def leaks(self) -> list[str]:
        """The ways out of the sandbox that a file found: none, if the sandbox holds."""
        self._resolve()
        outside = os.path.join(tempfile.gettempdir(), f"mathswarm-probe-{os.getpid()}")
        ran = self._run(PROBE.format(secret=str(ROOT / "pyproject.toml"), home=str(Path.home()), outside=outside))
        return ran.output.split("\n")[:-1] if ran.ok else [f"the probe did not run: {ran.error}"]

    # ---- running
    def check(self, code: str) -> Ran:
        return self.check_many([code])[0]

    def check_many(self, codes: list[str]) -> list[Ran]:
        """What each file did, in the order asked. The same file is run once."""
        unique = list(dict.fromkeys(codes))
        with ThreadPoolExecutor(max_workers=max(1, min(self.workers, len(unique) or 1))) as pool:
            ran = dict(zip(unique, pool.map(self._one, unique)))
        return [ran[code] for code in codes]

    def _one(self, code: str) -> Ran:
        try:
            setup = self._resolve()
        except RuntimeError as problem:
            return Ran("unavailable", error=str(problem))
        key = hashlib.sha256(f"4\n{setup}\n{self.timeout}\n{self.memory_mb}\n{code}".encode()).hexdigest()
        if (kept := self._recall(key)) is not None:
            return kept
        ran = self._run(code)
        self._remember(key, code, ran)
        return ran

    def _run(self, code: str) -> Ran:
        folder = Path(tempfile.mkdtemp(dir=self._work))
        desk = folder / "desk"                                 # where the file runs, and all it can write to
        desk.mkdir()
        (desk / FILE).write_text(code, encoding="utf-8")
        # The shell only sets the most a run may write and then becomes the sandbox, which becomes Python: one
        # process, so the one that is watched and killed is the agent's.
        command = ["/bin/sh", "-c", 'ulimit -f "$0" && exec "$@"', str(MAX_PRINTED // 512),
                   SANDBOX, "-p", self._rules(desk), sys.executable, "-B", "-s", "-u", "-X", "faulthandler", FILE]
        env = {**ENV, "HOME": str(desk), "TMPDIR": str(desk), "PYTHONPATH": str(self._watch), "MATHSWARM_TIMEOUT": f"{self.timeout:g}"}
        started, stopped, child = time.monotonic(), "", None
        try:
            with open(folder / "printed", "wb") as out, open(folder / "said", "wb") as err:
                child = subprocess.Popen(command, cwd=desk, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
                while child.poll() is None and not stopped:
                    if time.monotonic() - started > self.timeout + GRACE:  # it did not stop itself when its time was up
                        stopped = "timeout"
                    elif self._footprint(child.pid) > self.memory_mb * 2**20:
                        stopped = "memory"
                    else:
                        time.sleep(0.01)
            if stopped:
                child.kill()
            child.wait()
            seconds = time.monotonic() - started
            full = (folder / "printed").stat().st_size >= MAX_PRINTED
            printed, said = (tidy((folder / name).read_bytes().decode("utf-8", "replace"), desk) for name in ("printed", "said"))
            if not stopped and child.returncode == 1 and seconds >= self.timeout and _TIME_UP.search(said):
                stopped = "timeout"                            # its time was up, and it said where it was
            answer = answered(printed)
            printed, said = middle(printed, KEPT), middle(said, KEPT)
        finally:
            if child is not None and child.poll() is None:     # the lab was interrupted: the file does not outlive it
                child.kill()
            shutil.rmtree(folder, ignore_errors=True)
        if stopped == "timeout":
            return Ran("timeout", printed, f"no result after {self.timeout:g} seconds" + (f"; it was {at}" if (at := where(said)) else ""), seconds)
        if stopped == "memory":
            return Ran("memory", printed, f"it held more than {self.memory_mb:,} MB of memory", seconds)
        if full:
            return Ran("error", printed, f"it printed more than {MAX_PRINTED // 2**20} MB and was stopped: print less", seconds)
        if child.returncode:
            crashed = f"Python crashed (signal {-child.returncode})" if child.returncode < 0 else f"Python stopped with code {child.returncode}"
            return Ran("error", printed, said.strip() or crashed, seconds)
        return Ran("ok", printed, said.strip(), seconds, answer=answer)

    # ---- remembering
    def _recall(self, key: str) -> Ran | None:
        self.asked += 1
        if self._db is None:
            return None
        with self._lock:
            row = self._db.execute("select ran from runs where key = ?", (key,)).fetchone()
        if row is None:
            return None
        self.recalled += 1
        return Ran(**json.loads(row[0]))

    def _remember(self, key: str, code: str, ran: Ran):
        if self._db is None:
            return
        with self._lock:
            self._db.execute("insert or replace into runs values (?, ?, ?, ?)",
                             (key, code, json.dumps(asdict(ran)), time.strftime("%Y-%m-%d %H:%M:%S")))
            self._db.commit()

    def close(self):
        for folder in (self._work, self._watch):
            if folder is not None:
                shutil.rmtree(folder, ignore_errors=True)
        if self._db is not None:
            self._db.close()
