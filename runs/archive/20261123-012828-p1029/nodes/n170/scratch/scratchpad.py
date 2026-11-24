from pathlib import Path
for p in Path('experiments').rglob('*.md'):
 text=p.read_text()
 if any(w in text.lower() for w in ['quantitative','cotype','2/3','holder','hölder','exhaust']):
  print('\nFILE',p)
  lines=text.splitlines()
  for i,l in enumerate(lines):
   if any(w in l.lower() for w in ['cotype','2/3','holder','hölder','exhaust']):
    print('\n'.join(lines[max(0,i-2):i+4]))
