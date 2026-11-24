from pathlib import Path
p=Path('/workspace')
s=Path('workspace/agent1_certificate.py').read_text()
s=s[:s.index('from pathlib import Path')]
exec(compile(s,'agent1_certificate.py','exec'))
