import sys,math
sys.path.insert(0,'workspace')
import agent3_lower as L
from fractions import Fraction
G=24
from functools import lru_cache
@lru_cache(None)
def I(mu):
 n=len(mu)
 return sum((-1)**(n-k)*math.factorial(45+k)*v for k,v in enumerate(L.exact_bell(mu)))
def kappa(mu):
 nz=tuple(sorted((x for x in mu if x),reverse=True));return 46**mu.count(0)*I(nz)
def base_moment(mu,a,b):
 return kappa(mu+(a-1,b-1))+kappa(mu+(a+b-2,))
def direct(mu,a,b):
 n=len(mu)
 return sum((-1)**(n-k)*math.factorial(47+k)*v for k,v in enumerate(L.exact_bell(mu)))/Fraction(math.prod(range(1,2*a,2))*math.prod(range(1,2*b,2)))
mu=(2,);a=b=11
expanded=base_moment(mu,a,b)+base_moment((),a+2,b)+base_moment((),a,b+2)
print('Direct',direct(mu,a,b));print('Expanded',expanded);print('Equal?',expanded==direct(mu,a,b))
from itertools import product
import random
cases=[]
for s in range(23):
 for mu in L.partitions(s):
  if len(mu)>5:continue
  for a in range(1,24-s):cases.append((mu,a,24-s-a))
random.seed(25);cases=random.sample(cases,100)
for mu,a,b in cases:
 ex=0
 for ass in product(range(3),repeat=len(mu)):
  base=tuple(m for m,j in zip(mu,ass) if j==0)
  aa=a+sum(m for m,j in zip(mu,ass) if j==1)
  bb=b+sum(m for m,j in zip(mu,ass) if j==2)
  ex+=base_moment(base,aa,bb)
 assert ex==direct(mu,a,b),(mu,a,b,ex,direct(mu,a,b))
print('100 independent exact expansion checks passed')
