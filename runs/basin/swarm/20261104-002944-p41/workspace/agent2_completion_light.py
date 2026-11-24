from itertools import combinations
from collections import deque
import random

def bits(f):
 out=[]
 while f:
  b=f&-f;out.append(b);f^=b
 return out

def tris(f):return [f^b for b in bits(f)]

def complete_light(facets,n,seed=862891):
 """Search shelling-extendable attachments until triangle-full or stalled.
 Returns(success,E,T,meaningful_added_facets). If success, append all other
 facets arbitrarily: they now have full boundaries. If stall, also fill all
 full-boundary facets; no further shelling-compatible addition exists.
 Input vertices must be exactly range(n); facets may be bitmasks or lists.
 """
 rng=random.Random(seed);bs=[1<<i for i in range(n)]
 base={f if isinstance(f,int) else sum(1<<v for v in f) for f in facets}
 assert all(f.bit_count()==4 for f in base)
 assert set().union(*(set(bits(f)) for f in base))==set(bs)
 T={t for f in base for t in tris(f)}
 E={sum(e) for f in base for e in combinations(bits(f),2)}
 C=[];co={};Q=deque();order=[];target=n*(n-1)*(n-2)//6
 for t in T:
  for b in bs:
   if not t&b:
    f=t|b;co[f]=co.get(f,0)+1
 for f,c in co.items():
  if c==2:C.append(f)
  elif c==3:Q.append(f)
 def addf(f):
  order.append(f)
  E.update(sum(e) for e in combinations(bits(f),2))
  for t in tris(f):
   if t in T:continue
   T.add(t)
   for b in bs:
    if t&b:continue
    h=t|b;co[h]=co.get(h,0)+1
    if co[h]==2:C.append(h)
    elif co[h]==3:
     if h!=f:Q.append(h)
 while True:
  while Q:
   f=Q.popleft()
   if co[f]==3:addf(f)
   if len(T)==target:return True,E,T,order
  while C:
   i=rng.randrange(len(C));f=C[i];C[i]=C[-1];C.pop()
   if co[f]!=2:continue
   rr=[t for t in tris(f) if t in T]
   opposite=f^(rr[0]&rr[1])
   if opposite not in E:break
  else:return len(T)==target,E,T,order
  addf(f)
  if len(T)==target:return True,E,T,order
