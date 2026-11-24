import runpy
for path in ['workspace/agent1_solution_checks.py','workspace/agent3_finite_chart_checks.py','workspace/agent3_analytic_bound_checks.py','workspace/agent3_chart_formulas.py','workspace/agent2_planar_checks_final.py','workspace/agent4_lower_checks.py','workspace/agent4_exact3_checks.py']:
    print('\nRUN',path,flush=True)
    runpy.run_path(path,run_name='__main__')
