import runpy
from pathlib import Path
for script in ['upper_bound_agent3.py','complete_check_agent1.py','factor_check_agent2.py','agent4_gaussian_obstruction.py']:
    print('\n===',script,'===', flush=True)
    runpy.run_path(str(Path('workspace')/script), run_name='__main__')
