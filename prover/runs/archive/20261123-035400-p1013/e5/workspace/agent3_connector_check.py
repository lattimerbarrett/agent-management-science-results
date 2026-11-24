import networkx as nx,itertools,json
H=nx.Graph([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(1,5),(5,3),(2,6),(6,4)])
def core(G):
 G=G.copy();G.remove_nodes_from(list(nx.isolates(G)));return nx.convert_node_labels_to_integers(G)
def sub(A,B):return nx.algorithms.isomorphism.GraphMatcher(B,A).subgraph_is_monomorphic()
pats=[]
for colors in itertools.product(range(2),repeat=7):
 pair=tuple(core(H.subgraph([v for v in H if colors[v]==i])) for i in (0,1))
 if any(sub(p[0],pair[0]) and sub(p[1],pair[1]) for p in pats):continue
 pats=[p for p in pats if not(sub(pair[0],p[0]) and sub(pair[1],p[1]))]
 pats.append(pair)
assert len(pats)==4
star=nx.path_graph(3);matching=nx.Graph([(0,1),(2,3)]);empty=nx.empty_graph()
expected=[(star,empty),(matching,empty),(empty,star),(empty,matching)]
assert all(any(nx.is_isomorphic(a,x) and nx.is_isomorphic(b,y) for x,y in expected) for a,b in pats)
print("All 128 colorings checked; exact minimal decomposition pairs:")
for a,b in pats: print(list(a.edges()),list(b.edges()))
