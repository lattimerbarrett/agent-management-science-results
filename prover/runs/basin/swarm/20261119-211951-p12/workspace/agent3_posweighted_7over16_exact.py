from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from collections import Counter
from math import comb,factorial
from pathlib import Path
import numpy as np,sympy as sp,json,time
from sage.all import GF,matrix,QQ
P=1000003;W=42;start=time.time()
old=json.load(open('workspace/agent3_fz25.json'));cols=[tuple(p) for p in old['columns']];F=QQ;FZ=matrix(F,[[F(QQ(x)) for x in row] for row in old['rows']])
def conv(a,b):return np.convolve(a,b)[:W]
def mul(a,b):
 out={}
 for p,x in a.items():
  for q,y in b.items():
   if sum(p)+sum(q)>12:continue
   r=tuple(sorted(p+q));out[r]=(out.get(r,0)+x*y)
 return {p:x for p,x in out.items() if x}
def run(k,weights):
 q=sp.Rational(k,48);b=Q(48-k,48);A=sum(weights)
 Mom=[np.zeros(W,dtype=object)];Mom[0][0]=1
 for a in range(1,A+1):Mom.append(conv(Mom[-1],np.array([1,(b+a-1)]+[0]*(W-2),dtype=object)))
 @lru_cache(None)
 def cumul(ps):
  a=sum(ps);out=Mom[a].copy();first=ps[0];rest=Counter(ps[1:]);vals=list(rest);cs=[rest[x] for x in vals]
  for ns in product(*(range(c+1) for c in cs)):
   block=tuple(sorted((first,)+tuple(v for v,n in zip(vals,ns) for _ in range(n))))
   if len(block)==len(ps):continue
   mult=1
   for c,n in zip(cs,ns):mult*=comb(c,n)
   out=(out-(mult)*conv(cumul(block),Mom[a-sum(block)]))
  return out
 @lru_cache(None)
 def H(ps):
  if not ps:return {():1}
  first=ps[0];rest=Counter(ps[1:]);vals=list(rest);cs=[rest[x] for x in vals];out={}
  for ns in product(*(range(c+1) for c in cs)):
   block=tuple(sorted((first,)+tuple(v for v,n in zip(vals,ns) for _ in range(n))));remain=tuple(v for v,c,n in zip(vals,cs,ns) for _ in range(c-n));mult=1
   for c,n in zip(cs,ns):mult*=comb(c,n)
   cumulpoly=cumul(block);m=len(block)
   L={(() if j==0 else (j,)):cumulpoly[m+j]*(-1)**(j+1)*(48 if j==0 else 1)*mult for j in range(13)}
   for p,x in mul(L,H(tuple(sorted(remain)))).items():out[p]=(out.get(p,0)+x)
  return {p:x for p,x in out.items() if x}
 C={():1}
 for m in range(1,13):
  z=(-1)**(m-1)*sp.bernoulli(m+1,q)/m/(m+1);coef=Q(int(z.p),int(z.q))
  C=mul(C,{(m,)*a:coef**a/Q(factorial(a)) for a in range(12//m+1)})
 poly=mul(C,H(tuple(sorted(weights))));row=[poly.get(p,0) for p in cols]
 print('degree',k,'weights',Counter(weights),'row_nonzero',sum(bool(x) for x in row),'rank',FZ.stack(matrix(F,[row])).rank(),'seconds',time.time()-start,flush=True)
 return row

row=run(21,(2,)*14)
