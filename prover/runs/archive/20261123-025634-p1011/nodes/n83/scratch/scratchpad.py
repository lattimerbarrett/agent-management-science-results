from pathlib import Path
p=Path('experiments/e3/agent2_n19_critical_certificate.py')
print(p.read_text()[:14000])
