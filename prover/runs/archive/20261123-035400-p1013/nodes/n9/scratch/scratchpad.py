import numpy as np,random
random.seed(44)
for q,i in [(4,4),(5,5),(6,6),(7,7)]:
 n=1+q+i;masks=np.arange(1<<(n-1),dtype=np.uint32)
 colors=np.array([((masks>>v)&1).astype(np.int8) for v in range(n)])
 count=0
 for rep in range(3000):
  edges=[(0,1),(0,2)]+[(0,v) for v in range(q+1,n) if random.random()<.6]+[(u,v) for u in range(1,q+1) for v in range(q+1,n) if random.random()<.35]
  adj=[[] for _ in range(n)]
  for u,v in edges:adj[u].append(v);adj[v].append(u)
  valid=np.ones(len(masks),dtype=bool)
  ca=np.zeros(len(masks),dtype=np.int16);cb=ca.copy()
  for u in range(n):
   d=np.zeros(len(masks),dtype=np.int8)
   for v in adj[u]:d+=colors[u]==colors[v]
   valid&=d<=1
  if not valid.any():continue
  for u,v in edges:
   ca+=(colors[u]==1)&(colors[v]==1);cb+=(colors[u]==0)&(colors[v]==0)
  ps=set(zip(ca[valid].tolist(),cb[valid].tolist()));ps|={(b,a) for a,b in ps}
  ts=[b for a,b in ps if a==0]
  if not ts:continue
  t=min(ts)
  if t<=1:continue
  count+=1
  if t>=4 and rep<100:
   print('large t',t,'patterns',ps,flush=True)
  allowed=[(a,b) for a in range(t) for b in range(t) if not any(a>=p and b>=q0 for p,q0 in ps)]
  me=max(a+b for a,b in allowed);w=lambda a,b:3.3*max(a,b)+min(a,b)
  mw=max(w(a,b) for a,b in allowed);be=max(w(a,b) for a,b in allowed if a+b==me)
  if be<mw-1e-8:
   print('FOUND',n,'edges',edges,'patterns',ps,'allowed',allowed,flush=True);raise SystemExit
 print('done',n,'qualified',count,flush=True)
print('none')