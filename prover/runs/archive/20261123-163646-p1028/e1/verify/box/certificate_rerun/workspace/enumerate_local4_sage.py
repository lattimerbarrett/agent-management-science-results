import sys,time,json,networkx as nx
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import matrix,QQ

def exact_sage(n,p):
 best=QQ(0);count=0;bc=0;witness=None
 ds=[2]*p+[4]*(n-p)
 for edges in graphs_degseq(ds):
  count+=1;G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
  if not nx.is_biconnected(G):continue
  bc+=1;L=matrix(QQ,n-1,n-1)
  for i in range(1,n):L[i-1,i-1]=ds[i]
  for a,b in edges:
   if a>0 and b>0:L[a-1,b-1]=L[b-1,a-1]=-1
  Z=L.inverse();r=max(Z.diagonal()) if p==1 else Z[0,0]
  if r>best:best=r;witness=edges
 return dict(n=n,ports=p,count=count,biconnected=bc,maximum=str(best),witness=witness)
if __name__=='__main__':
 out=[]
 for n in [13,14]:
  for p in [1,2]:
   t=time.time();r=exact_sage(n,p);out.append(r);print(r,'seconds',time.time()-t,flush=True)
   json.dump(out,open('workspace/local4_exact_13_14.json','w'),indent=2)
