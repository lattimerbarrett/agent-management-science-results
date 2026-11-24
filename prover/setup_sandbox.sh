#!/bin/sh
# Build .sandbox/, the Python that agents' scratchpad.py files run with (see sandbox.py), from the
# pinned sandbox-requirements.txt. Binary wheels only: nothing is compiled. About 2 GB, a minute or two.
set -eu
cd "$(dirname "$0")"

uv venv .sandbox --python 3.12 --allow-existing -q
uv pip install --python .sandbox/bin/python --only-binary :all: -r sandbox-requirements.txt

# Sage's caches (import cache, GAP workspace), built once and seeded into each agent's home; then check
# that the sandbox holds and that every library imports inside it.
uv run python -c "
from pathlib import Path
import tempfile
from sandbox import Sandbox
box = Sandbox()
assert box.ready() is None, box.ready()
box.build_home_template()
with tempfile.TemporaryDirectory() as d:
    leaks = box.leaks(Path(d) / 'probe')
    assert not leaks, f'sandbox leaks: {leaks}'
    (Path(d) / 'probe' / 'libs.py').write_text(
        'import numpy, scipy, sympy, networkx, pandas, sklearn, gmpy2, z3, mpmath\n'
        'from sage.all import factor, libgap\n'
        'print(factor(2**64 + 1), libgap.SymmetricGroup(4).Size())\n')
    ran = box.run(Path(d) / 'probe', 'libs.py', timeout=120)
    assert ran.status == 'ok', ran
print('sandbox ok: no leaks; NumPy, SciPy, SymPy, NetworkX, pandas, scikit-learn, gmpy2, Z3, Sage, GAP import')
"
