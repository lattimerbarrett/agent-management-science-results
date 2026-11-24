import networkx as nx
H=nx.Graph();H.add_edges_from([(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4),(4,1),(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
for k in range(2,8):
 G=nx.complete_bipartite_graph(10+k,10)
 A=list(range(k));z=20+k;G.add_node(z);G.add_edges_from((z,v) for v in range(20+k) if v not in A)
 G.add_edges_from((i,j) for i in A for j in A if i<j)
 GM=nx.algorithms.isomorphism.GraphMatcher(G,H)
 found=GM.subgraph_is_monomorphic()
 print('bad clique',k,'extra gain',k*(k-1)//2-k,'contains',found,flush=True)
 if found:print('map',{v:u for u,v in GM.mapping.items()},flush=True)
