from pathlib import Path
for name in ['e1','e2','e3','e4']:
 p=Path('experiments')/name
 print(name, p.exists())
 if p.exists():
  print('\n'.join(str(q) for q in list(p.rglob('*'))[:30]))
