"""Reproduce all exact certificates; requires Python, SymPy, NumPy, mpmath.
No network, subprocess, numerical PDE solver, or unstated expected-output test.
Each source hash is checked unchanged after the entire run.
"""
from pathlib import Path
import os, sys, runpy, hashlib, time
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0,str(ROOT/'workspace'))
SCRIPTS=['agent1_machin_checks.py', 'agent1_conformal_checks.py', 'agent1_exact_spectral_sums.py', 'agent1_forced_schur_checks.py', 'agent1_green_flux_warning.py', 'agent1_high_dim_exponent_checks.py', 'agent2_flattening_checks.py', 'agent2_gauge_bubble_checks.py', 'agent2_forced_schur_checks.py', 'agent2_degree4_translation_identity.py', 'agent2_n19_critical_certificate.py', 'agent2_finite_maxima_certificates.py', 'agent3_weighted_estimate.py', 'agent3_general_blocks.py', 'agent3_moment_checks.py', 'agent3_pohozaev_identity.py', 'agent3_borderline_checks.py', 'agent3_compensated_flux_checks.py', 'agent3_general_counterterm_checks.py', 'agent3_forced_schur_checks.py', 'agent4_graph_checks.py', 'agent4_certificates.py', 'agent4_all_n_certificate.py', 'agent4_translation_ge40.py', 'agent4_mass_flux_checks.py']
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'workspace').glob('*.py')}
t0=time.perf_counter()
for name in SCRIPTS:
    print('\n=== RUN', name, '===',flush=True)
    runpy.run_path(str(ROOT/'workspace'/name),run_name='__main__')
after={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in before}
assert before==after, 'A test modified source code'
print('\nALL',len(SCRIPTS),'SCRIPTS PASSED; source hashes unchanged; seconds',round(time.perf_counter()-t0,3),flush=True)
