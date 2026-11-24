from pathlib import Path
p=Path('experiments/e3/boundary_yamabe_verified/workspace')
for name in ['agent2_n19_critical_certificate.py','agent2_finite_maxima_certificates.py','agent4_all_n_certificate.py']:
 s=(p/name).read_text(); print('\nFILE',name,'\n',s[:2500], '\nEND\n',s[-1800:])
