from pathlib import Path
p=Path('experiments/e2/agent3_odd_hilbert_norm_checks.py')
s=p.read_text();s=s[:s.rfind("Path('workspace/")];exec(compile(s,str(p),'exec'))
p=Path('experiments/e2/agent2_hilbert_checks.py')
s=p.read_text();s=s[:s.index('json.dump')];exec(compile(s,str(p),'exec'))