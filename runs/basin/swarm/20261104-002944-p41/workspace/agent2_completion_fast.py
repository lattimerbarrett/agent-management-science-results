from pathlib import Path
from itertools import combinations
from collections import deque
import random,json,time
rng=random.Random(862891)
def bits(f):
 out=[]
 while f:
  b=f&-f;out.append(b);f^=b
 return out
def tris(f):return [f^b for b in bits(f)]
def complete(facets,n,trial=0,seed=862891):
 rng=random.Random(seed)
 bs=[1<<i for i in range(n)]
 target=n*(n-1)*(n-2)*(n-3)//24
 FS={f if isinstance(f,int) else sum(1<<v for v in f) for f in facets};T={t for f in FS for t in tris(f)};E={sum(e) for f in FS for e in combinations(bits(f),2)}
 C=set();co={};Q=deque();order=[]
 for t in T:
  for b in bs:
   if not t&b:
    f=t|b;co[f]=co.get(f,0)+1
 for f,c in co.items():
  if c==2:C.add(f)
  elif c>=3 and f not in FS:Q.append(f)
 def addf(f):
  assert f not in FS
  FS.add(f);order.append(f)
  E.update(sum(e) for e in combinations(bits(f),2))
  for t in tris(f):
   if t in T:continue
   T.add(t)
   for b in bs:
    if t&b:continue
    h=t|b;co[h]=co.get(h,0)+1
    if co[h]==2:C.add(h)
    elif co[h]==3:
     C.discard(h)
     if h not in FS:Q.append(h)
 while True:
  while Q:
   f=Q.popleft()
   if f not in FS:addf(f)
  if len(FS)==target:return True,len(E),len(T),len(FS),order
  while C:
   f=rng.choice(tuple(C));C.remove(f)
   rr=[t for t in tris(f) if t in T]
   if len(rr)!=2:continue
   shared=rr[0]&rr[1];opposite=f^shared
   if opposite not in E:break
  else:
   Path(f'workspace/agent2_cover_stall{trial}.json').write_text(json.dumps({'order':order,'facets':sorted(FS)}))
   return False,len(E),len(T),len(FS),order
  addf(f)
