from pathlib import Path
from itertools import combinations
from collections import deque
import random,json,time
rng=random.Random(862891)
raw=json.loads(Path('workspace/agent2_cover36.json').read_text());n=36
base={sum(1<<v for v in f) for f in raw}
bs=[1<<i for i in range(n)]
def bits(f):return [x for x in bs if x&f]
def tris(f):return [f^b for b in bits(f)]
def attempt(trial):
 FS=set(base);T={t for f in FS for t in tris(f)};E={sum(e) for f in FS for e in combinations(bits(f),2)}
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
  if len(FS)==58905:return True,len(E),len(T),len(FS),order
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
if __name__=='__main__':
 Path('workspace/agent2_cover_completion.py').write_text(Path(__file__).read_text())
 start=time.time()
 for trial in range(30):
  good,e,t,f,order=attempt(trial)
  print('trial',trial,'complete',good,'E,T,F',e,t,f,'added',len(order),'time',time.time()-start,flush=True)
  if trial==0:
   Path('workspace/agent2_cover_completion_order.json').write_text(json.dumps(order))
   # Independent direct pure-ridge attachment check, not incremental counters.
   fs=set(base);tt={t for f in fs for t in tris(f)};ee={sum(e) for f in fs for e in combinations(bits(f),2)}
   for h in order:
    assert h not in fs
    face_tris=[t for t in tris(h) if t in tt]
    covered={sum(e) for t in face_tris for e in combinations(bits(t),2)}
    assert all(sum(e) not in ee or sum(e) in covered for e in combinations(bits(h),2))
    assert set().union(*(set(bits(t)) for t in face_tris))==set(bits(h))
    fs.add(h);tt.update(tris(h));ee.update(sum(e) for e in combinations(bits(h),2))
   assert fs=={sum(f) for f in combinations(bs,4)}
   print('INDEPENDENTLY VERIFIED all58743facet attachments andexactfinalfacetset',flush=True)
  if not good:break
