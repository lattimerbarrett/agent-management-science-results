from itertools import combinations
from functools import lru_cache
import time

def verts(f):
 while f:
  a=f&-f;yield a;f-=a

def connected(fs):
 V=0
 for f in fs:V|=f
 if not V:return True
 reached=V&-V
 while True:
  old=reached
  for f in fs:
   if f&reached:reached|=f
  if reached==old:return reached==V

calls=0
@lru_cache(None)
def solve(fs):
 global calls
 calls+=1
 if calls%10000==0:print('calls',calls,'facets',len(fs),flush=True)
 if len(fs)==1:return ('simplex',next(iter(fs)))
 q=next(iter(fs)).bit_count()
 if q<=2:return ('graph',tuple(fs)) if connected(fs) else None
 ridges={};stars={}
 for f in fs:
  vs=list(verts(f))
  for v in vs:
   r=f^v;ridges[r]=ridges.get(r,0)+1
   stars.setdefault(v,[]).append(f)
  for a,b in combinations(vs,2):stars.setdefault(a|b,[]).append(f)
 cand=[]
 for sig,S in stars.items():
  if not all(ridges[f^v]>=2 for f in S for v in verts(sig)):continue
  lk=frozenset(f^sig for f in S)
  if sig.bit_count()==2 and not connected(lk):continue
  cand.append((-len(S),sig,lk,frozenset(S)))
 cand.sort()
 for _,sig,lk,S in cand:
  linkcert=solve(lk)
  if linkcert is None:continue
  delcert=solve(fs-S)
  if delcert is not None:return ('shed',sig,delcert,linkcert)
 return None
