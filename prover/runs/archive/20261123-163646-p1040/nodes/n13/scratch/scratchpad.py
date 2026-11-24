from pathlib import Path
p=Path('experiments/e1/agent1_compact_D7_conflict_certificate.py')
exec(compile(p.read_text(),str(p),'exec'))
