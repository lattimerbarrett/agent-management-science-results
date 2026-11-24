from pathlib import Path
p=Path('experiments/e3/boundary_yamabe_verified')
print([q.name for q in p.iterdir()])
print((p/'verify_all.py').read_text()[:6000])
print(Path('experiments/e3/agent4_certificate_notes.txt').read_text()[:8000])
