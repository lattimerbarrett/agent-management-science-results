from pathlib import Path
p=Path('workspace/agent3_all_finite_checks.py').read_text()
print(p[p.index('def verify_geometric_linear_algebra'):])
