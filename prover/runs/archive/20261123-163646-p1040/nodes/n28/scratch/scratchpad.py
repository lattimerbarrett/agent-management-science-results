from pathlib import Path
for name in ['agent3_stable_symbolic_checks.py','agent3_odd_hilbert_norm_checks.py']:
 s=(Path('experiments/e2')/name).read_text()
 s='\n'.join(line for line in s.splitlines() if not line.startswith("Path('workspace/"))
 exec(compile(s,name,'exec'))
