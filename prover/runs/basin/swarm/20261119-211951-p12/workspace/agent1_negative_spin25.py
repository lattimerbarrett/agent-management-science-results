from fractions import Fraction as Q
from math import factorial
from functools import lru_cache
import sympy as sp,json
from pathlib import Path
p=1000000007;NN=23;D=12;M=NN+D;q=-pow(2,-1,p)%p

def conv(a,b):
 out=[0]*(M+1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b[:M+1-i]):
    if y:out[i+j]=(out[i+j]+x*y)%p
 return out
Gs=[[1]+[0]*M]
for n in range(1,NN+1):
 c=(n-q)%p
 Gs.append(conv(Gs[-1],[pow(c,j,p) for j in range(M+1)]))
H=[[v*pow(factorial(n),-1,p)%p for v in row] for n,row in enumerate(Gs)]
Ls=[[0]*(M+1)]
for n in range(1,NN+1):
 row=H[n][:]
 for k in range(1,n):
  v=conv(Ls[k],H[n-k]);a=k*pow(n,-1,p)%p
  row=[(x-a*y)%p for x,y in zip(row,v)]
 Ls.append(row)
 assert all(v==0 for v in row[:n-1]),(n,row[:n])
print('diagonal connected series computed',flush=True)
# a[k][m] coefficient of kappa_m in log generating S
A=[[0]*(D+1) for k in range(NN+1)]
for k in range(1,NN+1):
 for m in range(D+1):
  A[k][m]=Ls[k][m+k]*((-1)**(k-1))%p
 A[k][0]=A[k][0]*48%p
S=[{():1}]
for n in range(1,NN+1):
 row={}
 for k in range(1,n+1):
  for part,v in S[n-k].items():
   weight=sum(part)
   for m in range(D-weight+1):
    coeff=A[k][m]*k%p
    if coeff:
     key=tuple(sorted(part+((m,) if m else ())))
     row[key]=(row.get(key,0)+v*coeff)%p
 inv=pow(n,-1,p);S.append({k:v*inv%p for k,v in row.items() if v})
 print('S',n,len(S[-1]),flush=True)
C={():1}
for m in range(1,D+1):
 b=Q(sp.bernoulli(m+1,sp.Rational(-1,2)))
 coeff=(-1)**m*b/Q(m*(m+1));c=coeff.numerator%p*pow(coeff.denominator,-1,p)%p
 out={}
 for part,v in C.items():
  for k in range((D-sum(part))//m+1):
   key=tuple(sorted(part+(m,)*k));out[key]=(out.get(key,0)+v*pow(c,k,p)*pow(factorial(k),-1,p))%p
 C=out
@lru_cache(None)
def parts(n,lo=1):
 if not n:return ((),)
 return tuple((i,)+x for i in range(lo,n+1) for x in parts(n-i,i))
cols=parts(D);ix={c:i for i,c in enumerate(cols)}
base=json.load(open('workspace/agent3_fz25.json'));pivs={}
def add(row):
 row=row[:]
 for c,v in sorted(pivs.items()):
  if row[c]:
   a=row[c];row=[(x-a*y)%p for x,y in zip(row,v)]
 if any(row):
  c=next(i for i,x in enumerate(row) if x);a=pow(row[c],-1,p);pivs[c]=[x*a%p for x in row];return True
 return False
for row in base['rows']:
 add([Q(x).numerator%p*pow(Q(x).denominator,-1,p)%p for x in row])
print('initialrank',len(pivs),flush=True)
rows=[]
for n in range(19,NN+1):
 row=[0]*len(cols)
 for a,v in C.items():
  for b,w in S[n].items():
   if sum(a)+sum(b)==D:
    key=tuple(sorted(a+b));row[ix[key]]=(row[ix[key]]+v*w*factorial(n))%p
 rows.append(row)
 print('negative-spin n',n,'row_nonzero',sum(bool(x) for x in row),'NEW?',add(row),'rank',len(pivs),flush=True)
if Path(__file__).name=='scratchpad.py':Path('workspace/agent1_negative_spin25.py').write_text(Path(__file__).read_text())
json.dump({'prime':p,'columns':cols,'rows':rows,'rank':len(pivs)},open('workspace/agent1_negative_spin25.json','w'))
