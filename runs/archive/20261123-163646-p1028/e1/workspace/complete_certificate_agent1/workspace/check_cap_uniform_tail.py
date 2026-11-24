import sys,json
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import matrix,QQ,vector
out=[]
for n in range(6,11):
 best=QQ(0);w=None;cnt=0
 for edges in graphs_degseq([2]+[4]*(n-1)):
  nb=[b if a==0 else a for a,b in edges if a==0 or b==0]
  tail=[(a-1,b-1) for a,b in edges if a!=0 and b!=0]
  L=matrix(QQ,n-1,n-1)
  for a,b in tail:L[a,a]+=1;L[b,b]+=1;L[a,b]-=1;L[b,a]-=1
  try:Z=L[:-1,:-1].inverse()
  except:continue
  cnt+=1
  for v in range(1,n):
   f=vector(QQ,n-1)
   for a in nb:f[a-1]+=QQ(1)/2
   f[v-1]-=1
   energy=f[:-1]*Z*f[:-1]
   if energy>best:best=energy;w=[edges,v]
 thresh=3*QQ(n-1)/16-QQ(51)/80
 assert best<=thresh
 print(n,best,thresh,flush=True)
 out.append(dict(n=n,count=cnt,maximum=str(best),threshold=str(thresh),witness=w))
json.dump(out,open('workspace/cap_uniform_tail_exact.json','w'),indent=2)
