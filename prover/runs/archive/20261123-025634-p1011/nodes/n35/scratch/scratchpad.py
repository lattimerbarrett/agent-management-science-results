from pathlib import Path
r=Path('experiments/e3')
print((r/'agent2_conditional_simple_estimate.md').read_text())
print('\n### high-dimensional finite lemma and certificates (headers)')
for name in ['agent2_n19_critical_certificate.py','agent2_finite_maxima_certificates.py','agent4_all_n_certificate.py']:
 t=(r/name).read_text(); print('\n',name,'\n',t[:2400])
