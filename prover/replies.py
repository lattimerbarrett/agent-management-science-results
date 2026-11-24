"""Reading a model's reply when it was asked for one JSON object."""

import json
import re

FENCED = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)
BACKSLASH = re.compile(r'\\(\\|"|/)?')  # a backslash, with what it escapes when that is \, " or /


def literal(text):
    """`text` with each backslash that doesn't escape \\, " or / doubled: LaTeX that gpt-6.1-sol writes in a JSON string,
    such as \\(1+d^2\\), read as itself (JSON allows no \\( escape, so the whole reply would fail to parse)."""
    return BACKSLASH.sub(lambda m: m.group(0) if m.group(1) else "\\\\", text)


def parse(text):
    """The JSON object of a reply: in a ```json block, or else from its first { to its last }; failing that, the same
    with its backslashes read as themselves (`literal`). None if there is none."""
    candidates = [*(m.group(1) for m in FENCED.finditer(text)), text[text.find("{") : text.rfind("}") + 1]]
    for candidate in candidates + [literal(c) for c in candidates]:
        try:
            value = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(value, dict):
            return value
    return None
