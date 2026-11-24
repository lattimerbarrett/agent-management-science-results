from pathlib import Path
p=Path('experiments/e1')
for f in sorted(p.glob('*.md')):
 print(f.name)
for name in ['agent2_degree3_BCH_audit.md','agent1_verified_partial_proof.md']:
 print('\n###',name,'\n',(p/name).read_text()[:20000])