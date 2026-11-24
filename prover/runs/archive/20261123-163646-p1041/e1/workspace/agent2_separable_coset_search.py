import numpy as np,itertools,time,json
from pathlib import Path
n=np.array([49,7,7,1],dtype=np.int64)
profiles=np.array([p for p in itertools.product(*[range(x+1) for x in n]) if sum(p)%2==0],dtype=np.int64)
H=np.array([[((i&1)*(j&1))^(((i>>1)&1)*((j>>1)&1)) for j in range(4)] for i in range(4)],dtype=np.int64)
print('profiles',len(profiles));hits={};t=time.time()
for k in range(0,len(profiles),100):
 R=profiles[k:k+100];S=(n-R)@H+R@(1-H);W=(S@n)[:,None]+(profiles@(64-2*S).T).T
 for target in [194,198,202,206]:
  if target in hits:continue
  z=np.argwhere(W==target)
  if len(z):i,j=z[0];hits[target]={'rowcounts':R[i].tolist(),'colcounts':profiles[j].tolist()};print('HIT',target,hits[target],flush=True)
print('DONE',hits,time.time()-t)
json.dump(hits,open('workspace/agent2_separable_coset_hits.json','w'))
Path('workspace/agent2_separable_coset_search.py').write_text(Path('scratchpad.py').read_text())
