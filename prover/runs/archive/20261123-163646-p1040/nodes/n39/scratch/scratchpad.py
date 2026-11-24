from pathlib import Path
p=Path('experiments/e2')
for name in ['agent3_odd_hilbert_norm_checks.py','agent4_odd_hilbert_norm_checks.py','agent3_n3_proof.txt']:
 f=p/name
 print('\n###',name,'\n',f.read_text()[:16000] if f.exists() else 'missing')