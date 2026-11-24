from pathlib import Path
for p in Path('experiments').rglob('*.md'):
 lines=p.read_text().splitlines()
 hits=[(i,l) for i,l in enumerate(lines) if 'normal' in l.lower() or 'suprem' in l.lower()]
 if hits:
  print('\n',p)
  for i,l in hits[:14]: print(i+1,l[:350])
