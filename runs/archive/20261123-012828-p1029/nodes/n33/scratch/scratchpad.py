from pathlib import Path
for root in ['e1','e2','e3']:
 for p in (Path('experiments')/root).rglob('*'):
  if p.is_file() and p.suffix in ['.md','.txt']:
   text=p.read_text(errors='ignore')
   for line in text.splitlines():
    if any(s in line.lower() for s in ['sait','berberian','wright','kaplansky','haagerup','monotone complete']):
     print(p.name+': '+line[:600])
