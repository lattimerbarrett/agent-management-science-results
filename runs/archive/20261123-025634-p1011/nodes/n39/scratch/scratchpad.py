from pathlib import Path
for name in ['agent2_n19_critical_certificate.py','agent2_finite_maxima_certificates.py','agent3_local_pohozaev_bridge.md']:
 s=(Path('experiments/e3')/name).read_text()
 print('\n###',name,'\n',s[:6500])
