import sys,json,time,networkx as nx
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import matrix,vector,QQ
cases=[('target_port',[3,4]+[5]*7,[QQ(-1)/2,QQ(1)/2]+[0]*7),('coincident',[4,3]+[5]*7,[-1,1]+[0]*7),('distinct',[4,4,4]+[5]*6,[-1,QQ(1)/2,QQ(1)/2]+[0]*6)]
out=[]
for name,ds,f in cases:
 best=QQ(0);count=0;w=None;t=time.time()
 for e in graphs_degseq(ds):
  G=nx.Graph();G.add_nodes_from(range(len(ds)));G.add_edges_from(e)
  if not nx.is_connected(G):continue
  count+=1;L=matrix(QQ,len(ds)-1,len(ds)-1)
  for i in range(1,len(ds)):L[i-1,i-1]=ds[i]
  for a,b in e:
   if a and b:L[a-1,b-1]=L[b-1,a-1]=-1
  F=vector(QQ,f[1:]);E=F*L.inverse()*F
  if E>best:best=E;w=e
 assert best<=QQ(13)/8,(name,best)
 r=dict(name=name,count=count,maximum=str(best),witness=w);out.append(r);print(r,'sec',time.time()-t,flush=True)
ds=[4]+[5]*6;best=QQ(0);w=None;count=0
for e in graphs_degseq(ds):
 G=nx.Graph();G.add_nodes_from(range(7));G.add_edges_from(e)
 if not nx.is_connected(G):continue
 count+=1;L=matrix(QQ,6,6)
 for i in range(1,7):L[i-1,i-1]=ds[i]
 for a,b in e:
  if a and b:L[a-1,b-1]=L[b-1,a-1]=-1
 E=max(L.inverse().diagonal())
 if E>best:best=E;w=e
assert best<=QQ(31)/40
r=dict(name='cap7',count=count,maximum=str(best),witness=w);out.append(r);print(r,flush=True)
json.dump(out,open('workspace/d5_tail9_cap7_exact.json','w'),indent=2)
