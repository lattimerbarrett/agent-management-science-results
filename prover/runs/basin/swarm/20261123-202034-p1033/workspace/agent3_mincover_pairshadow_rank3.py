from itertools import combinations
from z3 import *
from pathlib import Path
import json,time
out=[]
for n in (7,8,9,10):
 r=3;E=[frozenset(e) for e in combinations(range(n),r)]
 x=[Bool('x%d_%d'%(n,i)) for i in range(len(E))]
 b=[Bool('b%d_%d'%(n,i)) for i in range(len(E))]
 s=Solver();s.set(timeout=60000)
 for i,A in enumerate(E):
  for j in range(i):
   if not A&E[j]:s.add(Or(Not(x[i]),Not(x[j])))
 for C in combinations(range(n),r-1):
  C=set(C);s.add(Or([x[i] for i,A in enumerate(E) if not A&C]))
 for i,C in enumerate(E):s.add(b[i]==And([Not(x[j]) for j,A in enumerate(E) if not A&C]))
 for P in combinations(range(n),2):
  P=set(P);s.add(Or([b[i] for i,C in enumerate(E) if P<=C]))
 # Valid anchors edge012 and edge034 private against {1,2}; label symmetry.
 s.add(x[E.index(frozenset((0,1,2)))])
 s.add(x[E.index(frozenset((0,3,4)))])
 t=time.time();ans=s.check();R=dict(n=n,rank=3,result=str(ans),seconds=time.time()-t)
 if ans==sat:
  m=s.model();H=[sorted(A) for i,A in enumerate(E) if is_true(m.eval(x[i]))]
  B=[sorted(C) for i,C in enumerate(E) if is_true(m.eval(b[i]))]
  R.update(edges=H,mincovers=B)
  from scipy.optimize import linprog
  import numpy as np
  M=np.zeros((n,len(B)))
  for j,C in enumerate(B):M[C,j]=1
  lp=linprog(np.zeros(len(B)),A_eq=M,b_eq=np.ones(n),bounds=(0,None),method='highs')
  R['polar_fpm']=lp.success
 out.append(R);print(R,flush=True)
Path('workspace/agent3_mincover_pairshadow_rank3.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_mincover_pairshadow_rank3.json').write_text(json.dumps(out,indent=2))