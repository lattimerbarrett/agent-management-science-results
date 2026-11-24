from pathlib import Path
for e in ['e1','e2']:
 p=Path('experiments')/e
 print(e, p.exists())
 if p.exists():
  print('\n'.join(str(q) for q in p.rglob('*.py'))[:12000])
