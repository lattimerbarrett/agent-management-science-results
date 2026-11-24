from functools import lru_cache
from math import factorial, comb
from itertools import product
from pathlib import Path
import json
P=1000000007

def partitions(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for rest in partitions(n-a,a):yield (a,)+rest
invdf={};v=1
for d in range(24):
 if d:v=v*(2*d+1)%P
 invdf[d]=pow(v,P-2,P)
@lru_cache(None)
def poly(parts):
 if not parts:return (1,)
 first=parts[0];vals=sorted(set(parts[1:]));counts=[parts[1:].count(v) for v in vals];out=[0]*(len(parts)+1)
 for nums in product(*(range(c+1) for c in counts)):
  s=first+sum(v*n for v,n in zip(vals,nums));b=sum(nums);mult=1;rem=[]
  for v,c,n in zip(vals,counts,nums):mult=mult*comb(c,n)%P;rem +=[v]*(c-n)
  w=mult*invdf[s]%P
  if b%2:w=-w
  for k,a in enumerate(poly(tuple(rem))):out[k+1]=(out[k+1]+w*a)%P
 return tuple(out)
fact=[factorial(i)%P for i in range(80)]
scale=pow(invdf[23]*fact[48]%P,P-2,P)
@lru_cache(None)
def pairing(parts):return sum(a*fact[47+n] for n,a in enumerate(poly(parts)))%P*scale%P
A=list(partitions(12));B=list(partitions(11));M=[[pairing(tuple(sorted(a+b))) for b in B] for a in A]
assert pairing((23,))==1
for a in range(1,23):assert pairing(tuple(sorted((a,23-a))))==(fact[49]*invdf[a]*invdf[23-a]*scale-1)%P

def rank_pivots(M):
 N=[r[:] for r in M];rows=len(N);cols=len(N[0]);r=0;piv=[];labels=list(range(rows))
 for c in range(cols):
  k=next((k for k in range(r,rows) if N[k][c]),None)
  if k is None:continue
  N[k],N[r]=N[r],N[k];labels[k],labels[r]=labels[r],labels[k]
  inv=pow(N[r][c],P-2,P);N[r]=[x*inv%P for x in N[r]]
  for i in range(r+1,rows):
   m=N[i][c]
   if m:N[i]=[(x-m*y)%P for x,y in zip(N[i],N[r])]
  piv.append((labels[r],c));r+=1
 return r,piv

def det_mod(M):
 N=[x[:] for x in M];d=1
 for i in range(len(N)):
  k=next(k for k in range(i,len(N)) if N[k][i])
  if k!=i:N[k],N[i]=N[i],N[k];d=-d
  q=N[i][i];d=d*q%P;qi=pow(q,P-2,P)
  for j in range(i+1,len(N)):
   m=N[j][i]*qi%P
   for k in range(i+1,len(N)):N[j][k]=(N[j][k]-m*N[i][k])%P
 return d%P
r,piv=rank_pivots(M);rr=[x[0] for x in piv];cc=[x[1] for x in piv]
det=det_mod([[M[i][j] for j in cc] for i in rr])
print('matrix',len(A),len(B),'rank',r,'minor determinant',det)
assert r==43 and det==459309158
json.dump({'prime':P,'rows':A,'cols':B,'matrix':M,'minor_rows':rr,'minor_cols':cc,'minor_determinant':det},open('workspace/pairing25_agent2.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_pairing25.py').write_text(Path(__file__).read_text())
