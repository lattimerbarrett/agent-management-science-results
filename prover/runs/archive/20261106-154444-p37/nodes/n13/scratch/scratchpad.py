import itertools,time,pickle,os
import numpy as np,networkx as nx,z3

def critical_graph(m,n):
 verts=list(range(n));edges=list(itertools.combinations(verts,2))
 cp=[]
 for a in range(1,m):
  for i in range(3):
   p=tuple(a if j==i else 0 for j in range(3));q=tuple(a-1 if j==i else m-1 for j in range(3))
   for e in edges:
    for v in e:cp.append((p,v,q,e))
 for v in verts:
  for e in edges:
   if v not in e:cp.append(((0,)*3,v,(m-1,)*3,e))
 N=len(cp)
 adj=np.zeros((N,N),dtype=bool)
 for i,(p,v,q,e) in enumerate(cp):
  for j,(p2,v2,q2,e2) in enumerate(cp):
   if v in e2 and all(a<=b for a,b in zip(p,q2)):adj[i,j]=True
 assert not adj.diagonal().any()
 G=nx.from_numpy_array(adj,create_using=nx.DiGraph)
 return cp,adj,G

def solve(m,n,t,seconds=20):
 cp,adj,G=critical_graph(m,n);N=len(cp)
 s=z3.Solver();s.set(timeout=int(seconds*1000));C=[z3.Int('c'+str(i)) for i in range(N)]
 for c in C:s.add(c>=0,c<t)
 for i,j in zip(*np.where(np.triu(adj&adj.T,1))):s.add(C[int(i)]!=C[int(j)])
 # An explicit three-clique of P critical pairs, at a fixed incidence.
 for i in range(3):s.add(C[i*n*(n-1)]==i)
 start=time.time();rounds=0;clauses=0
 while time.time()-start<seconds:
  s.set(timeout=max(1,int((seconds-time.time()+start)*1000)))
  res=s.check()
  if res!=z3.sat:return str(res),N,rounds,clauses,time.time()-start
  model=s.model();colors=[model.eval(c).as_long() for c in C];added=0
  for c in range(t):
   H=G.subgraph([i for i,v in enumerate(colors) if v==c]).copy()
   while True:
    try:cyc=nx.find_cycle(H)
    except nx.NetworkXNoCycle:break
    vs=list(dict.fromkeys(a for a,b in cyc));s.add(z3.Or([C[v]!=c for v in vs]));added+=1
    H.remove_nodes_from(vs)
  if not added:return 'sat',N,rounds,clauses,time.time()-start
  clauses+=added;rounds+=1
 return 'unknown',N,rounds,clauses,time.time()-start
results=[]
for n in [3,4,5,6]:
 for m in [2,3,4,6]:
  for t in [4,5,6]:
   out=solve(m,n,t,15)
   print('m,n,t',m,n,t,out,flush=True);results.append((m,n,t,out))
   if out[0]=='sat':break
pickle.dump(results,open('grid_product_results.pkl','wb'))
