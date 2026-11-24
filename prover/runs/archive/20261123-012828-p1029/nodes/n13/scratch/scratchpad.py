from pathlib import Path
for p in list(Path('experiments').rglob('*'))[:100]: print(p)
