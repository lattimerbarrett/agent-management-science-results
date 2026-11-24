from pathlib import Path
p=Path('experiments')
for f in p.rglob('*'):
 print(f)
