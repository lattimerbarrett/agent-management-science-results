from pathlib import Path
for name in ['final_checks.py','agent1_cantor_lower_checks.py','agent2_upper_checks.py','agent4_horizontal_checks.py']:
    print('\nRUNNING', name, flush=True)
    code=Path('workspace/'+name).read_text()
    if name=='agent4_horizontal_checks.py':
        code='\n'.join(code.splitlines()[:65])
    exec(compile(code, 'workspace/'+name, 'exec'), {'__name__':'__main__'})
