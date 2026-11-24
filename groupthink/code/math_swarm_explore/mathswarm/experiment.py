"""An experiment is a folder under experiments/ with an `experiment.py` that lists its arms.

    experiments/<name>/
        experiment.py     ARMS (a list of `Arm`), and which problems it is about (BENCHMARKS, SPLIT, PROBLEMS)
        README.md         the question, the status, the results
        reproduce.sh      rebuilds every number in the README
        runs/<run>/       one folder per run (mathswarm/tracking.py)

`lab new <name>` writes a new one from the template below; `lab run <name>` runs it.
"""
from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass
from pathlib import Path

from .paths import EXPERIMENTS
from .swarm import Arm


@dataclass
class Experiment:
    name: str
    folder: Path
    arms: dict[str, Arm]
    benchmarks: list[str]
    split: str
    problems: int | None
    question: str


def load(name: str) -> Experiment:
    folder = EXPERIMENTS / name
    path = folder / "experiment.py"
    if not path.exists():
        known = ", ".join(sorted(p.parent.name for p in EXPERIMENTS.glob("*/experiment.py"))) or "none yet"
        raise SystemExit(f"no experiment {name!r} (experiments: {known}). `lab new {name}` starts one.")
    spec = importlib.util.spec_from_file_location(f"experiment_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    arms = list(getattr(module, "ARMS", []))
    if not arms or not all(isinstance(arm, Arm) for arm in arms):
        raise SystemExit(f"{path} must define ARMS, a list of Arm")
    if len({arm.name for arm in arms}) != len(arms):
        raise SystemExit(f"{path}: two arms have the same name")
    return Experiment(name, folder, {arm.name: arm for arm in arms}, list(getattr(module, "BENCHMARKS", ["aime_2024"])),
                      getattr(module, "SPLIT", "train"), getattr(module, "PROBLEMS", None),
                      (module.__doc__ or "").strip().split("\n\n")[0])


TEMPLATE = '''"""{question}

    lab run {name} --dry-run           # scripted stand-ins: checks the arms run, in seconds
    lab run {name} --name pilot --problems 2 --mem-gb 28
    lab show {name}/pilot
"""
from mathswarm import Arm, RandomLooks

# Which problems. Learn and explore on a train split (aime_2024 for math, gpqa_diamond for logic) and keep the
# test splits for the result you mean to report.
BENCHMARKS = ["aime_2024"]
SPLIT = "train"
PROBLEMS = 5            # the first N of each benchmark's fixed order; None is all of them

# The baseline (CURRENT.md): every agent alone at its desk, and nobody reads anybody.
DESK = Arm("desk", agents=12)

# One arm per row of the results table. An agent is the same agent in every arm, reply for reply, until it is
# first shown something the others are not: differences between arms are differences in what that did.
ARMS = [
    DESK,
    DESK.but("look_at_self", looks=RandomLooks(at="own")),      # the control: the same extra turns, reading its own file
    DESK.but("look_at_others", looks=RandomLooks()),            # now and then an agent reads another's file and says what it makes of it
    # DESK.but("your_idea", looks=...),
]
'''

README = '''# {name}

**Question.** {question}

**Status.** Not run yet.

## Results

None yet. `lab show {name}/<run>` prints a run's tables.

## Run it

```bash
experiments/{name}/reproduce.sh
```
'''

REPRODUCE = '''#!/bin/bash
# Rebuild every number in this experiment's README from nothing. Resumable: run it again after a stop.
set -euo pipefail
cd "$(dirname "$0")/../.."
uv run lab data
uv run lab run {name} --name main
uv run lab show {name}/main
'''


def new(name: str, question: str) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise SystemExit("an experiment's name is lower case words joined by _ : random_gossip")
    folder = EXPERIMENTS / name
    if folder.exists():
        raise SystemExit(f"{folder} already exists")
    folder.mkdir(parents=True)
    question = question or "What is this experiment asking?"
    (folder / "experiment.py").write_text(TEMPLATE.format(name=name, question=question))
    (folder / "README.md").write_text(README.format(name=name, question=question))
    (folder / "reproduce.sh").write_text(REPRODUCE.format(name=name))
    (folder / "reproduce.sh").chmod(0o755)
    return folder
