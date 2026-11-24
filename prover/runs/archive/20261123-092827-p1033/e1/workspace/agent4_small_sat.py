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
for t in range(2,6):check(t,extra=2)
import pathlib
pathlib.Path('workspace/agent4_small_sat.py').write_text(pathlib.Path('scratchpad.py').read_text())
