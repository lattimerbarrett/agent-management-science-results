from pathlib import Path
for d in ('e5','e6'):
 print('\n',d)
 p=Path('experiments')/d
 for f in sorted(p.rglob('*')):
  if f.is_file() and f.suffix in ('.md','.txt'):
   print(f)
