from pathlib import Path
p=Path('experiments/e3')
print(list(p.iterdir()))
for f in p.glob('*'):
 if 'collapse' in f.name or 'ellipsoid' in f.name:
  print('\nFILE',f.name,'\n',f.read_text()[:18000])
