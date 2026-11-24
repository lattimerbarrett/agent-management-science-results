from z3 import *
from itertools import combinations

def test(t=3,k=4,r=2,extra=0):
 cores=[set(range(i*(k-r),(i+1)*(k-r))) for i in range(t)]
 V=set(range(t*(k-r)+extra)); E=[]
 for i,X in enumerate(cores):
  for R in combinations(V-X,r):E.append((i,frozenset(X|set(R))))
 B={a:Bool(str(a)) for a in E}; S=Solver()
 for i in range(t):S.add(Or([B[a] for a in E if a[0]==i]))
 for ai,a in enumerate(E):
  for b in E[ai+1:]:
   if not a[1]&b[1]:S.add(Or(Not(B[a]),Not(B[b])))
 for C in combinations(V,t-1):S.add(Or([B[a] for a in E if not a[1]&set(C)]))
 x,y=0,1
 for C in combinations(V-{y},t-1):
  if x not in C:continue
  C=set(C);S.push()
  for i,F in E:
   if F&C:continue
   if y not in F:S.add(Not(B[(i,F)]));continue
   G=frozenset((F-{y})|{x})
   if (i,G) in B:S.add(Or(Not(B[(i,F)]),Not(B[(i,G)])))
  if S.check()==sat:
   m=S.model();chosen=[(i,sorted(F)) for i,F in E if is_true(m.eval(B[(i,F)]))]
   print('SHIFT LOWERS TAU',t,k,r,extra,C,chosen);return
  S.pop()
 print('NO EXAMPLE',t,k,r,extra)
test(extra=2)
# Independently validate a fixed SAT-produced witness and its compression.
F=[{0,1,2,4},{0,1,2,5},{0,1,3,4},{0,1,3,5},{0,2,3,4},{0,2,3,5},{1,2,3,6},{2,3,4,5},{0,2,4,5},{0,3,4,5},{1,4,5,6}]
assert all(A&B for A in F for B in F)
assert all(any(not A&set(C) for A in F) for C in combinations(range(8),2))
FF={frozenset(A) for A in F}; shifted=set()
for A in FF:
 B=frozenset((A-{1})|{0})
 shifted.add(B if 1 in A and 0 not in A and B not in FF else A)
assert all(A&{0,2} for A in shifted)
print('Fixed compression counterexample verified exhaustively')
import pathlib
pathlib.Path('workspace/agent4_shift_counter.py').write_text(pathlib.Path('scratchpad.py').read_text())
