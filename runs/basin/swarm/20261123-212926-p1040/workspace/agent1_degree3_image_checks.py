"""Primitive integral degree<=3 Johnson-image certificate.
Primitivity: echelon max minor has only prime factor2; mod2 rank is full.
No source injectivity is claimed.
"""
from agent1_integral_derivations import generators,bracket,UnitLattice
from agent3_derivations import basis
from agent1_support_checks import lie,lyndon
from itertools import product

def necklace(w):return min(w[i:]+w[:i] for i in range(len(w)))
def check(n):
 gs=generators(n);bs=gs
 for d in [2,3]:
  L=UnitLattice()
  for a in gs:
   for b in bs:L.insert(bracket(a,b))
  bs=list(L.b.values());pivs=[v[p] for p,v in L.b.items()]
  assert all(x in [1,2] for x in pivs)
  mod2=len(basis(({k:x%2 for k,x in b.items() if x%2} for b in bs),2))
  assert mod2==len(bs)
  for b in bs:
   tr={}
   for (i,w),v in b.items():
    if w[0]==i:
     key=necklace(w[1:]);tr[key]=tr.get(key,0)+v
   assert all(x==0 for x in tr.values())
  expected=(n*n*(n*n-1)//3-n*(n+1)//2) if d==2 else n*(n**4-n*n)//4-(n**3+2*n)//3
  assert len(bs)==expected
  print('primitive integral image',n,d,len(bs),'minor2exponent',pivs.count(2),'mod2rank',mod2,flush=True)
 # Trace surjectivity, using integer gcd-echelon on cyclic target.
 T=UnitLattice()
 for w in product(range(n),repeat=4):
  if not lyndon(w):continue
  p=lie(w)
  for i in range(n):
   col={}
   for v,c in p.items():
    if v[0]==i:
     key=necklace(v[1:]);col[key]=col.get(key,0)+c
   T.insert({k:v for k,v in col.items() if v})
 assert len(T.b)==(n**3+2*n)//3
 assert all(v[p]==1 for p,v in T.b.items())
 print('cyclic trace is onto',n,len(T.b),flush=True)
if __name__=='__main__':
 for n in range(2,7):check(n)
