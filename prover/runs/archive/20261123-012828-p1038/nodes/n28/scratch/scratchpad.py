from pathlib import Path
p=Path('experiments/e1')
print('\n'.join(f.name for f in p.iterdir() if f.suffix=='.md'))
