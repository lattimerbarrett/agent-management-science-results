from fractions import Fraction as Q
from math import factorial,comb
from functools import lru_cache
import json,sys,os
N=12; g=25
@lru_cache(None)
def parts(n,lo=1):
 if n==0:return ((),)
 return tuple((i,)+p for i in range(lo,n+1) for p in parts(n-i,i))
def conv(a,b):
 c=[Q(0)]*(N+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b[:N+1-i]):c[i+j]+=x*y
 return c
A=[Q(factorial(6*n),factorial(3*n)*factorial(2*n)) for n in range(N+1)]
B=[a*Q(6*n+1,6*n-1) for n,a in enumerate(A)]
inv=[Q(1)]+[Q(0)]*N
for n in range(1,N+1):inv[n]=-sum(A[i]*inv[n-i] for i in range(1,n+1))
D=conv(B,inv)
logA=[Q(0)]*(N+1)
for n in range(1,N+1):logA[n]=sum(i*A[i]*inv[n-i] for i in range(1,n+1))/n
Dpow=[[Q(1)]+[Q(0)]*N]
for k in range(1,11):Dpow.append(conv(Dpow[-1],D))
def mul(a,b):
 c={}
 for p,x in a.items():
  for q,y in b.items():
   if sum(p)+sum(q)<=N:
    r=tuple(sorted(p+q));c[r]=c.get(r,0)+x*y
 return {p:x for p,x in c.items() if x}
P={():Q(1)}
for n in range(1,N+1):
 factor={tuple([n]*k):(-logA[n])**k/factorial(k) for k in range(N//n+1)}
 P=mul(P,factor)
@lru_cache(None)
def H(sig):
 if not sig:return P
 # Group blocks containing first occurrence: choose subset of remaining multiset.
 from collections import Counter
 first=sig[0];counts=list(Counter(sig[1:]).items());out={}
 def visit(i,block,rest,mult):
  if i<len(counts):
   v,c=counts[i]
   for k in range(c+1):visit(i+1,block+(v,)*k,rest+(v,)*(c-k),mult*comb(c,k))
   return
  block=(first,)+block;shift=sum(x//3 for x in block);b=sum(x%3==1 for x in block)
  l={(() if n==0 else (n,)):Dpow[b][n-shift]*(2*g-2 if n==0 else 1)*factorial(len(block)-1)*mult for n in range(shift,N+1) if Dpow[b][n-shift]}
  product=mul(l,H(tuple(sorted(rest))))
  for p,x in product.items():out[p]=out.get(p,0)+x
 visit(0,(),(),1)
 return {p:x for p,x in out.items() if x}
cols=parts(N); rows=[]; labels=[]
for r in range(1,N+1):
 for weight in range(3*r-g):
  if (r+weight)%2:continue
  for sig in parts(weight):
   if any(x%3==2 for x in sig):continue
   rel={p:x for p,x in H(sig).items() if sum(p)==r}
   for extra in parts(N-r):
    row={tuple(sorted(p+extra)):x for p,x in rel.items()}
    if row:
     rows.append([row.get(p,Q(0)) for p in cols]);labels.append((r,sig,extra))
print('matrix',len(rows),len(cols),flush=True)
# modular rank with denominators inverted: rigorous lower bound rank
prime=1000000007
mat=[[int(v.numerator%prime)*pow(int(v.denominator%prime),-1,prime)%prime for v in row] for row in rows]
pivs=[]; pivot_rows=[]
for ri,row in enumerate(mat):
 for c,p in pivs:
  if row[c]:
   z=row[c];row[:]=[(x-z*y)%prime for x,y in zip(row,p)]
 if any(row):
  c=next(i for i,x in enumerate(row) if x);z=pow(row[c],-1,prime);row[:]=[x*z%prime for x in row];pivs.append((c,row[:]));pivot_rows.append(ri)
print('modular rank',len(pivs),'upperdim',len(cols)-len(pivs),flush=True)
pivot_cols=[c for c,row in pivs]
minor=[[int(rows[i][j].numerator%prime)*pow(int(rows[i][j].denominator%prime),-1,prime)%prime for j in pivot_cols] for i in pivot_rows]
det=1
for c in range(len(minor)):
 ri=next(i for i in range(c,len(minor)) if minor[i][c])
 if ri!=c:minor[c],minor[ri]=minor[ri],minor[c];det=-det
 v=minor[c][c];det=det*v%prime;iv=pow(v,-1,prime)
 for i in range(c+1,len(minor)):
  a=minor[i][c]*iv%prime
  for j in range(c,len(minor)):minor[i][j]=(minor[i][j]-a*minor[c][j])%prime
print('minor determinant',det%prime,flush=True)
# Rational exact rank
import sympy as sp
M=sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).convert_to(sp.QQ)
print('rational rank',M.rank(),flush=True)
os.makedirs('workspace',exist_ok=True)
# Export this self-contained computation for independent reruns.
from pathlib import Path
if Path(__file__).name == 'scratchpad.py':
 Path('workspace/agent3_fz25.py').write_text(Path(__file__).read_text())
with open('workspace/agent3_fz25.json','w') as f:json.dump({'genus':g,'degree':N,'columns':cols,'labels':labels,'rows':[[str(v) for v in row] for row in rows],'rank_mod_prime':len(pivs),'prime':prime},f)
