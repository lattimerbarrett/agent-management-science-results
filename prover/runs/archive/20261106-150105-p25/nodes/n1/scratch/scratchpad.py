import networkx as nx
from itertools import combinations
Q=nx.complete_graph(4)
F=nx.Graph(); F.add_nodes_from(range(4)); C=[list(range(4)),[],[]]
for u,v in Q.edges:
 a=('a',u,v); b=('b',u,v)
 F.add_edges_from([(u,a),(a,b),(b,v)])
 C[1].append(a);C[2].append(b)
# construct independent sets of odd-third-power within each class, color exactly
P=nx.Graph();P.add_nodes_from(F)
for u in F:
 reach={u}
 for j in range(3):reach={w for v in reach for w in F[v]}
 for v in reach:P.add_edge(u,v)
G=F.copy()
for k,cc in enumerate(C):
 # every independent set; use singleton plus all independent sets
 sets=[S for r in range(1,len(cc)+1) for S in combinations(cc,r) if all(not P.has_edge(u,v) for u,v in combinations(S,2))]
 for i,S in enumerate(sets):
  a=('A',k,i);b=('B',k)
  G.add_edge(a,b)
  G.add_edges_from((a,v) for v in S)
# detect 3 or 5
for l in [3,5]:
 found=None
 for root in G:
  def dfs(path):
   if len(path)==l:
    return path if G.has_edge(path[-1],root) else None
   for w in G[path[-1]]:
    if w not in path:
     ret=dfs(path+[w])
     if ret:return ret
  found=dfs([root])
  if found:break
 print(l,found)
print(len(G),G.number_of_edges())