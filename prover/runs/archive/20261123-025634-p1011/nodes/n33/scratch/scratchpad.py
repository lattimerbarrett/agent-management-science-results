from pathlib import Path
b=Path('experiments/e3')
for f in ['agent2_finite_maxima_certificates.py','agent4_green_mass_reduction.md']:
 text=(b/f).read_text()
 print('FILE',f,'\n',text[:16000])
