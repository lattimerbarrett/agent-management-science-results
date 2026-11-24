from pathlib import Path
import runpy
for name in ['agent1_psh_check.py', 'agent2_hartogs_check.py', 'agent3_nonpoly_check.py', 'agent4_checks.py', 'agent4_basin_hull_check.py']:
    path = Path('workspace')/name
    print('\n===', name, '===', flush=True)
    runpy.run_path(str(path), run_name='__main__')
print('ALL CHECKS PASSED')
