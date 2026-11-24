import networkx as nx
from itertools import combinations
# Attempted finite extension: record neighbor colors and distance-two colors.
# The covered vertices are colored by a sampled neighbor.
for n in [7,9,11,13,15]:
 G=nx.cycle_graph(n)
 found=False
 for t in [1,2,3]:
  for S in combinations(G,t):
   covered={v for v in G if any(G.has_edge(v,s) for s in S)}
   color={v:next(i for i,s in enumerate(S) if G.has_edge(v,s)) for v in covered}
   if any(not any(w in covered for w in G[v]) for v in G if v not in covered):continue
   A={v:frozenset(color[w] for w in G[v] if w in covered) for v in G}
   B={v:frozenset(color[z] for w in G[v] for z in G[w] if z in covered) for v in G}
   labels={v:(color.get(v,-1),A[v],B[v]) for v in G}
   H=nx.Graph();H.add_nodes_from(labels.values())
   H.add_edges_from((labels[u],labels[v]) for u,v in G.edges)
   bad_loop=nx.number_of_selfloops(H)>0
   triangles=sum(nx.triangles(H).values())//3
   if bad_loop or triangles:
    print('failed extension',dict(n=n,S=S,uncovered=set(G)-covered,loops=bad_loop,triangles=triangles))
    found=True;break
  if found:break
 if not found:print('no counterexample on cycles of order',n)
# Regardless of graph realizability, disjoint nonempty neighbor-color sets
# alone permit a triangle, so they do not prove triangle-freeness.
L=[(frozenset([i]),frozenset(set(range(3))-{i})) for i in range(3)]
H=nx.Graph();H.add_nodes_from(range(3))
for i,j in combinations(range(3),2):
 A,B=L[i];C,D=L[j]
 if A<=D and C<=B:H.add_edge(i,j)
print('abstract A,B-label target contains triangle:',H.number_of_edges()==3)