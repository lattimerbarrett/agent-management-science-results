"""This machine's one hard rule: one model job at a time (Apple M5 Pro, 48 GB of unified memory).

`swarm_engine.ml_run` is the wrapper that enforces it: a machine-wide lock shared with every research repo on
this Mac, a memory budget, and a watchdog. A script that loads a model calls `under_lock()` first thing, which
re-runs the script through that wrapper, so `python my_script.py` just works and queues politely.

The lock file and the environment names are the ones the repos already use (`scripts/ml_run.py` in
swarm_experiment, swarm_explore, affect_explore, memory_explore), so jobs started from any of them and jobs
started from here queue behind each other.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import threading
import time

LOCK = "/tmp/memory_explore_ml.lock"
LOCKED_NAMES = ("SWARM_LOCKED", "AFFLAB_LOCKED")     # what each repo's wrapper sets on the job it runs


def locked() -> bool:
    return any(os.environ.get(name) == "1" for name in LOCKED_NAMES)


def under_lock(mem_gb: float = 20):
    """Make sure this process runs under the machine-wide model lock, re-running it through the wrapper if not."""
    if locked():
        return
    spec = getattr(sys.modules.get("__main__"), "__spec__", None)
    if spec is not None and spec.name:            # started as `python -m package.module`: start it that way again
        again = [sys.executable, "-m", spec.name.removesuffix(".__main__"), *sys.argv[1:]]
    else:
        again = [sys.executable, *sys.argv]
    command = [sys.executable, "-m", "swarm_engine.ml_run", "--mem-gb", str(mem_gb), "--", *again]
    os.execv(sys.executable, command)


def require_lock():
    if not locked():
        raise RuntimeError(
            "A model may only be loaded under the machine-wide model lock (one model job at a time on this Mac).\n"
            "Call swarm_engine.under_lock() at the start of the script, or run it through the wrapper:\n"
            "  swarm-run -- python <your_script.py> ...")


def budget_gb() -> float:
    """The memory this job may use, as the wrapper was told (default 20 of this laptop's 48 GB)."""
    return float(os.environ.get("SWARM_MEM_GB") or os.environ.get("AFFLAB_MEM_GB") or 20)


def cache_gb() -> float:
    """How much freed memory MLX may keep for reuse instead of handing it back."""
    return float(os.environ.get("SWARM_CACHE_GB", "4"))


def limit_memory():
    """Cap MLX at the wrapper's budget so one job cannot exhaust unified memory."""
    import mlx.core as mx

    gb = budget_gb()
    mx.set_memory_limit(int(gb * 2**30))
    mx.set_wired_limit(int(min(gb, 16) * 2**30))
    mx.set_cache_limit(int(cache_gb() * 2**30))


def available_gb() -> float:
    """Free + inactive + speculative + purgeable pages, in GB. Unlike kern.memorystatus_level, this follows
    MLX / Metal buffers. On Linux (a GPU server): what the kernel says is available to a new program."""
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/meminfo") as f:
                return int(re.search(r"MemAvailable:\s+(\d+) kB", f.read()).group(1)) / 2**20
        except (OSError, AttributeError):
            return 99.0
    try:
        out = subprocess.check_output(["vm_stat"]).decode()
        page = int(re.search(r"page size of (\d+)", out).group(1))
        pages = sum(int(re.search(key + r":\s+(\d+)", out).group(1))
                    for key in ("Pages free", "Pages inactive", "Pages speculative", "Pages purgeable"))
        return pages * page / 2**30
    except Exception:
        return 99.0


def guard(proc: subprocess.Popen, floor_gb: float = 7.0, on_kill=None) -> threading.Thread:
    """Kill `proc` if available memory falls under `floor_gb`. For anything that manages its own memory (a model
    server): the wrapper's watchdog only acts at 5 GB, after six seconds, and takes the whole job with it."""

    def watch():
        while proc.poll() is None:
            if available_gb() < floor_gb:
                proc.kill()
                if on_kill:
                    on_kill(f"available memory fell under {floor_gb:g} GB")
                return
            time.sleep(0.5)

    thread = threading.Thread(target=watch, daemon=True)
    thread.start()
    return thread
