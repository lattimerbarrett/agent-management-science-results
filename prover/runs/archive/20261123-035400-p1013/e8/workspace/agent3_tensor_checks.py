import itertools as it,networkx as nx,json,time

def tensor(r,m):
 vv=list(it.product(range(r),repeat=m));G=nx.Graph();G.add_nodes_from(vv)
 G.add_edges_from((u,v) for i,u in enumerate(vv) for v in vv[i+1:] if all(a!=b for a,b in zip(u,v)))
 return G

def colorings(G,r):
 V=list(G);V.sort(key=lambda u:-G.degree(u));col={};out=[]
 def rec():
  if len(col)==len(V):out.append(dict(col));return
  u=max((v for v in V if v not in col),key=lambda v:(len({col[w] for w in G[v] if w in col}),G.degree(v)))
  forbidden={col[w] for w in G[u] if w in col}
  for c in range(r):
   if c not in forbidden:col[u]=c;rec();del col[u]
 rec();return out
res=[]
for r,m in [(3,2),(3,3),(4,2)]:
 G=tensor(r,m);start=time.time();C=colorings(G,r)
 projections=[{v:perm[v[j]] for v in G} for j in range(m) for perm in it.permutations(range(r))]
 assert len(C)==len(projections)
 assert all(c in projections for c in C)
 d={'r':r,'m':m,'vertices':len(G),'edges':G.number_of_edges(),'all_colorings':len(C),'coordinate_colorings':len(projections),'seconds':time.time()-start}
 print(d,flush=True);res.append(d)
with open('workspace/agent3_tensor_checks.json','w') as f:json.dump(res,f)
