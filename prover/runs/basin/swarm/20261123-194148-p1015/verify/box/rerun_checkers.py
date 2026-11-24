import sys, importlib.util, json
from pathlib import Path
root=Path('/mnt')
# Read-only team scripts are imported, so their __main__ output files are not written.
sys.path.insert(0, 'workspace')
import agent2_birth_tree_checks as birth
print('BIRTH CHECK:')
print(birth.main())
print('OPERATOR CHECK SOURCE:')
print(Path('workspace/agent1_operator_checks.py').read_text())
