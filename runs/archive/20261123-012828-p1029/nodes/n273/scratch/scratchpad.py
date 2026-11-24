from pathlib import Path
for d in ('e1','e2','e3','e4'):
 p=Path('experiments')/d
 print(d, ':', ', '.join(x.name for x in p.glob('*') if x.is_file())[:2000])