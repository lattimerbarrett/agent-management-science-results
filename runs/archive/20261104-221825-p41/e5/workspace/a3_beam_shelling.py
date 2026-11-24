import itertools,random,time,json
from pathlib import Path
n=12
facets=[sum(1<<i for i in c) for c in itertools.combinations(range(n),4)];N=len(facets);ALL=(1<<N)-1
ridge_neigh=[];bad=[]
for j,f in enumerate(facets):
 vv=[i for i in range(n) if f>>i&1];rr=[f^(1<<i) for i in vv]
 ridge_neigh.append([sum(1<<k for k,g in enumerate(facets) if k!=j and g&r==r) for r in rr])
 bb=[]
 for pat in range(16):
  covered=[r for l,r in enumerate(rr) if pat>>l&1]
  bb.append(sum(1<<k for k,g in enumerate(facets) if k!=j and not any((f&g)&r==(f&g) for r in covered)))
 bad.append(bb)
def legal(s):
 out=[]
 for j in range(N):
  if s>>j&1:continue
  pat=sum(1<<l for l,nn in enumerate(ridge_neigh[j]) if s&nn)
  if pat and not s&bad[j][pat]:out.append(j)
 return out
rng=random.Random(313);beam={1};start=time.time();W=100
for depth in range(1,N):
 candidates=set()
 for s in beam:
  for j in legal(s):candidates.add(s|(1<<j))
 scored=[]
 for s in candidates:
  ll=legal(s)
  if not ll and s!=ALL:
   fs=[f for j,f in enumerate(facets) if s>>j&1];json.dump({'n':n,'facets':fs},open('workspace/a3_beam_stuck.json','w'));print('FOUND',depth+1,fs,flush=True);raise SystemExit
  scored.append((len(ll),rng.random(),s))
 scored.sort();beam={s for _,_,s in scored[:W]}
 if depth%10==0:print(depth+1,len(candidates),'minlegal',scored[0][0],'time',round(time.time()-start,1),flush=True)
print('COMPLETE no stuck candidate',time.time()-start)
Path('workspace/a3_beam_shelling.py').write_text(Path(__file__).read_text())
