from pathlib import Path
b=Path('experiments/e1')
for name in ['agent4_all_rank_degree2_proof.md','agent2_allrank_degree2_audit.md','agent1_verified_partial_proof.md']:
 print('\n###',name,'\n',(b/name).read_text()[:16000])
