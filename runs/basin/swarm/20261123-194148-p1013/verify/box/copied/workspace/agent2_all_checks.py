"""Reproduce the finite audits supporting the completed extremal-cycle proof.
Run from the repository root: python workspace/agent2_all_checks.py
Analytic statements are proved in the accompanying .md files; finite tests
are independent verification, not substitutes for universal proofs.
"""
from pathlib import Path
import contextlib, hashlib, io, json, runpy, time
SCRIPTS = [
 ('agent2_H17_odd_a0_checks.py', 'H17 critical vertex, matching and finite-hole equality catalogue'),
 ('agent2_H17_odd_cycles.py', 'Exact odd-order witness cycle counts; tiny brute-force cross-checks'),
 ('agent3_turan_coarse_cycle_lower_checks.py', 'Markov covariance and closure identities for the coarse cycle lower bound'),
 ('agent3_rotation_transfer_checks.py', 'Posa rotation identities, inverses and half-density prefix bound'),
 ('agent4_finite_hole_template_checks.py', 'Finite-hole abundance remapping'),
 ('agent2_uniform_imbalance_checks.py', 'Perron eigenvalue derivatives and exact covariance/Hessian normalization'),
 ('agent2_uniform_forest_error_checks.py', 'All small-graph path-forest error inequalities'),
 ('agent2_phase_bound_check.py', 'Exact rational exhaustive phase/lattice optimization'),
 ('agent2_lower_arithmetic_fast_checks.py', 'Symbolic threshold factorization, wedge extrema and cutoff signs'),
 ('agent3_profile_gadget_checks.py', 'CSP dictatorship, exact eigenbasis and robust-anchor SMT tests'),
 ('agent4_finite_phase_basis_checks.py', 'Finite forbidden basis catalogues, failure certificates and edge profiles'),
 ('agent2_endpoint_wedge_checks.py', 'Equal-(v,e) marker path-polynomial coefficients and endpoint wedge shift'),
]
def main():
 start=time.perf_counter(); rows=[]
 for name,scope in SCRIPTS:
  p=Path('workspace')/name; source=p.read_bytes(); out=io.StringIO(); t=time.perf_counter()
  print('CHECK',name,flush=True)
  with contextlib.redirect_stdout(out):runpy.run_path(str(p),run_name='__main__')
  rows.append(dict(script=name,scope=scope,sha256=hashlib.sha256(source).hexdigest(),seconds=round(time.perf_counter()-t,3),status='PASS',stdout=out.getvalue()))
  print(' PASS',rows[-1]['seconds'],'seconds',flush=True)
 result=dict(status='ALL CHECKS PASSED',seconds=round(time.perf_counter()-start,3),checks=rows)
 Path('workspace/agent2_all_checks_manifest.json').write_text(json.dumps(result,indent=2))
 print(result['status'],len(rows),'programs;',result['seconds'],'seconds',flush=True)
if __name__=='__main__':main()
