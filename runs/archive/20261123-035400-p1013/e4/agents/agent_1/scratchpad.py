import networkx as nx,random,itertools,json
random.seed(71)
n=9
colors=list(itertools.product((0,1),repeat=n-1))
colors=[(0,)+c for c in colors]
found=[]
for it in range(20000):
 # Vertex8 is critical; the remaining graph is bipartite with 4+4 parts.
 edges=[(u,v) for u in range(4) for v in range(4,8) if random.random()<.65]
 edges += [(u,8) for u in range(8) if random.random()<.7]
 # Early twomatching and onepartmatching tests.
 twomatch=False;onematch=False;p3min=n
 for bits in colors:
  deg=[0]*n;ed=[0,0];es=[]
  for u,v in edges:
   if bits[u]==bits[v]:
    deg[u]+=1;deg[v]+=1;ed[bits[u]]+=1;es.append((u,v))
  md=max(deg)
  if md<=1:
   twomatch=True
   if min(ed)==0:onematch=True;break
  if min(ed)==0 and md<=2:
   J=nx.Graph();J.add_edges_from(es)
   cc=list(nx.connected_components(J))
   if all(len(C)<=3 and J.subgraph(C).number_of_edges()<3 for C in cc):p3min=min(p3min,sum(len(C)==3 for C in cc))
 if twomatch and not onematch and 2<=p3min<n:
  H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(edges)
  code=nx.to_graph6_bytes(H,header=False).decode().strip()
  print(it,p3min,code,edges,flush=True)
  found.append({'g6':code,'edges':edges,'p3min':p3min})
  if len(found)==5:break
print('iterations',it+1,'found',len(found))
open('workspace/agent1_nine_vertex_candidates.json','w').write(json.dumps(found))
