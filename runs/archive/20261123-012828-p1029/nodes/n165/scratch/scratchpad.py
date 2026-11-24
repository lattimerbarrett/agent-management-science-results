from pathlib import Path
for f in Path('experiments/e1').rglob('*'):
 if f.is_file(): print(str(f), f.stat().st_size)
