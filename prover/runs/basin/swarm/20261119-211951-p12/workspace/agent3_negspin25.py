from math import factorial
from fractions import Fraction as Q
from functools import lru_cache
import json,time,pickle
import sympy as sp
from sage.all import matrix,GF
P=1000000007;N=23;D=N+12;a=3*pow(2,-1,P)%P;start=time.time()
def conv(a,b):
 c=[0]*(D+1)
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b[:D+1-i]):c[i+j]=(c[i+j]+x*y)%P
 return c
Z=[[1]+[0]*D];den=[1]+[0]*D
for n in range(1,N+1):
 aa=(a+n-1)%P
 for d in range(1,D+1):den[d]=(den[d]-aa*den[d-1])%P
 invfac=pow(factorial(n),-1,P);Z.append([x*invfac%P for x in den])
L=[[0]*(D+1)]
for n in range(1,N+1):
 v=Z[n][:]
 for k in range(1,n):
  prod=conv(L[k],Z[n-k]);fac=k*pow(n,-1,P)%P
  v=[(x-fac*y)%P for x,y in zip(v,prod)]
 L.append(v)
 assert all(v[d]==0 for d in range(n-1)),(n,v[:n])
f=[[0]*(N+1) for j in range(13)]
for j in range(13):
 for n in range(1,N+1):f[j][n]=(-1)**(j+1)*L[n][n+j]%P
assert all(f[j][1]==pow(a,j+1,P) for j in range(13))
print('logseries',time.time()-start,flush=True)
def mul(a,b):
 c={}
 for p,x in a.items():
  for q,y in b.items():
   if sum(p)+sum(q)<=12:
    r=tuple(sorted(p+q));c[r]=(c.get(r,0)+x*y)%P
 return {p:x for p,x in c.items() if x}
E=[{():1}]
for n in range(1,N+1):
 out={}
 for k in range(1,n+1):
  sk={():48*f[0][k]%P}
  for j in range(1,13):sk[(j,)]=f[j][k]
  for p,x in mul(sk,E[n-k]).items():out[p]=(out.get(p,0)+k*x)%P
 inv=pow(n,-1,P);E.append({p:x*inv%P for p,x in out.items() if x})
C={():1}
for m in range(1,13):
 z=sp.bernoulli(m+1,sp.Rational(-1,2));coef=(-1)**m*int(z.p)*pow(int(z.q)*m*(m+1),-1,P)%P
 factor={tuple([m]*k):pow(coef,k,P)*pow(factorial(k),-1,P)%P for k in range(12//m+1)}
 C=mul(C,factor)
print('polynomials',time.time()-start,flush=True)
old=json.load(open('workspace/agent3_fz25.json'));cols=[tuple(p) for p in old['columns']]
def mod(x):
 x=Q(x);return x.numerator*pow(x.denominator,-1,P)%P
oldrows=[[mod(x) for x in row] for row in old['rows']]
rows=[]
for n in range(19,24):
 rel=mul(C,E[n]);row=[rel.get(p,0) for p in cols];rows.append(row)
 print('n',n,'combinedrank',matrix(GF(P),oldrows+rows).rank(),flush=True)
pickle.dump({'rows':rows,'columns':cols,'prime':P,'ns':list(range(19,24))},open('workspace/agent3_negspin25.pkl','wb'))
from pathlib import Path
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_negspin25.py').write_text(Path(__file__).read_text())
