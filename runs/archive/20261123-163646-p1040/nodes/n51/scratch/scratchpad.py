from pathlib import Path
for p in Path('experiments/e2').rglob('*'):
 if p.is_file() and ('metaplectic_final' in p.name or 'metaplectic_filtration' in p.name):
  print('\nFILE',p,'\n',p.read_text()[:22000])