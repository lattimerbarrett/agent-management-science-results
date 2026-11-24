from pathlib import Path
for k in ('e1','e2','e3'):
 p=Path('experiments')/k
 print('\n',k, 'exists:',p.exists())
 if p.exists():
  print('\n'.join(str(x) for x in list(p.rglob('*'))[:45]))
