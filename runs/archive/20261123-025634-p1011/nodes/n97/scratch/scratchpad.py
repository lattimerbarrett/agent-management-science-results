from pathlib import Path
b=Path('experiments/e3/boundary_yamabe_verified/workspace')
for name in ['agent3_general_blocks.py','agent2_n19_critical_certificate.py']:
 s=(b/name).read_text()
 print('\n===',name,'===\n',s[-10000:])