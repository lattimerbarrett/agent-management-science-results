from functools import lru_cache
from math import factorial,prod
from collections import Counter
from sympy import bernoulli
from agent1_hodge_mod import P,Q,b,splits as old_splits
splits=lru_cache(maxsize=128)(old_splits.__wrapped__)
from math import factorial
BERN={m:Q(bernoulli(m+1),m+1) for m in range(1,50,2)}
@lru_cache(None)
def odd_df(n):
 return prod(range(n,0,-2))
@lru_cache(None)
def topconst(g):return Q(abs(bernoulli(2*g)),2**(2*g-1)*factorial(2*g))

def J(g,k,ds=()):return _J(g,k,tuple(sorted(ds)))
@lru_cache(None)
def _J(g,k,ds):
 n=len(ds)
 if k<0 or k>g or 2*g-2+n<=0 or sum(ds)+k!=2*g-3+n:return 0
 if g>0 and k==g:return 0
 if k==0:
  if g==0:return Q(factorial(n-3),prod(factorial(d) for d in ds))
  return b(g)*Q(factorial(sum(ds)),prod(factorial(d) for d in ds))%P
 if ds and ds[0]==0:
  rest=ds[1:];v=0
  for d,c in Counter(rest).items():
   if d:
    dd=list(rest);dd.remove(d);dd.append(d-1);v+=c*J(g,k,dd)
  return v%P
 if 1 in ds:
  dd=list(ds);dd.remove(1)
  return (2*g-3+n)*J(g,k,dd)%P
 if g>1 and k==g-1:
  return topconst(g)*Q(factorial(2*g-3+n),prod(odd_df(2*d-1) for d in ds))%P
 out=0
 for m in range(k if k%2 else k-1,0,-2):
  kk=k-m
  v=J(g,kk,ds+(m+1,))
  for d,c in Counter(ds).items():
   dd=list(ds);dd.remove(d);dd.append(d+m)
   v-=c*J(g,kk,dd)
  boundary=0
  for ga in range(g+1):
   gb=g-ga
   for da,db,cm in splits(ds):
    na=len(da);nb=len(db)
    if 2*ga-1+na<=0 or 2*gb-1+nb<=0:continue
    for ia in range(max(0,kk-gb),min(ga,kk)+1):
     ib=kk-ia;r=2*ga-2+na-sum(da)-ia
     if not 0<=r<m:continue
     x=J(ga,ia,da+(r,))
     if x:boundary+=(-1)**r*cm*x*J(gb,ib,db+(m-1-r,))
  v+=boundary*pow(2,-1,P)
  out+=BERN[m]*v
 return out*pow(k,-1,P)%P
