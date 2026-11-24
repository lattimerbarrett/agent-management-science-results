from pathlib import Path
p=Path('experiments/e3/boundary_yamabe_verified/workspace')
for f in ['agent3_general_blocks.py','agent2_n19_critical_certificate.py','agent2_finite_maxima_certificates.py','agent4_translation_ge40.py']:
 t=(p/f).read_text();print('\n##',f,'\n',t[:18000])