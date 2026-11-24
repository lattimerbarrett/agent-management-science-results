import sys
sys.path.insert(0,'workspace')
from agent2_derivations import elementary, degree2_columns
from itertools import combinations
from functools import reduce
import z3
n=4; E=elementary(n); m=len(E); pairs=list(combinations(range(m),2)); cols=degree2_columns(n)
piv={}; ker=[]
for j,c in enumerate(cols):
 d={k for k,v in c.items() if v%2}; v={j}
 while d:
  a=min(d)
  if a not in piv:piv[a]=(d,v); break
  dc,vc=piv[a]; d^=dc; v^=vc
 else:ker.append(v)
r=[z3.Bool('r%d'%i) for i in range(m)]
s=[z3.Bool('s%d'%i) for i in range(m)]
S=z3.Solver()
for v in ker:
 terms=[]
 for k in v:
  i,j=pairs[k]; terms.extend([z3.And(r[i],s[j]),z3.And(r[j],s[i])])
 S.add(z3.Not(reduce(z3.Xor,terms)))
S.add(z3.Or(*[z3.Xor(z3.And(r[i],s[j]),z3.And(r[j],s[i])) for i,j in pairs]))
assert S.check()==z3.unsat
print('n=4: no nonzero decomposable 2-form lies in rowspace of Johnson2 bracket matrix over F2')
