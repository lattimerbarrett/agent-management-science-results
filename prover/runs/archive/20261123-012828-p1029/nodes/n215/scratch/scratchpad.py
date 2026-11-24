from pathlib import Path
root=Path('experiments')
print('root:', root.exists())
for d in sorted(root.iterdir()) if root.exists() else []:
 print(d.name, len(list(d.iterdir())))
 for p in d.iterdir():
  if p.suffix=='.md':
   text=p.read_text()
   hits=[(i+1,line) for i,line in enumerate(text.splitlines()) if 'corner' in line.lower() or 'normaliz' in line.lower()]
   if hits:
    print(p.name)
    for i,line in hits[:12]: print(i,line)
