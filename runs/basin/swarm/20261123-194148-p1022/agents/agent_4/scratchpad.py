import runpy,sys
sys.path.insert(0,'workspace')
for path in ['workspace/agent2_p2_checks.py','workspace/agent4_integrability_checks.py','workspace/agent4_p4_quadratic_checks.py']:
 print('\nRUN',path)
 runpy.run_path(path,run_name='__main__')
