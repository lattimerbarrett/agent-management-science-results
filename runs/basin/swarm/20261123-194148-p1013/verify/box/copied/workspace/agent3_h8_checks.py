import networkx as nx
H_EDGES=[(0,4),(0,5),(0,6),(0,7),(1,3),(1,7),(2,3),(2,6),(2,7),(4,7),(5,7),(6,7)]
H=nx.Graph();H.add_nodes_from(range(8));H.add_edges_from(H_EDGES)
def in_p3_union(G):
 return all(len(c)<=3 and G.subgraph(c).number_of_edges()<=2 for c in nx.connected_components(G))
def one_part_host(F):
 for mask in range(256):
  A={v for v in H if mask>>v&1};B=set(H)-A
  if H.subgraph(B).number_of_edges():continue
  if all(nx.algorithms.isomorphism.GraphMatcher(F,H.subgraph(c)).subgraph_is_monomorphic() for c in nx.connected_components(H.subgraph(A))):return A
 return None
assert not nx.is_bipartite(H)
assert nx.is_bipartite(H.subgraph(set(H)-{7}))
assert one_part_host(nx.path_graph(3)) is None
for name,F in [('P4',nx.path_graph(4)),('claw',nx.star_graph(3)),('triangle',nx.complete_graph(3))]:
 A=one_part_host(F);assert A is not None
 print(name,sorted(A),list(H.subgraph(A).edges()))
A={0,4,1,2};B=set(H)-A
assert list(H.subgraph(A).edges())==[(0,4)]
assert in_p3_union(H.subgraph(B))
assert H.subgraph(B).number_of_edges()==2
for edge in H_EDGES:
 J=H.copy();J.remove_edge(*edge)
 good=False
 for mask in range(256):
  A={v for v in J if mask>>v&1};B=set(J)-A
  if not J.subgraph(B).number_of_edges() and in_p3_union(J.subgraph(A)):
   good=True;break
 assert good,edge
print('All H8 witnesses, 256-coloring nonembedding, and edge-minimality checked.')
