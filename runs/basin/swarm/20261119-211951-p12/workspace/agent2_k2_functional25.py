from functools import lru_cache
from math import factorial,comb
from itertools import product
from pathlib import Path
import json,time
P=1000000007;h=23
invdf={};v=1
for d in range(27):
 if d:v=v*(2*d+1)%P
 invdf[d]=pow(v,P-2,P)
fact=[factorial(i)%P for i in range(90)]
scale=pow(invdf[h-2]*fact[2*h-2]%P,P-2,P)
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
@lru_cache(None)
def pointed4(parts,es):
 assert sum(parts)+sum(es)==h+2
 assert es.count(0)<=1
 q=poly(parts);D=sum(parts);denom=1
 for e in es:
  if e:denom=denom*invdf[e-1]%P
 if all(es):return sum(a*fact[2*h+1+m] for m,a in enumerate(q))%P*denom%P*scale%P
 k=es.count(1);L=sum(e>=2 for e in es)
 SS=sum(2*e-1 for e in es if e>=2)
 total=0
 for m,a in enumerate(q):
  falling=1;F=0
  for j in range(k+1):
   if j:falling*=k-j+1
   F+=falling*fact[2*h-3+m+L+k-j]
  total+=a*(2*D+m+SS)*F
 return total%P*denom%P*scale%P
@lru_cache(None)
def psi(exps):
 if 0 in exps:
  exps=list(exps);exps.remove(0)
  return sum(psi(tuple(sorted(exps[:i]+[x-1]+exps[i+1:]))) for i,x in enumerate(exps) if x)%P
 val=fact[2*h-3+len(exps)]*scale%P
 for e in exps:val=val*invdf[e-1]%P
 return val
# Check against independent direct string recursion with0,1,2 kappa factors.
for a in range(0,11):
 for b in range(0,11):
  es=(1,1,1,h-1-a-b)
  if es[-1]<0:continue
  ks=tuple(x for x in sorted((a,b)) if x)
  expected=psi(tuple(sorted(es+tuple(x+1 for x in ks))))
  if len(ks)==2:expected-=psi(tuple(sorted(es+(sum(ks)+1,))))
  assert pointed4(ks,es)==expected%P
for es in [(0,1,1,23),(0,1,2,22),(0,2,2,21),(1,1,1,22)]:assert pointed4((),es)==psi(tuple(sorted(es)))
print('n4 direct string0/1/2 kappa checks passed',flush=True)
def partitions(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for rest in partitions(n-a,a):yield (a,)+rest
A=json.load(open('workspace/agent2_anomaly25.json'));V=[(tuple(ks),int(c)%P) for ks,c in zip(A['monomials'],A['coefficients']) if int(c)]
B=[]
for total in range(11):
 for ks in partitions(10-total):
  for a in range(total+1):
   for b in range(total-a+1):
    for c in range(total-a-b+1):B.append((ks,(a,b,c,total-a-b-c)))
start=time.time();L=[]
for ks,es in B:
 exp=tuple(es[i]+(i<3) for i in range(4))
 L.append(sum(c*pointed4(tuple(sorted(ks+vs)),exp) for vs,c in V)%P)
print('n4 functional',len(B),'rows in',time.time()-start,'seconds nonzero',sum(bool(v) for v in L),flush=True)
json.dump({'prime':P,'monomials':B,'values':L},open('workspace/agent2_k2_functional25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_k2_functional25.py').write_text(Path(__file__).read_text())
