import numpy as np,json,time,itertools
from functools import lru_cache
from collections import Counter
from math import comb,factorial
from sage.all import GF,matrix,QQ
from pathlib import Path
P=1000003;W=36;N=24;deg=12;b=3*pow(2,P-2,P)%P
start=time.time()
def conv(a,c,L=None):
 if L is None:L=len(a)
 return np.convolve(a,c)[:L]%P
def unit(L):
 z=np.zeros(L,dtype=np.int64);z[0]=1;return z
Mom=[unit(W)]
for A in range(1,24):
 v=(b+A-1)%P;factor=np.array([pow((-v)%P,k,P) for k in range(W)],dtype=np.int64)
 Mom.append(conv(Mom[-1],factor))
@lru_cache(None)
def cumul(weights):
 A=sum(weights);c=Mom[A].copy();first=weights[0];rest=weights[1:];vals=sorted(set(rest));cs=[rest.count(x) for x in vals]
 for ns in itertools.product(*(range(n+1) for n in cs)):
  block=(first,)+tuple(x for x,n in zip(vals,ns) for _ in range(n))
  if len(block)==len(weights):continue
  mult=1
  for a,n in zip(cs,ns):mult=mult*comb(a,n)%P
  c=(c-mult*conv(cumul(tuple(sorted(block))),Mom[A-sum(block)]))%P
 return c
@lru_cache(None)
def gfun(sig):
 weights=tuple(sorted(a for a,r in sig));R=sum(r for a,r in sig)
 return gfun_wr(weights,R)
@lru_cache(None)
def gfun_wr(weights,R):
 out=[np.zeros(N,dtype=np.int64) for j in range(13)]
 for n in range(24-sum(weights)):
  ww=tuple(sorted((1,)*n+weights));m=len(ww)
  if not m:continue
  c=cumul(ww);nf=pow(factorial(n)%P,P-2,P)
  for k in range(13):
   j=k-R
   if j>=-1:out[k][n]=int(c[m+j])*nf*((-1)**(j+1))%P
 return out

def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in parts(n-a,a):yield (a,)+t
PP=[list(parts(d)) for d in range(13)];allparts=sum(PP,[])
# C(V0) exponential coefficients.
import sympy as sp
G=[v.copy() for v in gfun(())]
for j in range(1,13):
 q=sp.bernoulli(j+1,sp.Rational(-1,2))*((-1)**j)/j/(j+1)
 G[j][0]=int(q.p)*pow(int(q.q),P-2,P)%P
A=48*G[0]%P;base=[1]
for n in range(1,N):base.append(sum(k*int(A[k])*base[n-k] for k in range(1,n+1))*pow(n,P-2,P)%P)
base=np.array(base,dtype=np.int64)
@lru_cache(None)
def ecoeff(ks):
 c=base.copy()
 for j,m in Counter(ks).items():
  for _ in range(m):c=conv(c,G[j])
  c=c*pow(factorial(m)%P,P-2,P)%P
 return c
@lru_cache(None)
def H(sig):
 if not sig:return {():unit(N)}
 first=sig[0];rest=sig[1:];vals=sorted(set(rest));cs=[rest.count(x) for x in vals];out={}
 for ns in itertools.product(*(range(n+1) for n in cs)):
  block=tuple(sorted((first,)+tuple(x for x,n in zip(vals,ns) for _ in range(n))))
  remain=tuple(x for x,c,n in zip(vals,cs,ns) for _ in range(c-n))
  mult=1
  for a,n in zip(cs,ns):mult=mult*comb(a,n)%P
  gf=gfun(block)
  for ks,pol in H(remain).items():
   sd=sum(ks)
   for j in range(13-sd):
    fac=mult*(48 if not j else 1)%P
    newks=tuple(sorted(ks+((j,) if j else ())))
    term=conv(pol,gf[j])*fac%P
    if newks in out:out[newks]=(out[newks]+term)%P
    else:out[newks]=term
 return out

cols=PP[12];ix={p:i for i,p in enumerate(cols)}
q=json.load(open('workspace/agent3_fz25.json'));F=GF(P);FZ=matrix(F,[[F(QQ(x)) for x in row] for row in q['rows']]).echelon_form()
piv=FZ.pivots();FZ=FZ[:len(piv),:];ER=[np.array([int(x) for x in row],dtype=np.int64) for row in FZ]
types=sorted((a,r) for a in range(1,11) for r in range(10) if 1<=a+r-1<=9)
def pats(cost,lo=0):
 if not cost:yield ()
 for i in range(lo,len(types)):
  a,r=types[i];c=a+r-1
  if c<=cost:
   for rest in pats(cost-c,i):yield ((a,r),)+rest
checked=0;nonzero=0;outside=[]
for cost in range(10):
 for sig in pats(cost):
  SS=sum(a for a,r in sig);RR=sum(r for a,r in sig);ell=len(sig)
  hp=H(sig)
  for d in range(1,13):
   nns=[n for n in range(24-SS) if 2*n+SS+ell+d-RR>48]
   if not nns:continue
   rs={p:np.zeros(N,dtype=np.int64) for p in PP[d]}
   for ks,c in hp.items():
    sd=sum(ks)
    if sd>d:continue
    for other in PP[d-sd]:
     kk=tuple(sorted(ks+other));rs[kk]=(rs[kk]+conv(c,ecoeff(other)))%P
   for n in nns:
    for extra in PP[12-d]:
     row=np.zeros(77,dtype=np.int64)
     for ks,c in rs.items():row[ix[tuple(sorted(ks+extra))]]=int(c[n])
     checked+=1
     if not np.any(row):continue
     nonzero+=1;red=row.copy()
     for p,e in zip(piv,ER):
      if red[p]:red=(red-int(red[p])*e)%P
     if np.any(red):
      outside.append({'label':(d,n,sig,extra),'row':row.tolist()})
      print('NEW RELATION OUTSIDE FZ',outside[-1]['label'],flush=True)
      raise RuntimeError('Potential breakthrough: inspect outside relation')
 print('cost',cost,'patterns/cache',H.cache_info(),'checked',checked,'nonzero',nonzero,'seconds',time.time()-start,flush=True)
print('ALL COMBINED WEIGHT+K INSERTIONS IN FZ SPAN:',checked,nonzero,flush=True)
json.dump({'prime':P,'checked':checked,'nonzero':nonzero,'outside':outside},open('workspace/agent2_full_negspin25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_full_negspin25.py').write_text(Path(__file__).read_text())
