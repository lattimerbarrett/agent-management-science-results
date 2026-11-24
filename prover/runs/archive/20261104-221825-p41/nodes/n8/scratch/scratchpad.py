from pathlib import Path
p=Path('experiments/e1')
print('workspace exists:',p.exists())
if p.exists():
 for q in p.rglob('*'):
  if q.is_file():print(q)
