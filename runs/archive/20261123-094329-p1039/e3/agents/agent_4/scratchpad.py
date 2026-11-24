from pathlib import Path
for p in sorted(Path('workspace').iterdir()):
    print(p.name,p.stat().st_size)
