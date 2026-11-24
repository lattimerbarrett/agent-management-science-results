import sys,time,json
sys.path.insert(0,'workspace')
from agent4_pairing import partitions
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
from collections import Counter
from math import comb,factorial
from sympy import Matrix
@lru_cache(None)
def df(n):
 z=1
 for i in range(n,0,-2):z*=i
 return z
@lru_cache(None)
def pp(a):
 if not a:return (Q(1),)
 first=a[0];c=Counter(a[1:]);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[Q(0)]*(len(a)+1)
 for vv in product(*(range(v+1) for v in cs)):
  size=1+sum(vv);s=first+sum(k*v for k,v in zip(ks,vv));mult=1
  for c0,v in zip(cs,vv):mult*=comb(c0,v)
  z=Q(mult*(-1)**(size-1),df(2*s+1))
  rem=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
  for j,y in enumerate(pp(rem)):out[j+1]+=z*y
 return tuple(out)
@lru_cache(None)
def value(a):return sum(z*factorial(47+j) for j,z in enumerate(pp(a)))
a=list(partitions(12));b=list(partitions(11));t=time.time()
M=[[value(tuple(sorted(x+y,reverse=True))) for y in b] for x in a]
print('built',time.time()-t,flush=True)
from sympy.polys.matrices import DomainMatrix
D=DomainMatrix.from_Matrix(Matrix(M)).to_field()
E,piv=D.rref()
print('exact rank',len(piv),'seconds',time.time()-t,flush=True)
assert len(piv)==43
json.dump({'basis12':a,'basis11':b,'matrix':[[str(v) for v in r] for r in M]},open('workspace/agent4_pairing_exact.json','w'))
