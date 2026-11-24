from pathlib import Path
root=Path('experiments')
print(list(root.iterdir()))
p=root/'e2'/'workspace'
print('workspace exists',p.exists())
print('\n'.join(str(f) for f in (root/'e2').rglob('*') if f.is_file() and ('universal' in f.name or 'standalone' in f.name or 'counterexample' in f.name)))