import numpy as np,itertools,json
T=list(itertools.combinations(range(6),3));E=list(itertools.combinations(range(6),2));N=1<<20
te=[sum(1<<j for j,e in enumerate(E) if set(e)<=set(t)) for t in T]
eu=np.zeros(N,dtype=np.uint16)
for j in range(20):eu[1<<j:1<<(j+1)]=eu[:1<<j]|te[j]
inds=np.arange(N,dtype=np.uint32)
results=[]
for k,path in [(0,'workspace/agent2_dim2_n6_VD.npz'),(1,'workspace/agent2_dim2_n6.npz')]:
 kd=np.load(path)['kd'];count=0
 for j in range(20):
  good=kd & ((inds&(1<<j))==0) & ((eu&te[j])==te[j])
  selected=inds[good]
  assert np.all(kd[selected|(1<<j)])
  count+=len(selected)
 results.append({'n':6,'d':2,'k':k,'checked_fullboundary_additions':count})
print(results)
json.dump(results,open('workspace/agent2_fullboundary_checks.json','w'))
