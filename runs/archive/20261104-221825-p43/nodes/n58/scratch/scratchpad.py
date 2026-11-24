from pathlib import Path
p=Path('experiments/e3')
print('\n'.join(str(x) for x in p.iterdir()))
for x in p.iterdir():
 if 'collapse' in x.name or 'ellipsoid' in x.name:
  print('\nFILE',x.name,'\n',x.read_text()[:16000])