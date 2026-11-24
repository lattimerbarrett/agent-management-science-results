from itertools import combinations
from pathlib import Path
import numpy as np, random, time

def search(n,q,trials=100,seed=1):
 rng=random.Random(seed)
 masks=np.array([sum(1<<i for i in c) for c in combinations(range(n),q)],dtype=np.int64)
 N=len(masks)
 dif=masks[None,:]&~masks[:,None]
 extra=np.where((dif!=0)&((dif&(dif-1))==0),dif,0)
 best=1e9
 def step(active,bad,S,u):
  na=active|extra[:,u]
  nb=bad+((masks[u]&na)==0)
  changed=np.flatnonzero(na!=active)
  if len(changed): nb[changed]=np.sum((masks[S][None,:]&na[changed,None])==0,axis=1)+((masks[u]&na[changed])==0)
  return na,nb
 t=time.time()
 for tr in range(trials):
  active=np.zeros(N,dtype=np.int64);bad=np.zeros(N,dtype=np.int64);S=[];present=np.zeros(N,dtype=bool)
  order=[]
  while len(S)<N:
   avail=np.flatnonzero((bad==0)&~present)
   if not len(avail):
    print('COUNTEREXAMPLE',n,q,tr,len(S),[int(masks[u]) for u in S],flush=True)
    Path(f'workspace/agent2_candidate_{n}_{q}.txt').write_text(str([int(masks[u]) for u in S]))
    return S
   if tr%3==0 and len(S)>0:
    opts=list(avail);rng.shuffle(opts);opts=opts[:min(12,len(opts))]
    scores=[]
    for u in opts:
     na,nb=step(active,bad,S,u)
     scores.append((int(np.sum((nb==0)&~present))-int(nb[u]==0),rng.random(),u,na,nb))
    _,_,u,active,bad=min(scores,key=lambda z:z[:2])
   else:
    u=int(rng.choice(avail))
    active,bad=step(active,bad,S,u)
   present[u]=True;S.append(u)
  if tr%100==0:print('progress',n,q,tr,'seconds',round(time.time()-t,1),flush=True)
 print('No stuck prefix',n,q,trials,'trials',round(time.time()-t,1),'seconds',flush=True)
 return None

if __name__=='__main__':
 for n,q in [(12,3),(13,3),(12,4),(12,5)]:search(n,q,1000)
 Path('workspace/agent2_linear_quotient_search.py').write_text(Path(__file__).read_text())
