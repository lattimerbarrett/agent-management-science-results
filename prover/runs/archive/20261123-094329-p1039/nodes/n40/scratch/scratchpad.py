from pathlib import Path
for d in Path('experiments').iterdir():
 for p in d.rglob('*'):
  if p.is_file() and p.suffix in ['.md','.txt']:
   lines=p.read_text(errors='replace').splitlines()
   for i,l in enumerate(lines):
    if any(k in l.lower() for k in ['zariski','hyperplane','convex section']):
     print(str(p)+': '+ '\n'.join(lines[max(0,i-1):min(len(lines),i+4)]))
