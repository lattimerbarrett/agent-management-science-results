import runpy
for p in ['workspace/agent2_pullback_checks.py','workspace/agent4_finite_checks.py','workspace/agent3_cut_checks.py','workspace/agent4_kpair_checks.py']:
    print('RUN', p)
    runpy.run_path(p, run_name='__main__')
