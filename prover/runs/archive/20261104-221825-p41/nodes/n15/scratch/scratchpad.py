from pathlib import Path
for e in ['e2','e3','e4']:
 p=Path('experiments')/e/'workspace'
 print(e,p.exists())
 if p.exists():
  for f in sorted(p.iterdir()):
   if any(s in f.name for s in ['standalone','universal','lower','cone','filling','tree_capacity','fewer_ghosts','README','notes','summary']):print(f.name)
