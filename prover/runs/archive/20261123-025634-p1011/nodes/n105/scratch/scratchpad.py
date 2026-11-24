from pathlib import Path
p=Path('experiments/e6/agent4_no_degree8_seed_n18.md')
if p.exists():
 print(p.read_text()[:14000])
else:
 for root in [Path('experiments/e6'),Path('experiments/e7')]:
  print(root, [x.name for x in root.glob('*') if 'compactness' in x.name or 'degree8' in x.name or 'no_degree' in x.name])
