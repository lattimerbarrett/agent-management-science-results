from pathlib import Path
p=Path('experiments/e2/agent3_stable_symbolic_checks.py')
code=p.read_text().split("Path('workspace/")[0]
exec(compile(code,str(p),'exec'))
