"""Run a Python file an agent wrote, in a macOS sandbox, and report what happened.

Adapted from ../math_swarm_explore/mathswarm/python.py. The code is a model's, so it is not trusted and nothing
screens it: the sandbox is all there is. A run happens under `sandbox-exec` with no network, no other programs
(no fork, no exec; a Sandbox made with `processes` > 1 may fork copies of its Python, for multiprocessing), no
signals to other processes and no system services. It can write only inside its agent's
folder, and read only that folder, the sandbox's Python and libraries, and the system's own libraries: nothing in
the home directory, this repo included, and nothing of another agent's. macOS enforces no memory limit on a
process, so each run is watched from outside (all its processes together) and killed if it goes over, as it is
when it runs out of time or starts more processes than it may.

The interpreter is .sandbox/bin/python, a venv built from sandbox-requirements.txt by setup_sandbox.sh (NumPy,
SciPy, SymPy, NetworkX, pandas, scikit-learn, gmpy2, Z3, mpmath, and Sage via passagemath).

Usage:
    box = Sandbox(memory_mb=3000, max_parallel=12)
    ran = box.run(Path("runs/x/agents/agent_0"), "scratchpad.py", timeout=60)
    ran.status   # "ok" | "error" | "timeout" | "memory" | "output" | "stopped" | "unavailable"
    box.leaks(Path("/tmp/probe"))   # the ways out a probe file found: [] if the sandbox holds
"""

import ctypes
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / ".sandbox" / "bin" / "python"
HOME_TEMPLATE = ROOT / ".sandbox" / "home-template"  # Sage's import caches, built by setup_sandbox.sh
SANDBOX_EXEC = "/usr/bin/sandbox-exec"
GRACE = 2.0  # seconds past its time limit a run has to say where it was, before it is killed
ENV = {
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",  # sets iterate in the same order every run
    "PYTHONINTMAXSTRDIGITS": "0",  # print integers of any length
    "PYTHONIOENCODING": "utf-8",
    "OMP_NUM_THREADS": "1",  # one core per run: many agents run at once
    "OPENBLAS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "MPLBACKEND": "Agg",
}

# Read by Python at startup (a sitecustomize): when the run's time is up, print where it is and exit.
WATCH = """import faulthandler, os
faulthandler.dump_traceback_later(float(os.environ["SWARM_TIMEOUT"]), exit=True)
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
way_out("connect to the internet", lambda: socket.create_connection(("1.1.1.1", 80), timeout=2))
way_out("start a program", lambda: subprocess.run(["/bin/echo"], stdout=subprocess.DEVNULL))
way_out("fork", lambda: os.fork() or os._exit(0))
way_out("signal another process", lambda: os.kill(os.getppid(), 0))
"""

_LIBRARY = re.compile(r"/[^\s\"'()]*/(?:site-packages|lib/python[\d.]+)/")  # library paths in tracebacks
_FRAME = re.compile(r'File "([^"]+)", line (\d+) in (\S+)')  # a frame as faulthandler prints it
_TIME_UP = re.compile(r"^Timeout \(\d+:\d\d:\d\d(?:\.\d+)?\)!$", re.M)  # what WATCH makes Python print


@dataclass(frozen=True)
class Ran:
    status: str  # ok | error | timeout | memory | output | file | processes | stopped (the harness stopped it) | unavailable
    returncode: int | None
    stdout: str
    stderr: str
    seconds: float
    where: str = ""  # for a timeout: which line of the file it was in


def _quote(path) -> str:
    """A path as a sandbox profile string literal."""
    return '"' + str(path).replace("\\", "\\\\").replace('"', '\\"') + '"'


