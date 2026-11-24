from pathlib import Path
p=Path('experiments/e1')
for f in ['agent4_crossed_cover_lemma.md','agent4_H4_torsion_centrality.json','agent2_H4_full_audit.json','agent2_cover_class3_invariants.json','agent4_d9_lcs_ranks.json','agent1_direct_d8_certificate.json']:
 print('\n###',f,'\n', (p/f).read_text()[:15000])