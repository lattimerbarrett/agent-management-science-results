from pathlib import Path
p=Path('experiments/e1')
for f in ['agent1_direct_d8_certificate.json','agent3_mod9_gamma5_invariants.json','agent3_mod9_gamma6_invariants.json','agent3_mod9_gamma7_invariants.json','agent3_mod27_gamma5_invariants.json','agent3_mod27_gamma6_invariants.json','agent2_H4_full_audit.json','agent4_degree6_primitive_cokernel.json','agent4_johnson_image_degree6_smith.json']:
 print(f,(p/f).read_text()[:4000])
print('\nSCRIPT\n',(p/'agent3_mod9_lcs.py').read_text()[:16000])