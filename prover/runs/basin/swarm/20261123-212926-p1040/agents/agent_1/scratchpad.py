from pathlib import Path
p=Path('workspace/agent1_final_certificate.py');print('bytes',len(p.read_text()),'lines',len(p.read_text().splitlines()));print(p.read_text())
