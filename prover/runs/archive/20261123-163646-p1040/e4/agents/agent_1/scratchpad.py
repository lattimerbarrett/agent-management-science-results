from pathlib import Path
for f in Path('workspace').glob('*'):
 print(f, f.stat().st_size)
