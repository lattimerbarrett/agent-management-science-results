from pathlib import Path
terms=['q-complete','q complete','pseudoconcave','collar','neighbourhood basis']
for d in ['e2','e3','e5','e6']:
 print('\n###',d)
 hits=0
 for p in sorted((Path('experiments')/d).rglob('*')):
  if p.is_file() and p.suffix in ['.md','.txt']:
   text=p.read_text(errors='replace')
   for line in text.splitlines():
    if any(t in line.lower() for t in terms) and ('theorem' in line.lower() or 'oka' in line.lower() or 'not' in line.lower()):
     print(p.name+': '+line[:500]);hits+=1
     if hits>=16: break
  if hits>=16:break
