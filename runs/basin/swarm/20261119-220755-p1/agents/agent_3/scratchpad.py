import runpy,time
from pathlib import Path
for name in ['agent3_root_turning_checks.py','agent3_virtual_root_checks.py']:
    p=Path('workspace')/name
    start=time.time()
    print('\nRUNNING',p,flush=True)
    runpy.run_path(str(p),run_name='__main__')
    print('COMPLETED',name,'seconds',time.time()-start,flush=True)
