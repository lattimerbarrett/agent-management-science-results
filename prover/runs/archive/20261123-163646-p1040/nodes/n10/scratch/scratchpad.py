from pathlib import Path
p=Path('experiments/e1')
for f in p.glob('*.md'):
 s=f.read_text()
 if any(w in s.lower() for w in ['bartholdi','andreadakis','degree 6','degree six','gamma7']):
  print('\n###',f.name)
  for line in s.splitlines():
   if any(w in line.lower() for w in ['bartholdi','andreadakis','degree 6','degree six','gamma7','classification','degree-three','degree three']):print(line)
for name in ['agent1_verified_partial_proof.md','agent2_degree3_BCH_audit.md','agent2_compact_cover_proof.md']:
 print('\n###',name,'\n',(p/name).read_text()[:18000])