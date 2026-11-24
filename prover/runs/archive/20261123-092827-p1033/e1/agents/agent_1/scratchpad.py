from itertools import combinations,combinations_with_replacement
from z3 import *
import json

def test(k,d):
 t=len(d);X=[];a=0
 for dd in d:X.append(set(range(a,a+k-dd)));a+=k-dd
 V=set(range(a));F=[];col=[]
 for i,dd in enumerate(d):
  for R in combinations(sorted(V-X[i]),dd):F.append(X[i]|set(R));col.append(i)
 B=[Bool(f'b_{i}') for i in range(len(F))];sol=Solver();sol.set(timeout=20000)
 for i in range(t):sol.add(Or([b for b,c in zip(B,col) if c==i]))
 for i,j in combinations(range(len(F)),2):
  if not F[i]&F[j]:sol.add(Or(Not(B[i]),Not(B[j])))
 for C in combinations(V,t-1):
  C=set(C);sol.add(Or([b for b,G in zip(B,F) if not C&G]))
 res=sol.check();print(k,d,'vars',len(F),res,flush=True)
 if res==sat:
  M=sol.model();chosen=[(i,G) for b,i,G in zip(B,col,F) if is_true(M[b])]
  ff=[G for i,G in chosen]
  assert all(A&B for A,B in combinations(ff,2))
  assert all(any(not set(C)&G for G in ff) for C in combinations(V,t-1))
  json.dump({'k':k,'deficits':d,'cores':[sorted(z) for z in X],'chosen':[(i,sorted(G)) for i,G in chosen]},open('workspace/agent1_D5_counter.json','w'))
 return res
from pathlib import Path
Path('workspace/agent1_D5_sat.py').write_text(Path('scratchpad.py').read_text())
for k in [4,5,6]:
 for d in [(1,1,1,1),(1,1,1,2),(0,1,1,1),(0,1,1,2),(0,1,1,3),(0,1,2,2)]:test(k,d)
