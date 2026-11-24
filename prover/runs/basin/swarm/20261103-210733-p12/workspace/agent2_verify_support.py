"""Recompute the upper bound and every exact boundary-support certificate.
Run from the directory containing workspace/: python workspace/agent2_verify_support.py
Requires Python, SymPy, and SageMath (imported in the same interpreter).

Geometric inputs, not numerical assumptions:
(1) Faber--Zagier/Pixton relations on M_g and M_{g,1};
(2) R^d(M_{g,1})=0 for d>g-1 (pointed socle vanishing).
The pointed variables are logarithmic kappa, so kappa_0=2g-1.

For each a+b=25 this code constructs quotient reductions using actual pointed
FZ relations, then solves OVER Q
 P(kappa^a+kappa^b) = (psi_a+psi_b) Q_{a,b} mod (I_a+I_b).
It checks the exact equality, never inferring consistency from modular rank.
Multiplication by lambda_a lambda_{a-1} lambda_b lambda_{b-1} turns these
open pointed relations into equalities on the compactifications, since that
Hodge product restricts to zero on every boundary of Mbar_{h,1}.
"""
import json, runpy, sys, time
from pathlib import Path
root=Path('.')
assert (root/'workspace').is_dir(), 'Run from the directory containing workspace/'
sys.path.insert(0, 'workspace')
start=time.time()
for name in ('fz25_upper.py','agent2_candidate.py','agent2_exact_divisibility.py'):
    print('RECOMPUTING',name,flush=True)
    runpy.run_path(str(root/'workspace'/name),run_name='__main__')
checks=json.load(open('workspace/agent2_exact_divisibility.json'))
assert len(checks)==12 and {v['split'] for v in checks}==set(range(1,13))
assert all(v['exact_solution'] for v in checks)
print('VERIFIED: 33 independent true degree12 relations, candidate P, and all12 exact support equations.',flush=True)
print('Elapsed seconds',time.time()-start)
