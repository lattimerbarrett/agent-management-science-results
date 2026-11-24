from pathlib import Path
for f in ['agent1_high_dim_analytic_bridge.md','agent2_gluing_theorem_audit.md']:
 for d in ['e3','e5']:
  p=Path('experiments')/d/f
  if p.exists():
   t=p.read_text(); print('\n###',p,'\n',t[-11000:])
