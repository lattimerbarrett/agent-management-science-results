import numpy as np,json,sympy as sp,time,itertools,pickle
from collections import Counter
from functools import lru_cache
from math import comb,factorial
from sage.all import GF,matrix,QQ
from pathlib import Path
P=1000003;W=27;start=time.time()
def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in parts(n-a,a):yield (a,)+t
PP=[list(parts(i)) for i in range(13)];allp=sum(PP,[]);ix={p:i for i,p in enumerate(allp)};cols=PP[12]
shifts=[]
for j in range(13):
 src=[ix[p] for p in allp if sum(p)+j<=12]
 dst=[ix[tuple(sorted(p+((j,) if j else ())))] for p in allp if sum(p)+j<=12]
 shifts.append((np.array(src,dtype=int),np.array(dst,dtype=int)))
old=json.load(open('workspace/agent3_fz25.json'));F=GF(P);FZ=matrix(F,[[F(QQ(x)) for x in row] for row in old['rows']]).echelon_form();piv=FZ.pivots();ER=[np.array([int(x) for x in r],dtype=np.int64) for r in FZ[:len(piv),:]]

def subparts(ps):
 vals=sorted(set(ps));cs=[ps.count(v) for v in vals]
 for ns in itertools.product(*(range(c+1) for c in cs)):
  aa=tuple(v for v,n in zip(vals,ns) for _ in range(n));bb=tuple(v for v,c,n in zip(vals,cs,ns) for _ in range(c-n));cf=1
  for c,n in zip(cs,ns):cf=cf*comb(c,n)%P
  yield aa,bb,cf
rows=[];labels=[]
for k in range(12,-1,-1):
 q=sp.Rational(k,48);b=(48-k)*pow(48,P-2,P)%P;total=49-k;Mom=[np.zeros(W,dtype=np.int64)];Mom[0][0]=1
 for a in range(1,total+1):
  c=Mom[-1].copy();c[1:]=(c[1:]+((b+a-1)%P)*Mom[-1][:-1])%P;Mom.append(c)
 @lru_cache(None)
 def cumul(ps):
  A=sum(ps);out=Mom[A].copy();first=ps[0]
  for aa,bb,cf in subparts(ps[1:]):
   block=tuple(sorted((first,)+aa))
   if not bb:continue
   out=(out-cf*(np.convolve(cumul(block),Mom[sum(bb)])[:W]%P))%P
  return out
 @lru_cache(None)
 def H(ps):
  out=np.zeros(len(allp),dtype=np.int64)
  if not ps:out[0]=1;return out
  first=ps[0]
  for aa,bb,cf in subparts(ps[1:]):
   block=tuple(sorted((first,)+aa));cp=cumul(block);m=len(block);old=H(bb)
   for j in range(13):
    fac=int(cp[m+j])*((-1)**(j+1))*(48 if not j else 1)*cf%P
    if not fac:continue
    src,dst=shifts[j];out[dst]=(out[dst]+fac*old[src])%P
  return out
 ac={}
 for j in range(1,13):
  z=(-1)**(j-1)*sp.bernoulli(j+1,q)/j/(j+1);ac[j]=int(z.p)*pow(int(z.q),P-2,P)%P
 eco={}
 for ps in allp:
  v=1
  for j,c in Counter(ps).items():v=v*pow(ac[j],c,P)*pow(factorial(c)%P,P-2,P)%P
  eco[ps]=v
 terms=[]
 for ps in cols:terms.append([(ix[bb],eco[aa]) for aa,bb,cf in subparts(ps)])
 patterns=[]
 for ex in parts(21-k):
  if len(ex)<=14:patterns.append(tuple(sorted((2,)*(14-len(ex))+tuple(2+x for x in ex))))
 for no,weights in enumerate(patterns):
  hv=H(weights);r=np.array([sum(int(hv[i])*cf for i,cf in tt)%P for tt in terms],dtype=np.int64)
  red=r.copy()
  for p,e in zip(piv,ER):
   if red[p]:red=(red-int(red[p])*e)%P
  if np.any(red):raise RuntimeError(('POTENTIAL NEW RELATION',k,weights,r.tolist()))
  rows.append(r.tolist());labels.append((k,weights))
  if no%100==0:print('k',k,'progress',no,'/',len(patterns),'Hstates',H.cache_info().currsize,'seconds',time.time()-start,flush=True)
 print('K COMPLETE',k,'patterns',len(patterns),'rows',len(rows),'seconds',time.time()-start,flush=True)
 json.dump({'prime':P,'rows':rows,'labels':labels},open('workspace/agent2_posspin_critical_extended.json','w'))
print('ALL',len(rows),'positivecriticalrowsIN FZ SPAN',flush=True)
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_posspin_critical_extended.py').write_text(Path(__file__).read_text())
