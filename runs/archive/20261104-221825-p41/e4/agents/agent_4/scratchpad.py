import sys,time,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_cone_shadow_sat import instance
from agent1_shellability import verify_shelling,restriction
from agent3_checker import subsets,verify
from agent2_fastcheck import fast_homology_certificate as cert
from z3 import *
for vbit in [1,8,32]:
 s,fs,t=instance(8,4,stuck=True,seed=True,timeout=110000,vbit=vbit)
 s.add(t[1]==2)
 for a in t:s.add(Implies(a>1,Or([b==a-1 for b in t])))
 a=time.time();res=s.check();print(vbit,res,time.time()-a,flush=True)
 if res==sat:
  mod=s.model();order=tuple(F for _,F in sorted((mod.eval(t[i]).as_long(),F) for i,F in enumerate(fs) if mod.eval(t[i]).as_long()))
  verify_shelling(order)
  K=tuple(sorted({G for F in order for G in subsets(F,3) if not G&vbit}));L=tuple(sorted(F^vbit for F in order if F&vbit))
  assert set(L)<set(K)
  assert all(restriction(L,G) is None for G in K if G not in L)
  c=cert(tuple(sorted(order)),1)
  if c:verify(tuple(sorted(order)),1,c)
  print('SHADOW COUNTER',order,'k1',bool(c),'K',K,'L',L,flush=True)
  Path('workspace/agent4_cone_shadow_stuck.json').write_text(json.dumps({'facets':sorted(order),'order':order,'K':K,'L':L,'vbit':vbit,'cert1':c}))
  break
