from itertools import combinations
from z3 import *

def check(t,r=1,extra=0):
 k=t
 cores=[set(range(i*(k-r),(i+1)*(k-r))) for i in range(t)]
 V=set(range(t*(k-r)+extra))
 edges=[]
 for i,X in enumerate(cores):
  for R in combinations(sorted(V-X),r):
   edges.append((i,X|set(R),Bool(f'e_{i}_{R}')))
 s=Solver()
 for i in range(t):s.add(Or([b for j,F,b in edges if i==j]))
 for a,(i,F,b) in enumerate(edges):
  for j,G,c in edges[a+1:]:
   if not F&G:s.add(Or(Not(b),Not(c)))
 for C in combinations(sorted(V),t-1):
  C=set(C)
  s.add(Or([b for i,F,b in edges if not F&C]))
 result=s.check()
 print('t,r,extra,result',t,r,extra,result)
 if result==sat:
  m=s.model(); chosen=[(i,sorted(F)) for i,F,b in edges if is_true(m.eval(b))]
  assert all(set(F)&set(G) for i,F in chosen for j,G in chosen)
  assert all(any(not set(F)&set(C) for i,F in chosen) for C in combinations(V,t-1))
  print(chosen)
 return result

from itertools import product

def cluster_test(m,n,r,B):
 E=list(map(set,combinations(range(n),r)))
 z=[[Bool(f'a_{i}_{e}') for e in range(len(E))] for i in range(m)]
 s=Solver()
 for q in range(1,m+1):
  for I in combinations(range(m),q):
   for C in combinations(range(n),q-1):
    s.add(Or([z[i][e] for i in I for e,R in enumerate(E) if not R&set(C)]))
 cnt=0
 for choice in product(range(len(E)),repeat=m):
  seen=set(); biggest=0
  for i in range(m):
   if i in seen:continue
   component={i};todo=[i];seen.add(i)
   while todo:
    j=todo.pop()
    for k in range(m):
     if k not in seen and E[choice[j]]&E[choice[k]]:
      seen.add(k);component.add(k);todo.append(k)
   biggest=max(biggest,len(component))
  if biggest<=B:
   cnt+=1;s.add(Or([Not(z[i][choice[i]]) for i in range(m)]))
 print('cluster clauses',cnt,'result',s.check())
 if s.check()==sat:
  model=s.model()
  print([[sorted(E[e]) for e in range(len(E)) if is_true(model.eval(z[i][e]))] for i in range(m)])
cluster_test(4,5,2,2)
import pathlib
pathlib.Path('workspace/agent4_cluster_sat.py').write_text(pathlib.Path('scratchpad.py').read_text())
