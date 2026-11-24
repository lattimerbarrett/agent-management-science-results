"""Run ONE model job at a time on this Mac, with memory guards.

    swarm-run [--mem-gb N] [--need-gb G] [--kill-gb K] -- <command...>
    python -m swarm_engine.ml_run ... -- <command...>

Every process that loads a model runs under this wrapper (`Engine` refuses to load one otherwise). Scripts call
`swarm_engine.under_lock()` first thing, which re-runs them through here, so you rarely type this yourself.

It takes the SAME lock file as the `scripts/ml_run.py` of the research repos on this Mac, so model jobs from all
of them queue behind each other instead of overlapping. The rule exists because on 2026-09-25 more than ten
concurrent MLX processes exhausted this machine's 48 GB of unified memory and caused a watchdog reset.

  --mem-gb N        memory budget for the job, passed to it as SWARM_MEM_GB (default 20).
  --need-gb G       wait to start until at least G GB of memory is available (default 12).
  --kill-gb K       kill the job if available memory stays below K GB for three checks 2 s apart (default 5).
Nothing stops a job for running long: it ends when it finishes, when it is told to stop, or when the machine runs
out of memory. The job's exit code is passed on (137 if killed by the memory watchdog, 130 if interrupted).
Starts and ends are logged to ~/.swarm_engine/ml_run.log.
"""
import fcntl
import os
import signal
import subprocess
import sys
import time

from .machine import LOCK, available_gb

LOG = os.path.expanduser("~/.swarm_engine/ml_run.log")
DEFAULTS = {"--mem-gb": 20.0, "--need-gb": 12.0, "--kill-gb": 5.0}


def note(msg: str):
    print(f"[ml_run] {msg}", file=sys.stderr, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except OSError:
        pass


def kill(child):
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(child.pid, sig)
        except OSError:
            pass
        time.sleep(5)
    child.wait()


def main():
    args, opts = sys.argv[1:], dict(DEFAULTS)
    while args and args[0] in opts:
        opts[args[0]] = float(args[1])
        args = args[2:]
    if args[:1] == ["--"]:
        args = args[1:]
    elif args and args[0].startswith("--"):
        sys.exit(f"[ml_run] unknown option {args[0]}\n{__doc__}")
    if not args:
        sys.exit(__doc__)
    mem_gb, need, kill_at = (opts[k] for k in DEFAULTS)

    # Any way of being told to stop ends the job and frees the lock. A plain `kill`, a closed terminal, and
    # ctrl-c all count; so does an interrupt sent to a wrapper started with `&` from a script, which a shell
    # starts with interrupts switched off. (A test server once held the lock for 36 minutes that way.)
    def stop(_signal, _frame):
        raise KeyboardInterrupt

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, stop)

    waited = time.time()
    lock = os.open(LOCK, os.O_CREAT | os.O_RDWR)
    try:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("[ml_run] another model job holds the machine lock; waiting for it to finish", file=sys.stderr, flush=True)
            fcntl.flock(lock, fcntl.LOCK_EX)   # blocks until the single machine-wide slot is free
        while available_gb() < need:
            print(f"[ml_run] waiting for memory ({available_gb():.1f} GB available, need {need:g})", file=sys.stderr, flush=True)
            time.sleep(10)
    except KeyboardInterrupt:
        sys.exit(130)                          # told to stop while still queueing: nothing was started
    cmd = " ".join(args)[:300]
    note(f"START waited={time.time() - waited:.0f}s avail={available_gb():.1f}GB cap={mem_gb:g}GB cmd={cmd}")
    env = dict(os.environ, SWARM_LOCKED="1", SWARM_MEM_GB=str(mem_gb), PYTHONUNBUFFERED="1")
    started = time.time()
    child = subprocess.Popen(args, env=env, start_new_session=True)
    low = 0
    try:
        while child.poll() is None:
            time.sleep(2)
            available = available_gb()
            low = low + 1 if available < kill_at else 0
            if low >= 3:
                note(f"WATCHDOG {available:.1f} GB available < {kill_at:g} GB; killing cmd={cmd}")
                kill(child)
                sys.exit(137)
    except KeyboardInterrupt:
        note(f"INTERRUPTED; killing cmd={cmd}")
        kill(child)
        sys.exit(130)
    note(f"END rc={child.returncode} dur={time.time() - started:.0f}s cmd={cmd}")
    sys.exit(child.returncode)


if __name__ == "__main__":
    main()
