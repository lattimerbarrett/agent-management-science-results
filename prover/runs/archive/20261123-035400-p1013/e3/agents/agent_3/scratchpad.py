from pathlib import Path
import ast
for p in sorted(Path('workspace').glob('agent3*.py')):
 text=p.read_text(); lines=text.splitlines(True); kept=[];removed=[]
 for line in lines:
  if 'scratchpad.py' in line or ('workspace/agent3' in line and '.write_text(source)' in line):removed.append(line.rstrip())
  else:kept.append(line)
 new=''.join(kept);ast.parse(new)
 if removed:p.write_text(new);print(p.name,'REMOVED',removed)
print('All agent3 Python files parse after export-artifact cleanup.')
