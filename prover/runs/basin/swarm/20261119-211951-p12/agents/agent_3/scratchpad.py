from fractions import Fraction as Q
from math import factorial,comb
from functools import lru_cache
from collections import Counter
from itertools import product
from pathlib import Path
import json,time,gc
from sage.all import matrix,GF
N=12;g=12;prime=65521;F=GF(prime);start=time.time()
@lru_cache(None)
def parts(n,lo=1):
 if n<0:return ()
 if n==0:return ((),)
 return tuple((i,)+p for i in range(lo,n+1) for p in parts(n-i,i))
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),-1,prime)%prime
A=[factorial(6*n)//(factorial(3*n)*factorial(2*n))%prime for n in range(N+1)]
B=[a*(6*n+1)*pow(6*n-1,-1,prime)%prime for n,a in enumerate(A)]
def conv(a,b):
 c=[0]*(N+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b[:N+1-i]):c[i+j]=(c[i+j]+x*y)%prime
 return c
inv=[1]+[0]*N
for n in range(1,N+1):inv[n]=-sum(A[i]*inv[n-i] for i in range(1,n+1))%prime
D=conv(B,inv);logA=[0]+[sum(i*A[i]*inv[n-i] for i in range(1,n+1))*pow(n,-1,prime)%prime for n in range(1,N+1)]
Dpow=[[1]+[0]*N]
for k in range(1,25):Dpow.append(conv(Dpow[-1],D))
def mul(a,b):
 c={}
 for p,x in a.items():
  for q,y in b.items():
   if sum(p)+sum(q)<=N:
    r=tuple(sorted(p+q));c[r]=(c.get(r,0)+x*y)%prime
 return {p:x for p,x in c.items() if x}
P={():1}
for n in range(1,N+1):P=mul(P,{(n,)*k:pow(-logA[n],k,prime)*pow(factorial(k),-1,prime)%prime for k in range(N//n+1)})
@lru_cache(None)
def H(sig,k0):
 if not sig:return P
 first=sig[0];cc=Counter(sig[1:]);vals=list(cc);cs=[cc[v] for v in vals];out={}
 for ns in product(*(range(c+1) for c in cs)):
  block=(first,)+tuple(v for v,n in zip(vals,ns) for _ in range(n));rest=tuple(v for v,c,n in zip(vals,cs,ns) for _ in range(c-n));mult=1
  for c,n in zip(cs,ns):mult*=comb(c,n)
  shift=sum(x//3 for x in block);b=sum(x%3==1 for x in block)
  L={(() if n==0 else (n,)):Dpow[b][n-shift]*(k0 if n==0 else 1)*factorial(len(block)-1)*mult%prime for n in range(shift,N+1) if Dpow[b][n-shift]}
  for p,x in mul(L,H(tuple(sorted(rest)),k0)).items():out[p]=(out.get(p,0)+x)%prime
 return {p:x for p,x in out.items() if x}
def pcols(d):return [(p,a,d-sum(p)-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
def rcols(d):return [(p,d-sum(p)) for k in range(d+1) for p in parts(k)]
prim=[];rootprim=[]
for r in range(1,N+1):
 for a1,a2 in product(range(2),repeat=2):
  for weight in range(3*r-g-a1-a2):
   if (r+weight+a1+a2)%2!=1:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    rel={}
    for p,x in H(sig,2*g).items():
     d=sum(p)
     if d>r:continue
     for e in range(r-d+1):
      f=r-d-e;y=x*(A if a1==0 else B)[e]*(A if a2==0 else B)[f]%prime
      if y:rel[p,e,f]=y
    tail={};s=sig.count(1)
    for m in range(s+1):
     fac=(-1)**(m+a1+a2)*factorial(s)//factorial(s-m);even=(m+a1+a2)%2==0
     for p,x in H(sig[m:],2*g-1).items():
      l=r-sum(p)
      if l<1:continue
      key=p,l-1;tail[key]=(tail.get(key,0)+x*fac*(-A[l] if even else B[l]))%prime
    prim.append((r,rel,tail))
 for a in range(2):
  for weight in range(3*r-g-a):
   if (r+weight+a)%2!=1:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    rel={}
    for p,x in H(sig,2*g-1).items():
     d=sum(p)
     if d<=r:
      y=x*(A if a==0 else B)[r-d]%prime
      if y:rel[p,r-d]=y
    rootprim.append((r,rel))
 print('primitivesr',r,len(prim),len(rootprim),'cache',H.cache_info().currsize,'seconds',time.time()-start,flush=True)
expected=[1,4,9,18,33,52,62,52,33,18,9,4,1];results=[]
for d in range(N+1):
 cs=pcols(d);ds=rcols(d-1);ix={p:i for i,p in enumerate(cs)};di={p:len(cs)+i for i,p in enumerate(ds)};nc=len(cs)+len(ds);rows=[]
 for r,rel,tail in prim:
  if r>d:continue
  for q,a,b in pcols(d-r):
   row={ix[tuple(sorted(p+q)),e+a,f+b]:x for (p,e,f),x in rel.items()}
   if a==b==0:
    row.update({di[tuple(sorted(p+q)),k]:x for (p,k),x in tail.items()})
   rows.append(row)
 for r,rel in rootprim:
  if r>d-1:continue
  for q,k in rcols(d-1-r):rows.append({di[tuple(sorted(p+q)),e+k]:x for (p,e),x in rel.items()})
 if rows:
  import random
  random.Random(2025).shuffle(rows)
  totalrows=len(rows);rows=rows[:2000]
  print('TOP subset',len(rows),'of',totalrows,'columns',nc,flush=True)
  R=matrix(F,len(rows),nc,{(i,j):v for i,row in enumerate(rows) for j,v in row.items()},sparse=False);rank=int(R.rank());del R;gc.collect()
 else:rank=0
 dim=nc-rank;results.append({'degree':d,'rows':len(rows),'columns':nc,'rank':rank,'upper_dimension':dim,'expected':expected[d]})
 print('DEGREE',d,'rows',len(rows),'cols',nc,'rank',rank,'upper',dim,'expected',expected[d],'seconds',time.time()-start,flush=True)
json.dump({'genus':g,'prime':prime,'results':results},open('workspace/agent3_rt12_dimensions.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_rt12_dimensions.py').write_text(Path(__file__).read_text())
