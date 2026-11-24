from pathlib import Path
p=Path('workspace/agent4_checks.py')
print(p.read_text())
exec(compile(p.read_text(),str(p),'exec'))
