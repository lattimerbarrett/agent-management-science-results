from pathlib import Path
root=Path('experiments')
print('Experiment directory exists:',root.exists())
if root.exists():
 for p in root.rglob('*'):
  if p.is_file() and p.suffix in ('.md','.txt','.py'):
   print(p)
