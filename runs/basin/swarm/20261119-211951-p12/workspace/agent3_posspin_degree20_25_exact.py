k=20
from math import factorial
from fractions import Fraction as Q
from functools import lru_cache
import json,time,pickle
import sympy as sp
from sage.all import matrix,GF,QQ
P=1000000007;N=21;D=N+12;a=Q(-20,48);start=time.time()
def conv(a,b):
 c=[0]*(D+1)
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b[:D+1-i]):c[i+j]+=x*y
 return c
Z=[[1]+[0]*D];den=[1]+[0]*D
for n in range(1,N+1):
 aa=a+n-1
 for d in range(D,0,-1):den[d]=den[d]-(Q(k,48)+n-1)*den[d-1]
 invfac=Q(1,factorial(n));Z.append([x*invfac for x in den])
L=[[0]*(D+1)]
for n in range(1,N+1):
 v=Z[n][:]
 for k in range(1,n):
  prod=conv(L[k],Z[n-k]);fac=Q(k,n)
  v=[x-fac*y for x,y in zip(v,prod)]
 L.append(v)
 assert all(v[d]==0 for d in range(n-1)),(n,v[:n])
f=[[0]*(N+1) for j in range(13)]
for j in range(13):
 for n in range(1,N+1):f[j][n]=(-1)**(j+1)*L[n][n+j]
assert f[0][1]==Q(k,48) and all(f[j][1]==0 for j in range(1,13))
print('logseries',time.time()-start,flush=True)
def mul(a,b):
 c={}
 for p,x in a.items():
  for q,y in b.items():
   if sum(p)+sum(q)<=12:
    r=tuple(sorted(p+q));c[r]=c.get(r,0)+x*y
 return {p:x for p,x in c.items() if x}
E=[{():1}]
for n in range(1,N+1):
 out={}
 for k in range(1,n+1):
  sk={():48*f[0][k]}
  for j in range(1,13):sk[(j,)]=f[j][k]
  for p,x in mul(sk,E[n-k]).items():out[p]=out.get(p,0)+k*x
 inv=Q(1,n);E.append({p:x*inv for p,x in out.items() if x})
C={():1}
for m in range(1,13):
 z=sp.bernoulli(m+1,sp.Rational(20,48));coef=(-1)**m*Q(int(z.p),int(z.q)*m*(m+1))
 factor={tuple([m]*k):coef**k/Q(factorial(k)) for k in range(12//m+1)}
 C=mul(C,factor)
print('polynomials',time.time()-start,flush=True)
old=json.load(open('workspace/agent3_fz25.json'));cols=[tuple(p) for p in old['columns']]
def mod(x):
 x=Q(x);return x.numerator*pow(x.denominator,-1,P)%P
oldrows=[[Q(x) for x in row] for row in old['rows']]
rows=[]
for n in range(21,22):
 rel=mul(C,E[n]);row=[rel.get(p,0) for p in cols];rows.append(row)
 print('n',n,'combinedrank',matrix(QQ,oldrows+rows).rank(),flush=True)
pickle.dump({'rows':rows,'columns':cols,'prime':P,'ns':list(range(21,22))},open('workspace/agent3_posspin_degree20_25_exact.pkl','wb'))
