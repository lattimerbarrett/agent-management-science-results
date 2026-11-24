import sys
sys.path.insert(0,'../agents/agent_1')
# Absolute path resolved relative to this folder through parent.
from pathlib import Path
print(Path.cwd())
p=Path('../agents/agent_1/scratchpad.py')
if not p.exists(): p=Path('agents/agent_1/scratchpad.py')
ns={'__name__':'team_checked'}
exec(p.read_text(),ns)
ns['self_test']()
ns['self_test'](300)
