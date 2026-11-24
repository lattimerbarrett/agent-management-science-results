"""The sandbox for agents' Python on Linux (a GPU server): what a file can see, and what it can do.

On macOS mathswarm/python.py hands a run to `sandbox-exec` with a list of rules. Linux has no such thing, so
here a run gets two walls, and each of the ways out that `python.PROBE` tries is closed by one of them:

    what it can see    bubblewrap (`bwrap`) starts the run in namespaces of its own, on a file system that is
                       made for it and holds nothing of this machine but Python, its libraries and the system's
                       own shared libraries, all read-only, and the folder the file runs in. There is no
                       home directory, no repo, no /etc, no /proc, no network device but a loopback, and no
                       other process to be seen.
    what it can do     a seccomp filter refuses the system calls that reach past those walls or start
                       something: sockets, new processes (threads are let through), signals to others,
                       tracing, mounting, and new namespaces.

A file's folder is `/work/desk` in every run, so a traceback reads the same wherever the lab runs. It is made in
memory for the run and is gone with it: the file is put there read-only, what the file writes there may come to
`DESK_BYTES` in all, and nothing a file writes reaches this machine's disk but what it prints. Python is the
interpreter this repo runs on, mounted at `/python`, and its libraries (sympy, numpy) at `/venv/site-packages`.
Among those libraries a few small files say where on this machine they were installed from (the links an
editable install leaves, each package's `direct_url.json`): a run finds an empty file in the place of each.

Whether the sandbox got as far as starting Python is said by bubblewrap itself, on a pipe the file has no part in
(`started`): a sandbox that did not start is the lab's trouble and stops it, and nothing a file prints can pass
for that.

Two things about the machine it runs on:
  - Ubuntu 24.04 keeps a program without a profile from using a user namespace, which bubblewrap needs: it stops
    with "loopback: Failed RTM_NEWADDR: Operation not permitted". On a machine that is rented for one job,
    `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` lifts that (`ready` says so when it is why).
  - Ubuntu's bubblewrap (0.9.0) can be made to write outside the sandbox while it sets one up, if it is told to
    make something under a folder that untrusted code wrote to before (CVE-2026-87766). Nothing is made under a
    file's folder here: a run's folder is new, holds only its file, and is the last thing mounted. Keep it so.

The memory a run holds is read from /proc, from outside, as python.py reads it from the kernel on macOS: the
watch and the limits are python.py's, and are the same on both.

`Python`, at the foot of this file, is `python.Python` with this sandbox in the place of macOS's. python.py is
not touched for it: it is part of the harness's version, and the Mac's. What a run is and what an agent is told
of it are written there; here `_run` is that one again with the differences a test names and holds it to, so a
change there that is not made here fails a test on any machine.

Nothing here is tried on macOS but the filter's bytes, the command line and that run loop's text
(tests/test_linux.py). `lab doctor` and tests/test_python.py run real files through it on a Linux machine, and
try the ways out.
"""
from __future__ import annotations

import glob
import hashlib
import os
import platform
import shutil
import struct
import subprocess
import sys
import sysconfig
import tempfile
import threading
import time
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path

from . import python as mac
from .python import ENV, FILE, GRACE, KEPT, MAX_PRINTED, _TIME_UP, Ran, answered, middle, tidy, where

VERSION = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]      # of this sandbox: kept with a run's machine

BWRAP = "/usr/bin/bwrap"
DESK = "/work/desk"       # the folder a file runs in, as the file sees it
DESK_BYTES = 256 * 2**20  # what a run may keep in that folder, all its files together
LOADERS = ("/lib64/ld-linux-x86-64.so.2", "/lib/ld-linux-aarch64.so.1")      # what starts a program, where a program expects it
PYTHON = "/python"        # this interpreter's own folder (`sys.base_prefix`), as the file sees it
LIBRARIES = "/venv"       # what is installed beside this repo: site-packages, under this
WATCH = "/watch"          # the folder that holds what stops a run when its time is up (python.WATCH)

