import sys,itertools,json
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import QQ,matrix,vector
results=[]
for a in [7,8,9]:
 best=QQ(0);cnt=0;valid=0
 for partition in [[4],[3,1],[2,2],[2,1,1],[1,1,1,1]]:
  p=partition+[0]*(a-len(partition))
  ds=[a-7+k for k in p]
  for missing in graphs_degseq(ds):
   S=set(tuple(sorted(e)) for e in missing)
   edges=[(i,j) for i in range(a) for j in range(i+1,a) if (i,j) not in S]
   L=matrix(QQ,a,a)
   for i,j in edges:L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
   try:Q=L[:-1,:-1].inverse()
   except:continue
   cnt+=1
   for t in range(a):
    good=True
    for mask in range(1,1<<a):
     if mask>>t&1:continue
     U={v for v in range(a) if mask>>v&1}
     ell=sum(p[v] for v in U)
     if not ell:continue
     c=sum((i in U)!=(j in U) for i,j in edges)
     if c<ell+2:good=False;break
    if not good:continue
    valid+=1
    j=vector(QQ,[QQ(k)/4-int(i==t) for i,k in enumerate(p)])
    en=j[:-1]*Q*j[:-1]
    if en>best:best=en;w=[partition,missing,t]
 thresh=QQ(a)/6-QQ(1)/3-QQ(139)/270
 assert best<=thresh
 print(a,cnt,valid,best,thresh,flush=True)
 results.append(dict(a=a,graphs=cnt,valid_targets=valid,max_energy=str(best),threshold=str(thresh),witness=w))
json.dump(results,open('workspace/d6_tail4_energy_agent4.json','w'),indent=2)
