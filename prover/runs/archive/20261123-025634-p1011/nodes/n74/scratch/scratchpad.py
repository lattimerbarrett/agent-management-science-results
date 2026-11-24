from pathlib import Path
import re
for e in ['e1','e2','e3','e4','e5','e6','e7']:
 print('\nTEAM',e)
 for p in (Path('experiments')/e).rglob('*'):
  if p.suffix not in ['.md','.txt']:continue
  text=p.read_text(errors='replace')
  lines=text.splitlines()
  for i,line in enumerate(lines):
   if re.search(r'Li.{0,8}Zhu|Marques.{0,20}(compact|theorem)|Han.{0,8}Li|dimension.{0,8}seven.{0,35}(example|construct)|[nN][ ≥=>]*7.{0,35}(counterexample|noncompactness)',line):
    if len(line)<1500: print(p.name,':',line[:700])