# ---------------------------------------------------------------- the seccomp filter

# System call numbers, by machine. A call that a machine does not have is left out there. Calls added to Linux
# since 2019 have one number on every machine.
NEWER = {"open_tree": 428, "move_mount": 429, "fsopen": 430, "fsconfig": 431, "fsmount": 432, "fspick": 433,
         "pidfd_getfd": 438, "process_madvise": 440, "mount_setattr": 442}
CALLS = {
    "x86_64": {"socket": 41, "socketpair": 53, "fork": 57, "vfork": 58, "clone": 56, "clone3": 435, "kill": 62, "tkill": 200,
               "rt_sigqueueinfo": 129, "rt_tgsigqueueinfo": 297, "pidfd_open": 434, "pidfd_send_signal": 424, "ptrace": 101,
               "process_vm_readv": 310, "process_vm_writev": 311, "unshare": 272, "setns": 308, "mount": 165, "umount2": 166,
               "pivot_root": 155, "chroot": 161, "bpf": 321, "perf_event_open": 298, "keyctl": 250, "add_key": 248,
               "request_key": 249, "io_uring_setup": 425, "io_uring_enter": 426, "io_uring_register": 427, "userfaultfd": 323,
               "open_by_handle_at": 304, "name_to_handle_at": 303, "execveat": 322, "kcmp": 312, **NEWER},
    "aarch64": {"socket": 198, "socketpair": 199, "clone": 220, "clone3": 435, "kill": 129, "tkill": 130,
                "rt_sigqueueinfo": 138, "rt_tgsigqueueinfo": 240, "pidfd_open": 434, "pidfd_send_signal": 424, "ptrace": 117,
                "process_vm_readv": 270, "process_vm_writev": 271, "unshare": 97, "setns": 268, "mount": 40, "umount2": 39,
                "pivot_root": 41, "chroot": 51, "bpf": 280, "perf_event_open": 241, "keyctl": 219, "add_key": 217,
                "request_key": 218, "io_uring_setup": 425, "io_uring_enter": 426, "io_uring_register": 427, "userfaultfd": 282,
                "open_by_handle_at": 265, "name_to_handle_at": 264, "execveat": 281, "kcmp": 272, **NEWER},
}
ARCH = {"x86_64": 0xC000003E, "aarch64": 0xC00000B7}          # AUDIT_ARCH_*: how the kernel names the machine a call was made for
# The second and third lines are refused by other walls already (a run has no capabilities and can get no handle
# on another process): they are refused here too, so that this wall does not lean on those.
REFUSED = ("socket", "socketpair", "fork", "vfork", "kill", "tkill", "rt_sigqueueinfo", "rt_tgsigqueueinfo", "pidfd_open",
           "pidfd_send_signal", "ptrace", "process_vm_readv", "process_vm_writev", "unshare", "setns", "mount", "umount2",
           "pivot_root", "chroot", "bpf", "perf_event_open", "keyctl", "add_key", "request_key", "io_uring_setup",
           "io_uring_enter", "io_uring_register", "userfaultfd", "open_by_handle_at", "name_to_handle_at",
           "open_tree", "move_mount", "fsopen", "fsconfig", "fsmount", "fspick", "mount_setattr",
           "pidfd_getfd", "process_madvise", "kcmp", "execveat")

LOAD, EQUAL, AT_LEAST, ANY_BIT, RETURN = 0x20, 0x15, 0x35, 0x45, 0x06     # BPF: load a word, jump if ==, if >=, if any bit, return
ALLOW, KILL, ERRNO = 0x7FFF0000, 0x80000000, 0x00050000                   # SECCOMP_RET_ALLOW, _KILL_PROCESS, _ERRNO
EPERM, ENOSYS = 1, 38
NUMBER, MACHINE, FIRST_ARGUMENT = 0, 4, 16                                # where `struct seccomp_data` keeps each
CLONE_THREAD = 0x00010000
X32 = 0x40000000                                                          # x86_64's second set of call numbers


