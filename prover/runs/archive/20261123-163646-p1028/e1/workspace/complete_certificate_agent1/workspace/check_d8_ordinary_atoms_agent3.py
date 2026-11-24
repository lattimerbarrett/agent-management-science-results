import sys,json,time,itertools,networkx as nx
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
from sage.all import QQ,matrix,vector

def parts(n,maxp=None):
 if n==0:yield [];return
 for j in range(min(n,maxp or n),0,-1):
  for p in parts(n-j,j):yield [j]+p

def allocations(p,k):
 if not p:
  if k==0:yield []
  return
 for j in range(min(p[0],k)+1):
  for rest in allocations(p[1:],k-j):yield [j]+rest

cases=[('22',9,4,2,QQ(1)/2,QQ(1)/2,QQ(0)),('22',10,4,2,QQ(1)/2,QQ(1)/2,QQ(0)),('24',9,6,2,QQ(1)/2,QQ(1)/4,QQ(1)/8),('24',10,6,2,QQ(1)/2,QQ(1)/4,QQ(1)/8),('44',8,8,4,QQ(1)/4,QQ(1)/4,QQ(1)/4),('44',9,8,4,QQ(1)/4,QQ(1)/4,QQ(1)/4),('44',10,8,4,QQ(1)/4,QQ(1)/4,QQ(1)/4),('44',9,6,3,QQ(1)/4,QQ(1)/4,QQ(1)/4)]
out=[]
for kind,a,h,left,cl,cr,charge in cases:
 best=QQ(0);cnt=0;flows=0;t=time.time();w=None
 outside=(left*cl*cl+(h-left)*cr*cr)/2
 threshold=QQ(a)/8-outside-charge
 for part in parts(h):
  if len(part)>a:continue
  p=part+[0]*(a-len(part));ds=[a-9+x for x in p]
  if min(ds)<0 or max(ds)>=a:continue
  vecs=[]
  for ell in allocations(p,left):
   j=vector(QQ,[cl*ell[i]-cr*(p[i]-ell[i]) for i in range(a)])
   if sum(j):continue
   vecs.append((ell,j[:-1]))
  for missing in graphs_degseq(ds):
   S=set(tuple(sorted(e))for e in missing);edges=[(i,j)for i in range(a)for j in range(i+1,a)if(i,j)not in S]
   G=nx.Graph();G.add_nodes_from(range(a));G.add_edges_from(edges)
   if not nx.is_connected(G):continue
   cnt+=1;L=matrix(QQ,a-1,a-1)
   for i in range(a-1):L[i,i]=8-p[i]
   for u,v in edges:
    if u<a-1 and v<a-1:L[u,v]=L[v,u]=-1
   Q=L.inverse()
   for ell,j in vecs:
    flows+=1;E=j*Q*j
    if E>best:best=E;w=[p,missing,ell]
 r=dict(kind=kind,a=a,h=h,graphs=cnt,flows=flows,maximum=str(best),threshold=str(threshold),witness=w)
 print(r,'sec',time.time()-t,flush=True)
 out.append(r)
 json.dump(out,open('workspace/d8_ordinary_atoms_agent3.json','w'),indent=2)
 assert best<=threshold,(kind,a,h,best,threshold)
