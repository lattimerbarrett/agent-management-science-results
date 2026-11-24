import sys,time,json,networkx as nx
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import matrix,vector,QQ
out=[]
for name,ds,f in [('targetport',[4,4]+[5]*6,[-QQ(1)/2,QQ(1)/2]+[0]*6),('coincident',[5,3]+[5]*6,[-1,1]+[0]*6),('distinct',[5,4,4]+[5]*5,[-1,QQ(1)/2,QQ(1)/2]+[0]*5)]:
 best=QQ(0);cnt=0
 for e in graphs_degseq(ds):
  G=nx.Graph(e)
  if not nx.is_connected(G):continue
  cnt+=1;L=matrix(QQ,7,7)
  for i in range(1,8):L[i-1,i-1]=ds[i]
  for a,b in e:
   if a and b:L[a-1,b-1]=L[b-1,a-1]=-1
  F=vector(QQ,f[1:]);E=F*L.inverse()*F
  best=max(best,E)
 print(name,cnt,best);out.append([name,cnt,str(best)])
json.dump(out,open('workspace/d5_fulltail8_exact.json','w'))