def machine() -> str:
    """This machine as the tables above name it."""
    name = platform.machine().lower()
    return {"amd64": "x86_64", "arm64": "aarch64"}.get(name, name)


def instruction(code: int, yes: int, no: int, value: int) -> bytes:
    return struct.pack("<HBBI", code, yes, no, value)


def filter_for(on: str | None = None) -> bytes:
    """The seccomp filter of a run, as the kernel reads it (an array of `struct sock_filter`), for machine `on`.

    A call made for another machine than this one kills the run. Each of `REFUSED` fails with "Operation not
    permitted", which Python raises as an error the file can see. `clone` is let through only when it starts
    a thread; `clone3` hides how it is used, so it fails with "Function not implemented", on which the C
    library falls back to `clone`. Everything else goes ahead: what a file may read and write is bubblewrap's
    wall, not this one."""
    on = on or machine()
    if on not in CALLS:
        raise RuntimeError(f"no seccomp filter for a {on} machine (x86_64 and aarch64 have one)")
    calls = CALLS[on]
    out = [instruction(LOAD, 0, 0, MACHINE), instruction(EQUAL, 1, 0, ARCH[on]), instruction(RETURN, 0, 0, KILL),
           instruction(LOAD, 0, 0, NUMBER)]
    if on == "x86_64":
        out += [instruction(AT_LEAST, 0, 1, X32), instruction(RETURN, 0, 0, ERRNO | EPERM)]
    for name in REFUSED:
        if name in calls:
            out += [instruction(EQUAL, 0, 1, calls[name]), instruction(RETURN, 0, 0, ERRNO | EPERM)]
    out += [instruction(EQUAL, 0, 1, calls["clone3"]), instruction(RETURN, 0, 0, ERRNO | ENOSYS)]
    out += [instruction(EQUAL, 0, 4, calls["clone"]), instruction(LOAD, 0, 0, FIRST_ARGUMENT),      # its flags
            instruction(ANY_BIT, 0, 1, CLONE_THREAD), instruction(RETURN, 0, 0, ALLOW), instruction(RETURN, 0, 0, ERRNO | EPERM)]
    out += [instruction(RETURN, 0, 0, ALLOW)]
    return b"".join(out)


# ---------------------------------------------------------------- the file system of a run

@dataclass(frozen=True)
class Cage:
    """How one run is started: the command, the file's folder as the file sees it, what its environment says of
    where Python's libraries are, and the open files the command needs handed down."""
    command: list[str]
    desk: str
    path: str
    fds: tuple[int, ...] = ()        # handed to the command, and closed here once it is started
    status: int | None = None        # where bubblewrap says how far it got (`started` reads it and closes it)


def interpreter() -> str:
    """This interpreter's own program, not a virtual environment's link to it."""
    return os.path.realpath(sys.executable)


def system_libraries() -> list[str]:
    """What puts the system's shared libraries where a program looks for them, read-only. On Debian and Ubuntu
    they are in one folder a kind of processor (/usr/lib/x86_64-linux-gnu), and that folder is all a run is
    given of /usr/lib, with /lib and the loader pointing into it as they do on the machine. Laid out otherwise,
    a machine gives all of /usr/lib and /usr/lib64."""
    out, shared = [], f"/usr/lib/{sysconfig.get_config_var('MULTIARCH') or machine() + '-linux-gnu'}"
    if os.path.isdir(shared):
        out += ["--ro-bind", shared, shared, "--symlink", "usr/lib", "/lib"]
        for loader in LOADERS:
            if os.path.exists(loader):
                out += ["--symlink", os.path.realpath(loader), loader]
    else:
        for folder in ("/usr/lib", "/usr/lib64"):
            if os.path.isdir(folder):
                out += ["--ro-bind", folder, folder]
        for name in ("/lib", "/lib64"):
            if os.path.islink(name):
                out += ["--symlink", os.readlink(name), name]
            elif os.path.isdir(name):
                out += ["--ro-bind", name, name]
    if os.path.exists("/etc/ld.so.cache"):                     # the list of those libraries, so that none is searched for
        out += ["--ro-bind", "/etc/ld.so.cache", "/etc/ld.so.cache"]
    return out


