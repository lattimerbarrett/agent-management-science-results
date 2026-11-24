from pathlib import Path
for eid in ['e1','e2']:
 p=Path('experiments')/eid
 print(eid, p.exists())
 if p.exists():
  for f in p.rglob('*'):
   if f.is_file() and f.suffix in ['.md','.txt','.py']:
    print(str(f))
