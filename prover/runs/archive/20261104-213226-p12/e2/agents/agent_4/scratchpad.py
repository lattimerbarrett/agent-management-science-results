from pathlib import Path
p=Path('workspace/agent1_bundle/proof.md')
s=p.read_text()
Path('workspace/agent4_full_proof_final.md').write_text(s)
print('Preserved independent full proof at own path; current bundle proof chars',len(s))