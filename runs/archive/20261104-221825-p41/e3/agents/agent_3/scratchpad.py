import sys,itertools,collections,time,json
sys.path.insert(0,'workspace')
from agent4_fastcert import fastcert
from agent3_check import maximal
import random
rng=random.Random(554)
for n,r in [(6,3),(7,4)]:
 fs=[sum(1<<v for v in t) for t in itertools.combinations(range(n),r)];cnt=0;start=time.time()
 for rep in range(30000):
  mask=rng.randrange(1,1<<len(fs))
  F=tuple(f for i,f in enumerate(fs) if mask>>i&1);F=tuple(sorted(F))
  if fastcert(F,1) is None:continue
  ridges=collections.Counter(f^(1<<v) for f in F for v in range(n) if f>>v&1)
  for u,v in itertools.combinations(range(n),2):
   s=(1<<u)|(1<<v);contain=[f for f in F if f&s==s]
   if not contain or len(contain)==len(F):continue
   if any(ridges[f^(1<<x)]==1 for f in contain for x in [u,v]):continue
   ds=tuple(f for f in F if f&s!=s);ls=tuple(sorted(f^s for f in contain))
   if fastcert(ds,1) is None or fastcert(ls,1) is None:continue
   contracted=maximal((f&~(1<<u))|(1<<v) if f>>u&1 else f for f in F)
   assert all(f.bit_count()==r for f in contracted)
   cnt+=1
   if fastcert(contracted,1) is None:
    print('CONTRACTION COUNTER',n,r,F,u,v,contracted,flush=True);json.dump({'facets':F,'u':u,'v':v,'contracted':contracted},open('workspace/agent3_contraction_counter.json','w'));raise SystemExit
 print('CONTRACTION PASS',n,r,cnt,'seconds',time.time()-start,flush=True)
