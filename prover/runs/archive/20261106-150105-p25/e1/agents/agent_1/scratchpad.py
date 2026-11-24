import networkx as nx
for F in [nx.cycle_graph(5),nx.cycle_graph(7),nx.petersen_graph(),nx.complete_bipartite_graph(3,3)]:
 G=nx.Graph();G.add_nodes_from(F)
 for i,(u,v) in enumerate(F.edges):G.add_edges_from([(u,('b',i)),(('b',i),('c',i)),(('c',i),v)])
 P=nx.Graph();P.add_nodes_from(G)
 for u in G:
  for a in G[u]:
   P.add_edge(u,a)
   for b in G[a]:
    for v in G[b]:P.add_edge(u,v)
 I=P.subgraph([v for v in G if v not in F])
 print(len(F),sum(nx.triangles(I).values())//3,max(nx.coloring.greedy_color(I).values())+1)
