import networkx as nx
from itertools import combinations

def odd3(G):
 P=nx.Graph();P.add_nodes_from(G)
 for u in G:
  reach={u}
  for _ in range(3):reach={w for v in reach for w in G[v]}
  for v in reach:P.add_edge(u,v)
 return P
# The original vertices of a three-edge subdivision induce precisely Q in odd3.
Q=nx.complete_graph(6)
F=nx.Graph();F.add_nodes_from(Q)
for e,(u,v) in enumerate(Q.edges):
 a=('a',e);b=('b',e)
 F.add_edges_from([(u,a),(a,b),(b,v)])
P=odd3(F)
print('3-subdivision: odd3 on original vertices equals Q:',set(P.subgraph(Q).edges)==set(Q.edges))
print('3-subdivision: loops in odd3:',list(nx.selfloop_edges(P)))
# Explicit universal target from a proper coloring of odd3.
k=4
labels=[(i,frozenset(j for j in range(k) if mask>>j&1)) for i in range(k) for mask in range(1<<k) if not (mask>>i&1)]
T=nx.Graph();T.add_nodes_from(labels)
for x,y in combinations(labels,2):
 i,A=x;j,B=y
 if i in B and j in A and A.isdisjoint(B):T.add_edge(x,y)
print('universal target:',len(T),'vertices;',T.number_of_edges(),'edges;',sum(nx.triangles(T).values())//3,'triangles')
# Circular generalized Andrasfai examples do not give the required lower bound.
for r in [2,3,4]:
 n=5*r+2;q=2*r+1
 A=nx.Graph();A.add_nodes_from(range(n))
 A.add_edges_from((u,v) for u,v in combinations(range(n),2) if q<=v-u<=n-q)
 cmap={u:(2*((5*u)//n))%5 for u in A}
 C5=nx.cycle_graph(5)
 ok=all(C5.has_edge(cmap[u],cmap[v]) for u,v in A.edges)
 print('circular example',r,'vertices',n,'C5 homomorphism:',ok,'odd3 proper 5-color:',all(cmap[u]!=cmap[v] for u,v in odd3(A).edges))