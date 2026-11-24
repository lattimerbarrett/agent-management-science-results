from pathlib import Path
p=Path('experiments/e1/agent4_checks.py')
print(p.read_text())
print('\n--- EXECUTION ---')
exec(compile(p.read_text(),str(p),'exec'))
