import sys,sympy as s
sys.path.insert(0,'workspace')
from agent4_chern_constraints import schur,reduce_xy,x,y
ranks=(1,5,1);weights=(-1,0,1)
coeffs=[s.Integer(1)];vs=[]
for i,(r,w) in enumerate(zip(ranks,weights)):
 C=[s.Integer(1)]
 for j in range(1,r+1):
  c=0
  for a in range(4):
   b=j-a
   if 0<=b<=a:
    v=s.Symbol('c%d_%d%d'%(i,a,b));vs.append(v);c+=v*schur(a,b)
  C.append(c)
 D=[0]*(r+1)
 for j,c in enumerate(C):
  for k in range(r-j+1):D[j+k]+=s.binomial(r-j,k)*(w*x)**k*c
 new=[0]*(len(coeffs)+r)
 for j,a in enumerate(coeffs):
  for k,b in enumerate(D):new[j+k]+=a*b
 coeffs=[reduce_xy(c) for c in new]
target=[1,0,1,0,-5,0,0,0]
eq=[]
for k,c in enumerate(coeffs):
 p=s.Poly(s.expand(c-target[k]*x**k),x,y)
 eq.extend(v for (_,v) in p.terms() if v!=0)
sub={}
while True:
 found=None
 for e in eq:
  for v in reversed(vs):
   d=s.diff(e,v)
   if d!=0 and not d.free_symbols:found=(e,v,d);break
  if found:break
 if not found:break
 e,v,d=found;val=s.expand(v-e/d)
 eq=[s.expand(f.subs(v,val)) for f in eq]
 eq=list(dict.fromkeys(f for f in eq if f!=0));vs.remove(v);sub[v]=val
print('remaining',vs,eq,flush=True)
assert not vs and any(e.is_number and e!=0 for e in eq)
print('Contradiction: no uniform bundle with candidate Chern classes and splitting (-1,0^5,1).')
from pathlib import Path
Path('workspace/agent4_candidate_chern_obstruction.py').write_text(Path('scratchpad.py').read_text())
