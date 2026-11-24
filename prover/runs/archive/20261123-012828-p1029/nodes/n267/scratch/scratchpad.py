from pathlib import Path
p=Path('experiments/e1/agent3_completion_audit.md')
print(p.read_text())
print('\nAvailable e4 files:')
p=Path('experiments/e4')
print([x.name for x in p.iterdir()] if p.exists() else 'not available')