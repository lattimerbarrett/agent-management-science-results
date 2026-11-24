from pathlib import Path
for p in sorted(Path('workspace').glob('agent2_*.py')):print(p.name,p.stat().st_size)
