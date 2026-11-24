from pathlib import Path
s=Path('workspace/agent2_exact_pairing.py').read_text().split("p=json.load")[0]
exec(s)
from functools import lru_cache
from sage.all import matrix,QQ
import time,json
start=time.time()
def partitions(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in partitions(n-a,a):yield (a,)+t
@lru_cache(None)
def l1(h,ks,e):
 assert sum(ks)+e==h-1
 sc=Q(1)/(invdf[h-2]*fact[2*h-2]);den=invdf[e-1] if e else Q(1)
 return sum(a*fact[2*h-2+m] for m,a in enumerate(poly(ks)))*den*sc
@lru_cache(None)
def mons(d):return [(ks,d-sum(ks)) for k in range(d+1) for ks in partitions(k)]
res=[]
for h in range(2,25):
 for d in range((h+1)//2,min(12,h-1)+1):
  b=h-1-d
  if b<0:continue
  B=mons(b);T=mons(d-1);D=list(partitions(d))
  M=matrix(QQ,[[l1(h,tuple(sorted(ks+ls)),e+f+1) for ls,f in T] for ks,e in B])
  L=matrix(QQ,[[l1(h,tuple(sorted(ks+ls)),e) for ls in D] for ks,e in B])
  r=M.rank();s=M.augment(L).rank();assert r==s,(h,d,r,s)
  res.append((h,d,b,len(B),len(T),r));print('EXACT h,d',h,d,'rank',r,'aug',s,'sec',time.time()-start,flush=True)
print('ALL',len(res),'FRAMED NECESSARYFILTERS FAIL OVER QQ',flush=True)
json.dump(res,open('workspace/agent2_framed_filter25_exact.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_framed_filter25_exact.py').write_text(Path(__file__).read_text())
