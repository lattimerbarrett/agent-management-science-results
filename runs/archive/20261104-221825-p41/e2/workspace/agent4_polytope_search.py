import numpy as np,itertools,time,json
from scipy.spatial import ConvexHull
rng=np.random.default_rng(1245)
def subs(s):
 t=s
 while t:
  yield t;t=(t-1)&s
 yield 0
for n in [9,10,12]:
 allf=[sum(1<<v for v in c) for c in itertools.combinations(range(n),4)]
 bits={f:[1<<v for v in range(n) if f>>v&1] for f in allf}
 best=99999;t=time.time()
 for trial in range(1000):
  pts=rng.normal(size=(n,4));pts/=np.linalg.norm(pts,axis=1)[:,None]
  hull=ConvexHull(pts);fs={sum(1<<int(v) for v in s) for s in hull.simplices}
  faces={s for f in fs for s in subs(f)}
  apps=[f for f in allf if f not in fs and sum(v for v in bits[f] if f^v in faces) not in faces]
  if len(apps)<best:
   best=len(apps);print('best',n,trial,best,'facets',len(fs),flush=True)
   json.dump({'n':n,'pts':pts.tolist(),'facets':sorted(fs),'appendable':apps},open('workspace/agent4_polytope_best_%d.json'%n,'w'))
  todo=set(allf)-fs
  order=[]
  while todo:
   apps=[f for f in todo if sum(v for v in bits[f] if f^v in faces) not in faces]
   if not apps:
    print('OBSTRUCTION',n,sorted(fs),order,flush=True);json.dump({'n':n,'pts':pts.tolist(),'sphere_facets':sorted(fs),'addition_order':order},open('workspace/agent4_polytope_obstruction.json','w'));raise SystemExit
   f=apps[int(rng.integers(len(apps)))];order.append(f);todo.remove(f);faces.update(subs(f))
 print('done',n,best,time.time()-t,flush=True)
