import networkx as nx
H=nx.Graph([(0,1),(0,4),(0,5),(0,7),(1,2),(1,4),(1,5),(1,6),(1,7),(2,3),(2,5),(3,6)])
patterns=[]
for mask in range(1<<8):
 S=[v for v in range(8) if mask>>v&1]
 if H.subgraph(S).number_of_edges():continue
 F=H.subgraph(set(range(8))-set(S));F=nx.convert_node_labels_to_integers(F.subgraph([v for v,d in F.degree() if d]))
 if not any(nx.is_isomorphic(F,J) for _,J in patterns):patterns.append((S,F))
for S,F in sorted(patterns,key=lambda p:p[1].number_of_edges()):
 if not any(len(J)<=len(F) and J.number_of_edges()<F.number_of_edges() and nx.algorithms.isomorphism.GraphMatcher(F,J).subgraph_is_monomorphic() for _,J in patterns):
  print('minimal: remove',S,'F edges',list(F.edges()),'components',[len(c) for c in nx.connected_components(F)])
print('critical vertices',[v for v in H if nx.is_bipartite(nx.subgraph_view(H,filter_node=lambda u:u!=v))])