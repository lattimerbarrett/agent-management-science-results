"""Run the independently verified construction checks from agent3.
This does NOT assert or prove a full determination of S_r;
unresolved lower-bound structure is deliberately not included.
"""
import runpy,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
root=Path(__file__).resolve().parent
for name in ['agent3_h8_checks.py','agent3_h14_checks.py','agent3_h14_cycles.py']:
 print('RUN',name)
 runpy.run_path(str(root/name),run_name='__main__')
for d in range(-1000,1001):
 assert (-d*d+d//2==0)==(d==0)
print('H14 lattice optimization integer test passed; general proof follows d²>|d|/2 for d!=0.')
print('All agent3 verified construction checks PASS.')
