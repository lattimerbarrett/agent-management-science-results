"""Reproduce the finite checks for the sharp restart threshold.
Run from the parent of workspace/: python workspace/run_final_checks.py
Add --full to recompute the directed interval certificate (about ten minutes).
Dependencies: SageMath (importable), NumPy, SciPy, SymPy, mpmath, z3.
No external programs and no network are used.
"""
import sys, runpy, time
from pathlib import Path
sys.path.insert(0, str(Path('workspace').resolve()))
CHECKS = [
 'agent2_s1_checks.py', 'agent4_polynomial_tv_check.py',
 'agent1_s2_checks.py', 'agent2_s3_logmoment_checks.py',
 'agent2_quadratic_flight_checks.py', 'agent2_strict_left_deflation_checks.py',
 'agent2_s3_sixnode_geometry_checks.py', 'agent4_virtual_probe_checks.py',
 'agent3_root_turning_checks.py', 'agent3_virtual_root_checks.py',
 'agent4_lifting_checks.py', 'agent2_floquet_budget_check_v2.py',
 'agent2_certificate_post_audit.py']

def main():
 for name in CHECKS:
  start=time.time(); print('\n===', name, '===', flush=True)
  runpy.run_path(str(Path('workspace') / name), run_name='__main__')
  print('PASS; %.3f seconds' % (time.time()-start), flush=True)
 if '--full' in sys.argv:
  import agent4_periodic_pointwise_certificate as cert
  # New output directory avoids accepting cached interval calculations.
  cert.OUT=Path('workspace/final_recomputed_certificate')
  assert not cert.OUT.exists(), 'Remove or rename final_recomputed_certificate before rerunning --full'
  cert.OUT.mkdir(); cert.main()
 print('\nALL FINITE CHECKS PASSED. The analytic proof is indexed in workspace/PROOF_INDEX.md.')

if __name__=='__main__': main()
