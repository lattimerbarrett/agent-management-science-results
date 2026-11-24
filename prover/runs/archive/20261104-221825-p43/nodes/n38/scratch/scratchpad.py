from pathlib import Path
for e in ['e1','e2']:
 p=Path('experiments')/e
 print(e, p.exists())
 if p.exists():
  for f in p.rglob('*'):
   if f.is_file(): print(f)
