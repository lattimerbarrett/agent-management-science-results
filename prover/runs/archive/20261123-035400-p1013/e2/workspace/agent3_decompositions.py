import networkx as nx

def witness():
 g=nx.Graph();g.add_nodes_from(range(10))
 g.add_edges_from((i,i+1) for i in [0,1,2,3,5,6,7,8])
 g.add_edges_from((u,v) for u in range(5) for v in range(5,10))
 g.remove_edges_from([(0,5),(0,9),(2,9),(4,5),(4,7)])
 return g

def minimal_decompositions():
 g=witness();V=set(g);D=[]
 for mask in range(1<<len(g)):
  A={v for v in V if mask>>v&1}
  if not nx.is_bipartite(g.subgraph(V-A)):continue
  h=g.subgraph(A).copy();h.remove_nodes_from(list(nx.isolates(h)))
  if not any(nx.is_isomorphic(h,k) for k in D):D.append(h)
 D.sort(key=lambda h:(h.number_of_edges(),len(h)))
 mins=[]
 for h in D:
  if not any(nx.algorithms.isomorphism.GraphMatcher(h,k).subgraph_is_monomorphic() for k in mins):mins.append(h)
 expected=[nx.cycle_graph(4),nx.path_graph(5),nx.disjoint_union(nx.path_graph(4),nx.path_graph(2))]
 assert len(mins)==len(expected)==3
 assert all(any(nx.is_isomorphic(h,k) for k in expected) for h in mins)
 return len(D),[(len(h),h.number_of_edges(),sorted(dict(h.degree()).values())) for h in mins]
if __name__=='__main__':print(minimal_decompositions())
