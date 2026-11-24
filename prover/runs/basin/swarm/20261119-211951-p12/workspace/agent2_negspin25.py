from sage.all import *
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json,sympy as sp,time
P=1000000007;N=24;bb=GF(P)(3)/2;K=48

def add(a,b):return [(x+y)%P for x,y in zip(a,b)]
def smul(a,c):return [int(x*c)%P for x in a]
def mul(a,b):
 c=[0]*N
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b[:N-i]):c[i+j]=(c[i+j]+x*y)%P
 return c
def inv(a):
 c=[pow(int(a[0]),P-2,P)]
 for n in range(1,N):c.append(-sum(a[k]*c[n-k] for k in range(1,n+1))*c[0]%P)
 return c
def exp(a):
 assert not a[0]
 c=[1]
 for n in range(1,N):c.append(sum(k*a[k]*c[n-k] for k in range(1,n+1))*pow(n,P-2,P)%P)
 return c
def integ(a):return [0]+[a[n]*pow(n,P-2,P)%P for n in range(1,N)]
f0=[0]+[int((-1)**(n-1)*catalan_number(n-1))%P for n in range(1,N)]
f=[f0];den=smul(f0,2);den[0]=1;deni=inv(den)
for r in range(1,14):
 a=add(smul(f[r-1],bb-1),[n*x%P for n,x in enumerate(f[r-1])])
 for i in range(1,r):a=add(a,mul(f[i],f[r-i]))
 f.append(smul(mul(a,deni),-1))
base=exp(smul(integ(f[1]),-K));G={}
for r in range(1,13):
 G[r]=smul(integ(f[r+1]),(-1)**(r+1))
 q=sp.bernoulli(r+1,sp.Rational(-1,2))*((-1)**r)/r/(r+1)
 G[r][0]=int(q.p)*pow(int(q.q),P-2,P)%P

def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for rest in parts(n-a,a):yield (a,)+rest
@lru_cache(None)
def coeff(part):
 v=base[:];C=Counter(part)
 for i,m in C.items():
  for j in range(m):v=mul(v,G[i])
  v=smul(v,pow(int(factorial(m))%P,P-2,P))
 return v
A=list(parts(12));ix={a:i for i,a in enumerate(A)};rows=[];labels=[]
for d in range(1,13):
 pp=list(parts(d))
 for n in range(1,24):
  if n+d<=48-n:continue
  rr=[coeff(p)[n] for p in pp]
  print('degree',d,'n',n,'nonzero',sum(bool(x) for x in rr))
  for extra in parts(12-d):
   R=[0]*len(A)
   for p,x in zip(pp,rr):R[ix[tuple(sorted(p+extra))]]=x
   rows.append(R);labels.append((d,n,extra))
F=GF(P);q=json.load(open('workspace/agent3_fz25.json'))
FZ=matrix(F,[[F(QQ(x)) for x in row] for row in q['rows']]);R=matrix(F,rows)
print('NEW RELATIONS rank',R.rank(),'combinedrank',FZ.stack(R).rank(),flush=True)
json.dump({'rows':rows,'labels':labels,'monomials':A,'prime':P},open('workspace/agent2_negspin25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_negspin25.py').write_text(Path(__file__).read_text())
