"""The class that runs agents' Python on this kind of machine: python.py's on a Mac (`sandbox-exec`), linux.py's on
Linux (bubblewrap and a seccomp filter). Whoever runs files takes `Python` from here.

python.py is part of the harness's version and is the Mac's: it was not touched for Linux, so nothing a run on a
Mac is told or run with changed when Linux was added. What an agent is told of a run is written there, once;
linux.py's run loop is that one with a handful of named differences, and a test holds it to them
(tests/test_linux.py)."""
import sys

if sys.platform.startswith("linux"):
    from .linux import Python
else:
    from .python import Python

__all__ = ["Python"]
