from pathlib import Path
p=Path('experiments/e4')
print([f.name for f in p.iterdir() if 'highdim' in f.name or 'alln' in f.name])
q=p/'agent4_highdim_algebra.md'
print(q.read_text()[:12000] if q.exists() else '')
