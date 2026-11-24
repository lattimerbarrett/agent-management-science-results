from pathlib import Path
p=Path('experiments/e1/agent3_completion_audit.md')
print(p.read_text()[:6500])