def telltales(folder: str) -> list[str]:
    """The files among Python's libraries that say where on this machine something was installed from: the links
    an editable install leaves (this repo is installed that way) and each package's note of where it came from.
    Python inside the sandbox needs none of them. Paths from `folder`."""
    found = [*glob.glob(f"{folder}/*.pth"), *glob.glob(f"{folder}/__editable__*"), *glob.glob(f"{folder}/*.dist-info/direct_url.json")]
    return sorted(os.path.relpath(path, folder) for path in found if os.path.isfile(path))


def caged(desk: Path, watch: Path, filter_file: Path, arguments: list[str], file: str | None = None) -> Cage:
    """The command that runs Python on `arguments` inside the sandbox. `file` is the agent's file in `desk`, which
    is put into the run's folder read-only; `watch` is the folder of python.WATCH; `filter_file` holds
    `filter_for()`. Nothing of this machine is given to write to."""
    base = os.path.realpath(sys.base_prefix)
    program = interpreter()
    if not program.startswith(base + os.sep):
        raise RuntimeError(f"Python's program {program} is not under its own folder {base}")
    libraries = sorted({os.path.realpath(sysconfig.get_path(name)) for name in ("purelib", "platlib")})
    command = [BWRAP, "--unshare-all", "--die-with-parent", "--new-session", "--cap-drop", "ALL", "--hostname", "desk",
               *system_libraries(), "--ro-bind", base, PYTHON]
    # An empty file of the lab's own stands in the place of each telltale. Not /dev/null: bubblewrap binds without
    # devices, and a device that may not be used cannot be opened at all, where a file was to be found empty
    # (seen on the first Linux machine this ran on, 2026-10-11: a test that reads them was refused).
    nothing = filter_file.with_name(filter_file.name + ".nothing")
    try:                                                       # made by whoever is first, in one step: files are run on
        os.close(os.open(nothing, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o444))     # many threads, and two that both found
    except FileExistsError:                                    # none must not both try to write one that may not be written
        pass
    inside = []
    for number, folder in enumerate(libraries):                # one folder on every machine this has run on; two are kept apart
        at = f"{LIBRARIES}{number or ''}/site-packages"
        command += ["--ro-bind", folder, at]
        for name in telltales(folder):
            command += ["--ro-bind", str(nothing), f"{at}/{name}"]
        inside.append(at)
    # /work can be passed through and not listed. The run's folder is memory, of a size, with the file in it. /dev
    # and / are read-only once everything is in place (a device, like /dev/null, takes what is written to it all
    # the same). Nothing is made beneath a folder that a file could have written to before: see the top of this file.
    command += ["--ro-bind", str(watch), WATCH, "--dev", "/dev", "--remount-ro", "/dev",
                "--perms", "0111", "--dir", "/work", "--size", str(DESK_BYTES), "--tmpfs", DESK]
    if file is not None:
        command += ["--ro-bind", str(desk / file), f"{DESK}/{file}"]
    seccomp = os.open(filter_file, os.O_RDONLY)
    status, says = os.pipe()
    command += ["--remount-ro", "/", "--chdir", DESK, "--seccomp", str(seccomp), "--json-status-fd", str(says),
                PYTHON + program[len(base):], *arguments]
    return Cage(command, DESK, os.pathsep.join([WATCH, *inside]), (seccomp, says), status)


def started(status: int) -> bool:
    """Whether the sandbox got as far as starting Python, read once the run is over. bubblewrap writes a line
    with the command's exit code only when it did start the command; when it could not set the sandbox up
    (Ubuntu's restriction is back, a folder is gone) it writes none. The pipe is the sandbox's own: nothing the
    file prints or exits with can make a run that started look like one that did not."""
    said = b""
    try:
        os.set_blocking(status, False)
        while (more := os.read(status, 4096)):
            said += more
    except BlockingIOError:                                    # somebody still holds the other end: nothing more is coming in time
        pass
    finally:
        os.close(status)
    return b'"exit-code"' in said


