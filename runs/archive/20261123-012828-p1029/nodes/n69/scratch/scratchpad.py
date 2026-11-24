from pathlib import Path
p=Path('experiments')
print('Available files:')
for f in p.rglob('*'):
    if f.is_file(): print(f)
