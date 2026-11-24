from functools import lru_cache
from math import factorial,comb
from itertools import product
from collections import defaultdict
from pathlib import Path
import json,time
P=1000000007;h=24
invdf={};v=1
for d in range(26):
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
def pointed(parts,e,f):
 assert sum(parts)+e+f==h
 if e>f:e,f=f,e
 q=poly(parts);D=sum(parts)
 if not (e+f):
  n1=parts.count(1)
  qminus=poly(tuple(list(parts)[1:])) if n1 else ()
  result=0
  for m,a in enumerate(q):
   S=2*D+m
   t=n1*invdf[1]*qminus[m-1]%P if n1 and m>=1 and m-1<len(qminus) else 0
   result+=(a*(S*S-2*S)-3*t)*fact[2*h-3+m]
   result+=3*t*(S-3)*fact[2*h-4+m]
  return result%P*scale%P
 if e:
  return sum(a*fact[2*h-1+m] for m,a in enumerate(q))%P*invdf[e-1]%P*invdf[f-1]%P*scale%P
 if f>1:
  return sum(a*fact[2*h-2+m]*(2*D+m+2*f-1) for m,a in enumerate(q))%P*invdf[f-1]%P*scale%P
 return sum(a*(2*D+m)*(fact[2*h-2+m]+fact[2*h-3+m]) for m,a in enumerate(q))%P*scale%P

@lru_cache(None)
def onepoint(parts,e):
 assert sum(parts)+e==h-1
 q=poly(parts);D=sum(parts)
 if e:
  return sum(a*fact[2*h-2+m] for m,a in enumerate(q))%P*invdf[e-1]%P*scale%P
 return sum(a*fact[2*h-3+m]*(2*D+m) for m,a in enumerate(q))%P*scale%P

# Independent direct string recursion and inverse set partitions, for small tests.
@lru_cache(None)
def psi(exps):
 if 0 in exps:
  exps=list(exps);exps.remove(0)
  return sum(psi(tuple(sorted(exps[:i]+[x-1]+exps[i+1:]))) for i,x in enumerate(exps) if x)%P
 return fact[2*h-3+len(exps)]*scale%P*__import__('functools').reduce(lambda a,e:a*invdf[e-1]%P,exps,1)%P
for e in range(25):
 f=24-e
 if e+f:assert pointed((),e,f)==psi(tuple(sorted((e,f))))
for a in range(1,12):
 for e in range(24-a+1):
  f=24-a-e
  assert pointed((a,),e,f)==psi(tuple(sorted((a+1,e,f))))
for a in range(1,7):
 for b in range(1,7):
  for e in (0,1,2):
   f=24-a-b-e
   if f<0:continue
   direct=(psi(tuple(sorted((a+1,b+1,e,f))))-psi(tuple(sorted((a+b+1,e,f)))))%P
   assert pointed(tuple(sorted((a,b))),e,f)==direct
print('independent string and 0/1/2 kappa-factor checks passed',flush=True)

def partitions(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in partitions(n-a,a):yield (a,)+t
# On normalization of irreducible boundary, kappa(M25) pulls back to
# LOG kappa(M24,2), which is the convention used by pointed().
A=json.load(open('workspace/agent2_anomaly25.json'));V=defaultdict(int)
for parts,c in zip(A['monomials'],A['coefficients']):
 if int(c):V[(tuple(parts),0,0)]=int(c)%P
print('pullback anomaly terms',sum(bool(x) for x in V.values()),flush=True)
B=[(ks,e,f) for e in range(13) for f in range(13-e) for ks in partitions(12-e-f)]
start=time.time();L=[]
for ks,e,f in B:
 if not e+f:L.append(None);continue
 value=0
 for (vs,a,b),coef in V.items():
  if coef:value=(value+coef*pointed(tuple(sorted(ks+vs)),e+a,f+b))%P
 L.append(value)
print('evaluated',len(B),'b monomials in',time.time()-start,'sec;nonzero',sum(bool(x) for x in L),flush=True)
json.dump({'prime':P,'monomials':B,'values':L},open('workspace/agent2_boundary_functional25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_boundary_functional25.py').write_text(Path(__file__).read_text())
