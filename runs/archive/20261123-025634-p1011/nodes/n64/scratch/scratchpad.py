from pathlib import Path
for f in ['agent3_general_blocks.py','agent2_n19_critical_certificate.py','agent2_finite_profiles.txt','agent2_n19_critical_certificate.py']:
 p=Path('experiments/e3')/f
 print('\nFILE',f,'\n', p.read_text()[:22000])
