import sys,runpy,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
start=time.time()
for name in ['agent4_r2_bruteforce.py','agent4_bipartite_checks.py','agent4_edgeworth.py','agent4_second_order.py','agent4_sharp_checks.py','agent4_r2_counter.py']:
 print('\nRUNNING',name,flush=True)
 runpy.run_path(str(Path(__file__).parent/name),run_name='__main__')
print('All agent4 exact/symbolic checks passed in',time.time()-start,'seconds')
