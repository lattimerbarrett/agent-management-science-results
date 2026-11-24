from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb,factorial,prod
P=1000003
weights={a:pow(prod(range(1,2*a+2,2)),P-2,P) for a in range(25)}
@lru_cache(None)
def bell(mu):
 if not mu:return (1,)
 co=Counter(mu[1:]);keys=tuple(co);out=[0]*(len(mu)+1)
 for ns in product(*(range(co[k]+1) for k in keys)):
  s=mu[0]+sum(k*n for k,n in zip(keys,ns));rem=tuple(sorted(k for k,n in zip(keys,ns) for _ in range(co[k]-n)))
  c=prod(comb(co[k],n) for k,n in zip(keys,ns))*weights[s]%P
  for j,v in enumerate(bell(rem)):out[j+1]=(out[j+1]+c*v)%P
 return tuple(out)
@lru_cache(None)
def I(mu,a,b=None):
 n=len(mu);offset=46 if b is None else 47
 den=prod(range(1,2*a,2))*(1 if b is None else prod(range(1,2*b,2)))
 return sum((-1)**(n-k)*factorial(offset+k)*v for k,v in enumerate(bell(mu)))*pow(den,P-2,P)%P

def dual_values(beta,rho,targetmons,symmetrized=True):
 # beta rows=(kappa_partition,a,b,coefficient); rho rows=(kappa_partition,a,coefficient).
 # symmetrized means each beta row with a!=b denotes sum of both swaps.
 A=[];B=[]
 for m in targetmons:
  A.append(sum(c*(2 if symmetrized and a!=b else 1)*I(tuple(sorted(tuple(p)+tuple(m))),a,b) for p,a,b,c in beta)%P)
  r=m.count(1);mm=list(m)
  if r:mm.remove(1)
  B.append(sum(c*(I(tuple(sorted(tuple(p)+tuple(m))),a)-(r*I(tuple(sorted(tuple(p)+tuple(mm))),a+1) if r else 0)) for p,a,c in rho)%P)
 return A,B

