"""Tools defined in YAML and handled by methods of the same name.

A ToolSet subclass names a YAML file of tool definitions (TOOLS_FILE, next to this module). When the class is
created, the file is loaded and checked against the class's methods, so the YAML can't drift from the handlers:
every tool needs a public method of the same name whose parameters match the schema. A handler returns
(content, is_error).

A Toolbox combines several ToolSets into the one tool list an agent gets, and turns tool_use blocks into
tool_result blocks.

Usage:
    box = Toolbox(Scratchpad("scratch/agent_0", sandbox), Submission())
    resp = client.messages.create(..., tools=box.tools, ...)
    results = [box.handle(b) for b in resp.content if b.type == "tool_use"]

    # Log box.tools_hash with each trajectory so you know which descriptions produced it.
"""

import hashlib
import inspect
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent


def load_tools(path, cls):
    """Load and validate tool definitions for `cls`. Returns (tools, short hash of the file)."""
    raw = Path(path).read_bytes()
    tools = yaml.safe_load(raw)
    check_tools(tools, cls, Path(path).name)
    return tools, hashlib.sha256(raw).hexdigest()[:12]


def check_tools(tools, cls, where):
    """Fail fast if a YAML file has drifted from the handler signatures."""
    for t in tools:
        name = t.get("name")
        fn = getattr(cls, name, None) if name else None
        if fn is None or name.startswith("_"):
            raise ValueError(f"{where}: no {cls.__name__} handler for tool {name!r}")
        params = {k: p for k, p in inspect.signature(fn).parameters.items() if k != "self"}
        schema = t.get("input_schema", {})
        props = set(schema.get("properties", {}))
        required = set(schema.get("required", []))
        if extra := props - params.keys():
            raise ValueError(f"{where}: {name} declares {sorted(extra)}, which the handler doesn't accept")
        needed = {k for k, p in params.items() if p.default is p.empty}
        if missing := needed - required:
            raise ValueError(
                f"{where}: {name} handler requires {sorted(missing)}, which the schema doesn't mark as required"
            )
        if not isinstance(t.get("description"), str) or not t["description"].strip():
            raise ValueError(f"{where}: {name} has no description")


class ToolSet:
    """Base class: set TOOLS_FILE and write one method per tool, returning (content, is_error)."""

    TOOLS_FILE: str | None = None
    tools: list[dict] = []
    tools_hash: str = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.TOOLS_FILE:
            cls.tools, cls.tools_hash = load_tools(HERE / cls.TOOLS_FILE, cls)


class Toolbox:
    """The tools of several ToolSets, routed by name."""

    def __init__(self, *toolsets):
        self.tools, self._owner = [], {}
        for ts in toolsets:
            for t in ts.tools:
                if t["name"] in self._owner:
                    raise ValueError(f"duplicate tool {t['name']}")
                self._owner[t["name"]] = ts
                self.tools.append(t)
        self.tools_hash = hashlib.sha256(
            "".join(f"{type(ts).__name__}:{ts.tools_hash}" for ts in toolsets).encode()
        ).hexdigest()[:12]

    def _resolve(self, name):
        """The tool a name means. Accepts a name that differs only in letter case, as models occasionally
        send; anything else is an error that lists the real names."""
        if name in self._owner:
            return name, None
        same = [n for n in self._owner if n.lower() == str(name).lower()]
        if len(same) == 1:
            return same[0], None
        return None, f"Unknown tool {name!r}. Available tools: {', '.join(self._owner)}."

    def call(self, name, inp):
        """Run one tool call. Returns (content, is_error); never raises for a bad call."""
        name, err = self._resolve(name)
        if err:
            return err, True
        fn = getattr(self._owner[name], name)
        if not isinstance(inp, dict):
            return f"Tool error: the input to {name} must be a JSON object.", True
        params = {k: p for k, p in inspect.signature(fn).parameters.items()}
        if unknown := sorted(set(inp) - params.keys()):
            return (
                f"Tool error: {name} has no parameter {', '.join(map(repr, unknown))}. "
                f"Its parameters are: {', '.join(params) or 'none'}."
            ), True
        if missing := sorted(k for k, p in params.items() if p.default is p.empty and k not in inp):
            return f"Tool error: {name} needs {', '.join(map(repr, missing))}.", True
        try:
            content, is_error = fn(**inp)
        except Exception as e:  # bad argument types, IO errors, ...
            return f"Tool error: {type(e).__name__}: {e}", True
        return (content if content.strip() else "(no output)"), is_error

    def handle(self, block):
        """Turn a tool_use block into a tool_result block."""
        content, is_error = self.call(block.name, block.input)
        return {"type": "tool_result", "tool_use_id": block.id, "content": content, "is_error": is_error}
