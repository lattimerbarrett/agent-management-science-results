"""Exact proof certificates. Run python RUN_ALL.py in Sage-enabled Python.
--fast omits only the recorded local4 order6..13 enumeration."""
import os,sys,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT);sys.path.insert(0,str(ROOT/'workspace'))
def run(name):
 print('\n===',name,'===',flush=True)
 runpy.run_path(str(ROOT/'workspace'/name),run_name='__main__')
for f in ['check_even_terminals.py','check_chain_small_atoms_agent4.py','check_cap_uniform_tail.py','check_d5_tail9_cap7.py','check_d5_tail10_agent1.py','check_d6_tail4_agent4.py','check_d8_ordinary_atoms_agent3.py']:
 run(f)
if '--fast' not in sys.argv:
 from enumerate_local4_sage import exact_sage
 from sage.all import QQ
 caps=['4/5','104/115','36/35','52/45','31/20','91/55','9/5','343/180']
 mids=['5/4','4/3','3/2','19/12','2','25/12','9/4','7/3']
 for n in range(6,14):
  for p,table in [(1,caps),(2,mids)]:
   r=exact_sage(n,p)
   assert QQ(r['maximum'])==QQ(table[n-6]),r
   print('LOCAL4',r,flush=True)
for f in ['check_dense_agent1.py','check_even6_agent1.py','check_even_degree7plus.py','check_odd10plus_agent1.py','check_odd_minplus_agent1.py','check_odd6_independent_agent3.py','check_d8_core_agent2.py','check_d8_endpoints_agent4.py','check_d8_independent_agent3.py','check_d8_merris_agent1.py']:
 run(f)
run('odd_construction.py')
print('\nALL PROOF CERTIFICATES PASSED.',flush=True)
