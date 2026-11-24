import runpy
for path in ['workspace/agent2_upper_checks.py','workspace/agent2_general_group_checks.py','workspace/agent2_capacity_audit.py','workspace/agent3_simple_container_checks.py','workspace/lambda_suitable_checks.py']:
    print('\nRUN',path,flush=True)
    runpy.run_path(path,run_name='__main__')
