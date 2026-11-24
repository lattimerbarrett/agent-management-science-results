from pathlib import Path
for team in ['e2','e3']:
 p=Path('experiments')/team
 print('\n',team)
 for q in sorted(p.glob('*')):
  if ('standalone' in q.name or 'selfcontained' in q.name or 'universal' in q.name or 'checker' in q.name or 'lower' in q.name): print(q.name)
