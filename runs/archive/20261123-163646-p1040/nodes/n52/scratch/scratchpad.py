from pathlib import Path
p=Path('experiments/e2')
for name in ['agent3_n3_proof.txt','agent3_metaplectic_route.txt','agent4_base_derivation.txt']:
 print('\n###',name,'\n',(p/name).read_text()[:24000])