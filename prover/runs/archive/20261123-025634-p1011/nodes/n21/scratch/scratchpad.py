from pathlib import Path
import re
for folder in ['e1','e2','e3']:
 print('\n===',folder,'===')
 count=0
 for p in (Path('experiments')/folder).rglob('*'):
  if p.suffix not in ('.md','.txt'):continue
  for i,line in enumerate(p.read_text(errors='replace').splitlines(),1):
   if re.search(r'umbilic|Felli|Ahmedou|Disconzi|Khuri|compactness theorem|Marques',line,re.I):
    print(f'{p.name}:{i}: {line[:450]}')
    count+=1
    if count>=30:break
  if count>=30:break
