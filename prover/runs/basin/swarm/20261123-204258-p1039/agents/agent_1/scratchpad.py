from pathlib import Path
for p in Path('workspace').iterdir():
 print(p.name, p.stat().st_size)