class Sandbox:
    """Runs agents' files. Safe to share between threads; `max_parallel` caps how many run at once."""

    def __init__(
        self,
        python=PYTHON,
        memory_mb=3000,
        max_output_bytes=2**20,
        max_parallel=None,
        stop: threading.Event | None = None,
        max_file_bytes=None,
        processes=1,
        gate: threading.Semaphore | None = None,
    ):
        """`max_output_bytes`: the most a run may print; `max_file_bytes` (default the same): the largest file it may
        write. `processes`: how many processes a run may have at once (1: fork denied). `memory_mb` is for all of a
        run's processes together. `gate`: a semaphore several Sandboxes share, capping their runs at once together
        (in place of `max_parallel`)."""
        self.python = Path(python)
        self.memory_mb = memory_mb
        self.max_output = max_output_bytes
        self.max_file = max_file_bytes or max_output_bytes
        self.processes = processes
        self.stop = stop or threading.Event()
        self._gate = gate or (threading.BoundedSemaphore(max_parallel) if max_parallel else None)
        self._lock = threading.Lock()
        self._paths = None  # what Python needs to read, found once
        self._watch = None  # folder holding WATCH
        self._usage = None  # proc_pid_rusage, to watch memory
        self._group = None  # proc_listpgrppids, to find a run's processes

    # ---- setup ------------------------------------------------------------

    def ready(self):
        """None if files can be run here, otherwise why not."""
        try:
            self._resolve()
        except RuntimeError as e:
            return str(e)
        return None

    def _resolve(self):
        with self._lock:
            if self._paths is not None:
                return self._paths
            if not os.access(SANDBOX_EXEC, os.X_OK):
                raise RuntimeError(f"no {SANDBOX_EXEC} to run agents' Python in (macOS only)")
            if not self.python.exists():
                raise RuntimeError(f"no sandbox interpreter at {self.python}: run ./setup_sandbox.sh")
            try:
                libproc = ctypes.CDLL("/usr/lib/libproc.dylib")
                self._usage, self._group = libproc.proc_pid_rusage, libproc.proc_listpgrppids
            except (OSError, AttributeError):
                raise RuntimeError("no libproc to watch the memory of agents' Python with") from None
            probe = (
                "import json, os, sys, sysconfig; print(json.dumps({"
                "'base': os.path.realpath(sys.base_prefix), "
                "'cfg': os.path.realpath(os.path.join(sys.prefix, 'pyvenv.cfg')), "
                "'libs': sorted({os.path.realpath(sysconfig.get_path(n)) for n in ('purelib', 'platlib')})}))"
            )
            out = subprocess.run(
                [str(self.python), "-c", probe], capture_output=True, text=True, timeout=60
            )
            if out.returncode:
                raise RuntimeError(f"the sandbox interpreter does not start: {out.stderr.strip()}")
            paths = json.loads(out.stdout)
            paths["bins"] = [b for lib in paths["libs"] if os.path.isdir(b := os.path.join(lib, "sage_wheels", "bin"))]
            self._watch = Path(os.path.realpath(tempfile.mkdtemp(prefix="swarm-watch-")))
            (self._watch / "sitecustomize.py").write_text(WATCH)
            self._paths = paths
            return self._paths

    def _rules(self, folder: Path, shared=(), read_only=()) -> str:
        """The sandbox of one run, handed over as text (there is no profile file for a run to rewrite).
        Reading file contents is refused everywhere and then allowed place by place. `shared`: folders besides its
        own that the run may read and write too (a workspace several agents share); `read_only`: folders it may only
        read (another team's workspace).

        Exec is allowed for Python itself and for Sage's bundled programs (sage_wheels/bin): Sage refuses to
        import unless `access(Singular, X_OK)` succeeds, which the sandbox ties to exec permission. Fork is denied
        unless the Sandbox allows several processes; then a run may fork, and exec only those programs (so
        multiprocessing's workers are more of the same Python, under the same rules), and signal its own processes."""
        p = self._paths
        readable = " ".join(
            f"(subpath {_quote(place)})"
            for place in [
                "/usr/lib", "/usr/share", "/System", "/dev",
                p["base"], *p["libs"], self._watch, os.path.realpath(HOME_TEMPLATE), folder, *shared, *read_only,
            ]
        )  # fmt: skip
        programs = " ".join(f"(subpath {_quote(place)})" for place in [p["base"], *p["bins"]])
        writable = " ".join(f"(subpath {_quote(place)})" for place in [folder, *shared])
        return "\n".join(
            [
                "(version 1)",
                "(allow default)",
                "(deny network*)",
                *(["(deny process-fork)"] if self.processes <= 1 else []),
                "(deny process-exec*)",
                f"(allow process-exec {programs})",
                "(deny signal)",
                "(allow signal (target self))" if self.processes <= 1 else "(allow signal (target pgrp))",
                "(deny mach-lookup)",
                "(deny file-write*)",
                f'(allow file-write* {writable} (literal "/dev/null"))',
                "(deny file-read-data)",
                f'(allow file-read-data (literal "/") (literal {_quote(p["cfg"])}) {readable})',
            ]
        ) + "\n"

    def _footprint(self, pid) -> int:
        """Memory a process holds, in bytes, as Activity Monitor counts it; 0 once it is gone."""
        usage = (ctypes.c_uint64 * 64)()  # rusage_info_v2; field 9 is ri_phys_footprint
        return usage[9] if self._usage(pid, 2, ctypes.byref(usage)) == 0 else 0

    def _members(self, group) -> list[int]:
        """The processes of a run: its process group (a run is started as a session of its own)."""
        if self.processes <= 1:
            return [group]
        pids = (ctypes.c_int * 256)()
        n = self._group(group, ctypes.byref(pids), ctypes.sizeof(pids))  # how many it found
        return [p for p in pids[: max(0, min(n, len(pids)))] if p > 0] or [group]

    # ---- running ----------------------------------------------------------

    def run(self, folder, filename, timeout, shared=(), read_only=()) -> Ran:
        """Run `filename` inside `folder` (its working directory and, with the `shared` folders, the only place it
        can read files of or write; the `read_only` folders it can read too)."""
        try:
            self._resolve()
        except RuntimeError as e:
            return Ran("unavailable", None, "", str(e), 0.0)
        folder = Path(os.path.realpath(folder))
        shared = tuple(Path(os.path.realpath(s)) for s in shared)
        read_only = tuple(Path(os.path.realpath(s)) for s in read_only)
        if self._gate is None:
            return self._run(folder, filename, timeout, shared, read_only)
        with self._gate:
            return self._run(folder, filename, timeout, shared, read_only)

    def _run(self, folder: Path, filename: str, timeout: float, shared=(), read_only=()) -> Ran:
        home = folder / ".home"  # Sage and Maxima keep caches here
        if not home.exists() and HOME_TEMPLATE.is_dir():
            # Small files are copied; big ones (the 58 MB GAP workspace) are symlinked, read-only to the run.
            link_big = lambda src, dst: (
                os.symlink(os.path.realpath(src), dst) if os.path.getsize(src) > 2**20 else shutil.copy2(src, dst)
            )
            shutil.copytree(HOME_TEMPLATE, home, copy_function=link_big)
        home.mkdir(parents=True, exist_ok=True)
        logs = Path(tempfile.mkdtemp(prefix="swarm-run-"))  # what it prints, outside its folder
        # The shell only sets the most a run may write, then becomes sandbox-exec, which becomes Python:
        # one process, so the one that is watched and killed is the agent's.
        # No `-X faulthandler`: its C signal handlers break Sage's cysignals at import. The timeout traceback
        # comes from WATCH, which needs no handlers.
        command = [
            "/bin/sh", "-c", 'ulimit -f "$0" && exec "$@"', str(max(1, self.max_file // 1024)),  # /bin/sh counts KiB
            SANDBOX_EXEC, "-p", self._rules(folder, shared, read_only),
            str(self.python), "-B", "-s", "-u", filename,
        ]  # fmt: skip
        env = {
            **ENV,
            "HOME": str(home),
            "TMPDIR": str(home),
            "PYTHONPATH": str(self._watch),
            "SWARM_TIMEOUT": f"{timeout:g}",
        }
        started, stopped, child = time.monotonic(), "", None
        try:
            with open(logs / "out", "wb") as out, open(logs / "err", "wb") as err:
                child = subprocess.Popen(
                    command, cwd=folder, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                    start_new_session=True,  # its own process group, which holds every process it starts
                )  # fmt: skip
                ticks = 0
                while child.poll() is None and not stopped:
                    members, ticks = self._members(child.pid), ticks + 1
                    if time.monotonic() - started > timeout + GRACE:  # it did not stop itself
                        stopped = "timeout"
                    elif ticks % 25 == 0 and self.max_file > self.max_output and max(
                        (logs / n).stat().st_size for n in ("out", "err")) >= self.max_output:  # fmt: skip
                        stopped = "output"  # files may be bigger than the output, so ulimit doesn't stop it
                    elif sum(map(self._footprint, members)) > self.memory_mb * 2**20:
                        stopped = "memory"
                    elif len(members) > self.processes:
                        stopped = "processes"
                    elif self.stop.is_set():
                        stopped = "stopped"
                    else:
                        time.sleep(0.02)
            if stopped:
                child.kill()
            child.wait()
            self._kill_group(child.pid)  # workers it left behind
            seconds = time.monotonic() - started
            full = max((logs / n).stat().st_size for n in ("out", "err")) >= self.max_output
            stdout, stderr = (self._tidy((logs / n).read_bytes().decode("utf-8", "replace"), folder) for n in ("out", "err"))
        finally:
            if child is not None and child.poll() is None:  # the harness was interrupted
                child.kill()
                self._kill_group(child.pid)
            shutil.rmtree(logs, ignore_errors=True)
        code = child.returncode
        if not stopped and code == 1 and seconds >= timeout and _TIME_UP.search(stderr):
            stopped = "timeout"  # its time was up and it said where it was
        if stopped == "stopped":
            return Ran("stopped", code, stdout, stderr, seconds)
        if stopped == "output":
            return Ran("output", code, stdout, stderr, seconds)
        if stopped == "timeout":
            return Ran("timeout", code, stdout, stderr, seconds, where=self._where(stderr, filename))
        if stopped in ("memory", "processes"):
            return Ran(stopped, code, stdout, stderr, seconds)
        if code == -signal.SIGXFSZ or (code and "[Errno 27] File too large" in stderr):  # Python ignores SIGXFSZ
            return Ran("file", code, stdout, stderr, seconds)
        if full:
            return Ran("output", code, stdout, stderr, seconds)
        return Ran("ok" if code == 0 else "error", code, stdout, stderr, seconds)

    @staticmethod
    def _kill_group(group):
        try:
            os.killpg(group, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass

    @staticmethod
    def _tidy(text, folder: Path) -> str:
        """Tracebacks without this machine's folders: the agent's file is its own name, and a library file is
        its path inside the library."""
        return _LIBRARY.sub("", text.replace(f"{folder}/", ""))

    @staticmethod
    def _where(stderr, filename) -> str:
        """Where in the agent's file a timed-out run was: 'line 5 (in f), called from line 9'."""
        frames = [(line, name) for f, line, name in _FRAME.findall(stderr) if Path(f).name == filename]
        parts = [f"line {line}" + ("" if name == "<module>" else f" (in {name})") for line, name in frames[:4]]
        return ", called from ".join(parts)

    def build_home_template(self):
        """Sage's caches, built once (setup_sandbox.sh) and seeded into each agent's home: the lazy-import
        cache (~20 s on a first `import sage.all`) and libgap's saved workspace, which Sage writes on first use
        and cannot inside the sandbox. Sage names the workspace by a hash that includes a subprocess's output,
        so inside the sandbox (no subprocesses) the name differs: the file built outside is renamed to it."""
        self._resolve()
        shutil.rmtree(HOME_TEMPLATE, ignore_errors=True)
        HOME_TEMPLATE.mkdir(parents=True)
        build = "from sage.all import *; print(libgap.SymmetricGroup(4).Size())"
        env = {**ENV, "HOME": str(HOME_TEMPLATE)}
        out = subprocess.run([str(self.python), "-c", build], env=env, capture_output=True, text=True, timeout=600)
        if out.returncode:
            raise RuntimeError(f"building Sage's caches failed: {out.stderr.strip()[-2000:]}")
        gap = HOME_TEMPLATE / ".sage" / "gap"
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "name.py").write_text(
                "import os\nfrom sage.interfaces.gap_workspace import gap_workspace_file\n"
                "print(os.path.basename(gap_workspace_file('libgap')))"
            )
            ran = self.run(Path(tmp), "name.py", timeout=120)
        if ran.status != "ok":
            raise RuntimeError(f"cannot name the workspace inside the sandbox: {ran.stderr.strip()[-2000:]}")
        inside = ran.stdout.strip()
        for f in gap.glob("libgap-workspace-*"):
            if f.name != inside:
                f.rename(gap / inside)

    def leaks(self, folder) -> list[str]:
        """The ways out of the sandbox a probe file found: none, if the sandbox holds."""
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        outside = Path(tempfile.gettempdir()) / f"swarm-probe-{os.getpid()}"
        (folder / "probe.py").write_text(
            PROBE.format(secret=str(ROOT / "pyproject.toml"), home=str(Path.home()), outside=str(outside))
        )
        ran = self.run(folder, "probe.py", timeout=30)
        if ran.status != "ok":
            return [f"the probe did not run ({ran.status}): {ran.stderr.strip()[-500:]}"]
        found = ran.stdout.split()
        return [w for w in found if w != "fork"] if self.processes > 1 else found

    def close(self):
        if self._watch is not None:
            shutil.rmtree(self._watch, ignore_errors=True)
