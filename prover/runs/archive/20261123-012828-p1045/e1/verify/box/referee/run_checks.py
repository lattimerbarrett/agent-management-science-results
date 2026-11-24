import runpy
print('ELEMENTARY CHECKS:')
runpy.run_path('workspace/agent1_elementary_complete_checks.py',run_name='__main__')
print('BERNSTEIN CHECKS:')
runpy.run_path('workspace/agent2_mixed_certificate.py',run_name='__main__')
