from pathlib import Path
p=Path('experiments/e4')
print('Available e4 files:')
print('\n'.join(str(f) for f in p.rglob('*') if f.is_file()))
