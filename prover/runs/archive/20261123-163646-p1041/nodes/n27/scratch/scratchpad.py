from pathlib import Path
for f in ['agent3_h316_type2_closure_certificate.py','agent3_h316_type3_closure_certificate.py','agent2_mixed_search.py','agent3_low.py']:
 print('\n###',f);print(Path('experiments/e1/'+f).read_text()[:13000])