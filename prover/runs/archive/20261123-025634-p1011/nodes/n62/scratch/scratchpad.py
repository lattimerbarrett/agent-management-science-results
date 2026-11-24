from pathlib import Path
p=Path('experiments/e3/boundary_yamabe_verified/workspace')
for f in p.glob('*.py'):
 t=f.read_text()
 if any(z in t for z in ['write_text','write_bytes',"'w'",'"w"']):
  print('may write',f.name)
print('\nLOW DIM BLOCK FORMULAS\n')
print((p/'agent3_general_blocks.py').read_text()[:16000])
print('\nN19 CERTIFICATE\n')
print((p/'agent2_n19_critical_certificate.py').read_text()[:18000])
