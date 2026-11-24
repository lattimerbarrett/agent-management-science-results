import networkx as nx
from itertools import combinations
# Test the explicit wide-coloring target on a sampled-neighborhood cover.
G=nx.cycle_graph(11)
S=[0,3,6,9]
covered={v for v in G if any(G.has_edge(v,s) for s in S)}
color={v:next(i for i,s in enumerate(S) if G.has_edge(v,s)) for v in covered}
# Use neighborhoods only inside the covered induced subgraph.
labels={v:(color[v],frozenset(color[w] for w in G[v] if w in covered)) for v in covered}
L=set(labels.values()); H=nx.Graph(); H.add_nodes_from(L)
for x,y in combinations(L,2):
 i,A=x;j,B=y
 if i in B and j in A and A.isdisjoint(B):H.add_edge(x,y)
preserved=all(H.has_edge(labels[u],labels[v]) for u,v in G.edges if u in covered and v in covered)
print('sample:',S)
print('uncovered:',set(G)-covered)
print('covered edges preserved:',preserved)
print('target triangles:',sum(nx.triangles(H).values())//3)
print('number of target labels:',len(H))