"""Single-file Python scratchpad: handlers for the tools defined in tools.yaml.

The model gets one file (scratchpad.py) that it can read, overwrite, edit, and run. Each run is a fresh
Python process in the sandbox (sandbox.py); the file, and anything a run writes next to it, persists
across turns.

Usage:
    pad = Scratchpad("runs/x/agents/agent_0", Sandbox())
    box = Toolbox(pad)
    resp = client.messages.create(model=..., tools=box.tools, messages=msgs, max_tokens=...)
    results = [box.handle(b) for b in resp.content if b.type == "tool_use"]
"""

import difflib
import hashlib
from pathlib import Path

from sandbox import Sandbox
from toolkit import ToolSet

FILENAME = "scratchpad.py"  # tools.yaml hardcodes this name in its descriptions


class Scratchpad(ToolSet):
    TOOLS_FILE = "tools.yaml"

    def __init__(self, workdir, sandbox: Sandbox, max_output_chars=20_000, max_seconds=None):
        """`max_seconds`: the longest run a call may ask for (default MAX_SECONDS, read at each call)."""
        self.max_seconds = max_seconds
        self.dir = Path(workdir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / FILENAME
        self.path.touch(exist_ok=True)
        self.sandbox = sandbox
        self.max_output = max_output_chars
        # An empty file counts as "seen"; a pre-existing non-empty one must be read first.
        self._seen = self._hash() if not self._text() else None

    # ---- helpers ----------------------------------------------------------

    def _text(self):
        return self.path.read_text()

    def _hash(self, text=None):
        return hashlib.sha256((self._text() if text is None else text).encode()).hexdigest()

    def _stale(self):
        return self._hash() != self._seen

    def _clip(self, s):
        if len(s) <= self.max_output:
            return s
        half = self.max_output // 2
        return f"{s[:half]}\n... [{len(s) - 2 * half} chars truncated] ...\n{s[-half:]}"

    _STALE_MSG = f"Rejected: {FILENAME} has changed since you last read it. Call read_scratchpad first."

    # ---- tools (method names must match tool names in tools.yaml) ---------

    def read_scratchpad(self, start_line=1, end_line=None):
        text = self._text()
        self._seen = self._hash(text)
        lines = text.splitlines()
        if not lines:
            return f"({FILENAME} is empty)", False
        if start_line > len(lines):
            return f"start_line {start_line} is past the end of the file ({len(lines)} lines).", True
        end = min(end_line or len(lines), len(lines))
        body = "\n".join(f"{i:>6}\t{lines[i - 1]}" for i in range(start_line, end + 1))
        return f"{body}\n\n({len(lines)} lines total)", False

    def write_scratchpad(self, content):
        if self._stale():
            return self._STALE_MSG, True
        self.path.write_text(content)
        self._seen = self._hash(content)
        return f"Wrote {FILENAME} ({len(content.splitlines())} lines).", False

    def edit_scratchpad(self, old_string, new_string, replace_all=False):
        if self._stale():
            return self._STALE_MSG, True
        if old_string == new_string:
            return "Rejected: old_string and new_string are identical.", True
        if not old_string:
            return "Rejected: old_string is empty. Use write_scratchpad to set the whole file.", True
        text = self._text()
        n = text.count(old_string)
        if n == 0:
            hint = ""
            first = next((l for l in old_string.splitlines() if l.strip()), "")
            file_lines = text.splitlines()
            close = difflib.get_close_matches(first, file_lines, n=1, cutoff=0.6)
            if close:
                lineno = file_lines.index(close[0]) + 1
                hint = f" Closest line is {lineno}: {close[0]!r}. Check whitespace and indentation."
            return f"Rejected: old_string not found in {FILENAME}.{hint}", True
        if n > 1 and not replace_all:
            return (
                f"Rejected: old_string occurs {n} times. Include more surrounding "
                "context to make it unique, or set replace_all=true."
            ), True
        new_text = text.replace(old_string, new_string) if replace_all else text.replace(old_string, new_string, 1)
        self.path.write_text(new_text)
        self._seen = self._hash(new_text)
        count = n if replace_all else 1
        return f"Edited {FILENAME} ({count} replacement{'s' if count != 1 else ''}).", False

    def run_scratchpad(self, timeout_seconds=60, content=None):
        timeout_seconds = max(1, min(int(timeout_seconds), self.max_seconds or MAX_SECONDS))
        wrote = ""
        if content is not None:
            text, err = self.write_scratchpad(content)
            if err:
                return text, True
            wrote = f"\n(ran it after writing {len(content.splitlines())} lines)"
        if not self._text().strip():
            return f"{FILENAME} is empty, so there is nothing to run: pass content, or write the file first.", True
        ran = self.sandbox.run(self.dir, FILENAME, timeout_seconds)
        if ran.status == "unavailable":
            return f"Could not run {FILENAME}: {ran.stderr}", True
        status = {
            "ok": f"exit code {ran.returncode}",
            "error": f"exit code {ran.returncode}",
            "timeout": f"killed after {timeout_seconds}s timeout" + (f"; it was at {ran.where}" if ran.where else ""),
            "memory": f"killed: it used more than {self.sandbox.memory_mb:,} MB of memory",
            "output": f"stopped: it printed more than {self.sandbox.max_output // 2**20} MB",
            "file": f"stopped: it wrote a file larger than {getattr(self.sandbox, 'max_file', self.sandbox.max_output) // 2**20:,} MB",
            "processes": f"killed: it had more than {getattr(self.sandbox, 'processes', 1)} processes at once",
            "stopped": "killed: the harness is shutting down",
        }[ran.status]
        # A crashing script is a valid result, not a tool failure, so is_error stays False.
        return (
            f"[{status}, {ran.seconds:.1f}s]{wrote}\n"
            f"--- stdout ---\n{self._clip(ran.stdout) or '(empty)'}\n"
            f"--- stderr ---\n{self._clip(ran.stderr) or '(empty)'}"
        ), False


# The longest run a call may ask for: the schema's maximum in tools.yaml, which is what the model is shown.
MAX_SECONDS = next(t for t in Scratchpad.tools if t["name"] == "run_scratchpad")["input_schema"]["properties"][
    "timeout_seconds"
]["maximum"]
