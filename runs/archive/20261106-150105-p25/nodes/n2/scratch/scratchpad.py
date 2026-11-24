import networkx as nx
from itertools import combinations
from fractions import Fraction
m,k=5,2
sets=list(combinations(range(m),k))
Q=nx.Graph(); Q.add_nodes_from(range(len(sets)))
Q.add_edges_from((u,v) for u,v in combinations(Q.nodes,2) if not set(sets[u])&set(sets[v]))
G=nx.Graph(); labels={}
for u in Q:
 labels[('v',u)]=(0,sets[u]);G.add_node(('v',u))
for u,v in Q.edges:
 a=('a',u,v);b=('b',u,v)
 labels[a]=(1,sets[u]);labels[b]=(2,sets[u])
 G.add_edges_from([(('v',u),a),(a,b),(b,('v',v))])
L=2
for i in range(3):
 A=[('A',i,j,l) for j in range(m) for l in range(L)]
 B=[('B',i,l) for l in range(k*L)]
 G.add_edges_from((a,b) for a in A for b in B)
 for x,(typ,S) in labels.items():
  if typ==i:
   G.add_edges_from((x,('A',i,j,l)) for j in S for l in range(L))
N={u:set(G[u]) for u in G}
N2={u:set().union(*(N[v] for v in N[u])) for u in G}
bad=[(u,v) for u,v in G.edges if N2[u]&N2[v]]
print('vertices:',len(G),'minimum degree:',min(dict(G.degree()).values()))
print('edges lying in a triangle or pentagon:',len(bad))
print('asymptotic lower ratio for this m,k:',Fraction(k,3*(m+k)))
print('limit as m/k tends to 2:',Fraction(1,9))
