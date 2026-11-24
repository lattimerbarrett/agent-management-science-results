import sys
sys.path.insert(0, '/agents/agent_1')
# Resolve available record paths without changing the original script.
from pathlib import Path
p=Path('agents/agent_1/scratchpad.py')
if not p.exists():
    for parent in Path.cwd().parents:
        q=parent/'agents/agent_1/scratchpad.py'
        if q.exists():
            p=q; break
print('source',p)
exec(compile(p.read_text(),str(p),'exec'), {'__name__':'__main__'})
