from pathlib import Path
p=Path('experiments/e5/agent1_n19_certificate.py')
print(p.read_text()[:35000])
