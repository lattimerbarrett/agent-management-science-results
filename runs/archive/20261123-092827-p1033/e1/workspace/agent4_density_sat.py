from itertools import combinations
from z3 import *
import time,json,pathlib

def run(m=6,n=7,r=2,B=6,limit=45):
 E=list(map(set,combinations(range(n),r))); N=len(E)
 z=[[Bool(f'a_{i}_{e}') for e in range(N)] for i in range(m)]
 outer=Solver();outer.set(timeout=3000)
 for q in range(1,m+1):
  for C in combinations(range(n),q-1):
   covered=[Not(Or([z[i][e] for e,R in enumerate(E) if not R&set(C)])) for i in range(m)]
   outer.add(PbLe([(b,1) for b in covered],q-1))
 # Break color symmetry by inclusion of an arbitrary edge in first family.
 outer.add(z[0][0])
 x=[Int(f'x_{i}') for i in range(m)]
 low=Solver();low.set(timeout=3000)
 for i in range(m):low.add(x[i]>=0,x[i]<N)
 overlap=[]
 for i,j in combinations(range(m),2):
  overlap.append(Or([And(x[i]==e,x[j]==f) for e in range(N) for f in range(N) if E[e]&E[f]]))
 low.add(PbLe([(b,1) for b in overlap],B))
 start=time.time();cnt=0
 while time.time()-start<limit:
  result=outer.check()
  if result!=sat:
   print('outer result',result,'cuts',cnt,'elapsed',round(time.time()-start,2));return
  model=outer.model(); allowed=[[e for e in range(N) if is_true(model.eval(z[i][e]))] for i in range(m)]
  low.push()
  for i in range(m):low.add(Or([x[i]==e for e in allowed[i]]))
  inner=low.check()
  if inner==unsat:
   print('COUNTEREXAMPLE',m,n,r,B,'cuts',cnt)
   print([[sorted(E[e]) for e in a] for a in allowed])
   pathlib.Path('workspace/agent4_density_counter.json').write_text(json.dumps(allowed));return
  if inner!=sat:
   print('inner',inner,'cuts',cnt);return
  mod=low.model();choice=[mod.eval(a).as_long() for a in x];low.pop()
  cost=sum(bool(E[choice[i]]&E[choice[j]]) for i,j in combinations(range(m),2))
  assert cost<=B
  outer.add(Or([Not(z[i][choice[i]]) for i in range(m)]));cnt+=1
 print('TIME LIMIT cuts',cnt,'elapsed',round(time.time()-start,2))
run()
pathlib.Path('workspace/agent4_density_sat.py').write_text(pathlib.Path('scratchpad.py').read_text())
