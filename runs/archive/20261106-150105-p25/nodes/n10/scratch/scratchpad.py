import networkx as nx
from itertools import combinations
q=5
vertices=[(i, mask) for i in range(q) for mask in range(1<<q) if not mask>>i&1]
W=nx.Graph();W.add_nodes_from(vertices)
for (i,A),(j,B) in combinations(vertices,2):
    if B>>i&1 and A>>j&1 and not (A&B): W.add_edge((i,A),(j,B))
witness=[(i,(1<<((i-1)%5)) | (1<<((i+1)%5))) for i in range(5)]
print('Target order:',len(W))
print('Number of triangles:',sum(nx.triangles(W).values())//3)
print('Explicit pentagon in target:',all(W.has_edge(witness[i],witness[(i+1)%5]) for i in range(5)))
print('Number of edges:',W.number_of_edges())
