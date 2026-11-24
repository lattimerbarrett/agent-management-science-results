from pathlib import Path
root=Path('experiments')
print('Available experiment directories:', [str(p) for p in root.iterdir()] if root.exists() else 'none')
if root.exists():
 for name in ['e3','e6']:
  p=root/name
  print('\n',name)
  if p.exists():
   files=list(p.rglob('*.md'))
   for f in files:
    if any(t in f.name for t in ['mass_reduction','local_pohozaev_bridge','fixed_domain_reduction','finite_spin_cover']):
     print(f)
     text=f.read_text()
     print(text[:12000])
