from functools import lru_cache
from math import factorial,comb
from itertools import product
from sage.all import GF,matrix
from pathlib import Path
import json,time
p=1000000007;F=GF(p);start=time.time()
invdf={};v=1
for d in range(26):
 if d:v=v*(2*d+1)%p
 invdf[d]=pow(v,-1,p)
fact=[factorial(i)%p for i in range(90)]
@lru_cache(None)
def parts(n,lo=1):
 if n==0:return ((),)
 return tuple((i,)+q for i in range(lo,n+1) for q in parts(n-i,i))
@lru_cache(None)
def poly(ps):
 if not ps:return (1,)
 a=ps[0];vs=sorted(set(ps[1:]));cs=[ps[1:].count(v) for v in vs];out=[0]*(len(ps)+1)
 for ns in product(*(range(c+1) for c in cs)):
  block=a+sum(v*n for v,n in zip(vs,ns));b=sum(ns);mult=1;rem=[]
  for v,c,n in zip(vs,cs,ns):mult=mult*comb(c,n)%p;rem +=[v]*(c-n)
  w=mult*invdf[block]*(-1)**b%p
  for k,c in enumerate(poly(tuple(rem))):out[k+1]=(out[k+1]+w*c)%p
 return tuple(out)
@lru_cache(None)
def L(h,ps,e):
 assert sum(ps)+e==h-1
 q=poly(ps);D=sum(ps)
 if e:return sum(a*fact[2*h-2+m] for m,a in enumerate(q))%p*invdf[e-1]%p
 return sum(a*fact[2*h-3+m]*(2*D+m) for m,a in enumerate(q))%p
@lru_cache(None)
def mons(d):return tuple((a,d-k) for k in range(d+1) for a in parts(k))
records=[]
for h in range(2,25):
 for d in range(1,min(12,h-1)+1):
  if h>2*d:continue
  b=h-1-d;rows=mons(b);cols=mons(d-1)
  A=matrix(F,[[L(h,tuple(sorted(a+c)),e+f+1) for c,f in cols] for a,e in rows])
  B=matrix(F,[[L(h,tuple(sorted(a+c)),e) for c in parts(d)] for a,e in rows])
  r=A.rank();r2=A.augment(B).rank();records.append([h,d,b,len(rows),len(cols),r,r2])
  if r2>r:print('EXCEPTION',records[-1],flush=True)
 print('h',h,'done','sec',time.time()-start,flush=True)
print('cases',len(records),'exceptions',sum(r[-1]>r[-2] for r in records),'sec',time.time()-start,flush=True)
json.dump({'prime':p,'records':records},open('workspace/agent4_framed_obstruction25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_framed_obstruction25.py').write_text(Path(__file__).read_text())