# ---------------------------------------------------------------- is there a sandbox here, and what a run holds

_checked = threading.Lock()
_why: list[str | None] = []           # why files cannot be run here, once it has been found out (None: they can)


def ready() -> None:
    """Raise RuntimeError, saying why, if files cannot be run in the sandbox on this machine. Found out once: by
    starting the sandbox on a Python that does nothing."""
    with _checked:
        if not _why:
            _why.append(_try())
        if _why[0] is not None:
            raise RuntimeError(_why[0])


def forget() -> None:
    """Have `ready` find out again whether files can be run here (the sandbox stopped starting)."""
    with _checked:
        _why.clear()


def _try() -> str | None:
    if not os.access(BWRAP, os.X_OK):
        return f"no {BWRAP} to run agents' Python in (sudo apt-get install -y bubblewrap)"
    if machine() not in CALLS:
        return f"no seccomp filter for a {machine()} machine"
    if not os.path.exists(f"/proc/self/task/{threading.get_native_id()}/children"):
        return "no list of a process's children in /proc to watch the memory of agents' Python with (CONFIG_PROC_CHILDREN)"
    with tempfile.TemporaryDirectory(prefix="mathswarm-try-") as folder:
        desk, watch, filter_file = Path(folder, "desk"), Path(folder, "watch"), Path(folder, "filter")
        desk.mkdir()
        watch.mkdir()
        filter_file.write_bytes(filter_for())
        try:
            cage = caged(desk, watch, filter_file, ["-B", "-s", "-c", "import numpy, sympy"])
        except RuntimeError as problem:
            return str(problem)
        try:
            tried = subprocess.run(cage.command, cwd=desk, env={"PYTHONPATH": cage.path, "HOME": cage.desk}, pass_fds=cage.fds,
                                   stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.SubprocessError) as problem:
            os.close(cage.status)
            return f"the sandbox ({BWRAP}) could not be started: {problem}"
        finally:
            for fd in cage.fds:
                os.close(fd)
        began = started(cage.status)
    if tried.returncode or not began:
        said = " ".join((tried.stderr or tried.stdout).split())[-400:]
        refused = any(sign in said for sign in ("RTM_NEWADDR", "uid map", "Creating new namespace", "not permitted", "Permission denied"))
        hint = (" (Ubuntu 24.04 keeps a program from using a user namespace: sudo sysctl -w "
                "kernel.apparmor_restrict_unprivileged_userns=0)" if refused and said.startswith("bwrap: ") else "")
        return f"the sandbox ({BWRAP}) does not start Python here: {said or f'code {tried.returncode}'}{hint}"
    return None


PAGE = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096


def footprint(pid: int) -> int:
    """The memory a run holds, in bytes: of the sandbox's process and every process under it, what is in memory
    and is the process's own (not a file's, like Python's libraries). 0 once they are gone."""
    held, left = 0, [pid]
    while left:
        at = left.pop()
        try:
            with open(f"/proc/{at}/statm") as f:
                _, resident, shared, *_ = f.read().split()
            held += (int(resident) - int(shared)) * PAGE
            with open(f"/proc/{at}/task/{at}/children") as f:
                left += [int(child) for child in f.read().split()]
        except (OSError, ValueError):
            continue
    return max(held, 0)


# ---------------------------------------------------------------- running a file

