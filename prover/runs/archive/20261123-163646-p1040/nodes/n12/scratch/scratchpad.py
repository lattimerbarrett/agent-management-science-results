from pathlib import Path
r=Path('experiments/e1')
for name in ['agent4_d9_lcs_ranks.json','agent4_H4_torsion_centrality.json','agent1_verified_partial_proof.md','rank2_proof.md','agent4_all_rank_degree2_proof.md','agent3_W_detector_functional.json']:
 print('\n###',name,'\n', (r/name).read_text()[:16000])
