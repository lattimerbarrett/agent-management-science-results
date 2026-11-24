from pathlib import Path
p=Path('experiments/e1/agent2_threshold_checks.py')
print(p.read_text())
exec(compile(p.read_text(), str(p), 'exec'))