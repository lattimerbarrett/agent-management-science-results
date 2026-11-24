from pathlib import Path
for folder in ['experiments/e1','experiments/e2']:
 print('\n',folder)
 for p in sorted(Path(folder).iterdir()):
  if p.name.endswith(('.json','.txt','.log')) and any(z in p.name for z in ['chat','slack','channel','final','notes','messages']): print(p,p.stat().st_size)
print('\nNeutral matrix proof source:\n')
p=Path('experiments/e1/neutral_witness_checks_agent2.py')
print(p.read_text() if p.exists() else 'Not found')