class Python(mac.Python):
    """`python.Python` on Linux: the same limits, the same watch from outside, the same words to an agent and the
    same cache of what files did, with this file's sandbox in the place of macOS's."""

    def __init__(self, *args, **settings):
        super().__init__(*args, **settings)
        self._filter: Path | None = None                       # the file that holds a run's seccomp filter
        if self._db is not None:                               # a rented machine copies this file whole every few minutes:
            self._db.execute("pragma busy_timeout = 120000")   # a write waits for that

    _began = staticmethod(started)

    def _resolve(self) -> str:
        with self._lock:
            if self._setup is None:
                ready()                                        # says why, if files cannot be run in the sandbox here
                self._work = Path(os.path.realpath(tempfile.mkdtemp(prefix="mathswarm-python-")))
                self._watch = Path(os.path.realpath(tempfile.mkdtemp(prefix="mathswarm-watch-")))
                (self._watch / "sitecustomize.py").write_text(mac.WATCH, encoding="utf-8")
                self._filter = self._work / "seccomp"
                self._filter.write_bytes(filter_for())
                # what a file did is kept apart for each sandbox it was run in
                self._setup = f"{sys.version}\nsympy {version('sympy')}\nnumpy {version('numpy')}\nlinux {VERSION}"
            return self._setup

    def _footprint(self, pid: int) -> int:
        return footprint(pid)

    def _run(self, code: str) -> Ran:
        folder = Path(tempfile.mkdtemp(dir=self._work))
        desk = folder / "desk"                                 # where the file runs, and all it can write to
        desk.mkdir()
        (desk / FILE).write_text(code, encoding="utf-8")
        # The shell only sets the most a run may write and then becomes the sandbox, which becomes Python: one
        # process, so the one that is watched and killed is the agent's. (Here the sandbox stays, with Python
        # under it: killing it takes Python with it, and the memory of both is what is watched.)
        cage = caged(desk, self._watch, self._filter, ["-B", "-s", "-u", "-X", "faulthandler", FILE], FILE)
        command = ["/bin/sh", "-c", 'ulimit -f "$0" && exec "$@"', str(MAX_PRINTED // 512), *cage.command]
        env = {**ENV, "HOME": cage.desk, "TMPDIR": cage.desk, "PYTHONPATH": cage.path, "MATHSWARM_TIMEOUT": f"{self.timeout:g}"}
        started, stopped, child, status = time.monotonic(), "", None, cage.status
        try:
            with open(folder / "printed", "wb") as out, open(folder / "said", "wb") as err:
                try:
                    child = subprocess.Popen(command, cwd=desk, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                             pass_fds=cage.fds)
                finally:
                    for fd in cage.fds:
                        os.close(fd)
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
            printed, said = (tidy((folder / name).read_bytes().decode("utf-8", "replace"), cage.desk) for name in ("printed", "said"))
            began, status = self._began(status), None
            if not began and not stopped:                      # the sandbox itself did not start: not something a file did,
                forget()                                       # and no agent is to be told it. The run of the lab stops
                raise RuntimeError(f"the sandbox for agents' Python did not start: {said.strip()[:300] or 'it said nothing'}")
            if not stopped and child.returncode == 1 and seconds >= self.timeout and _TIME_UP.search(said):
                stopped = "timeout"                            # its time was up, and it said where it was
            answer = answered(printed)
            printed, said = middle(printed, KEPT), middle(said, KEPT)
        finally:
            if child is not None and child.poll() is None:     # the lab was interrupted: the file does not outlive it
                child.kill()
            if status is not None:
                os.close(status)
            shutil.rmtree(folder, ignore_errors=True)
        if stopped == "timeout":
            return Ran("timeout", printed, f"no result after {self.timeout:g} seconds" + (f"; it was {at}" if (at := where(said)) else ""), seconds)
        if stopped == "memory":
            return Ran("memory", printed, f"it held more than {self.memory_mb:,} MB of memory", seconds)
        if full:
            return Ran("error", printed, f"it printed more than {MAX_PRINTED // 2**20} MB and was stopped: print less", seconds)
        if child.returncode:
            ended = 128 - child.returncode if child.returncode > 128 else child.returncode      # as bubblewrap passes on a signal
            crashed = f"Python crashed (signal {-ended})" if ended < 0 else f"Python stopped with code {ended}"
            return Ran("error", printed, said.strip() or crashed, seconds)
        return Ran("ok", printed, said.strip(), seconds, answer=answer)
