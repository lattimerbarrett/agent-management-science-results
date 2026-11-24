import networkx as nx
from fractions import Fraction
E=[(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),(2,5),(2,7),(3,7),(4,7),(6,7)]
H=nx.Graph(E)
FAMILY=[nx.complete_graph(3),nx.star_graph(3),nx.path_graph(4)]
seen=set()
for mask in range(256):
    I=[v for v in range(8) if mask>>v&1]
    if H.subgraph(I).number_of_edges():continue
    Q=H.subgraph(set(H)-set(I)).copy()
    assert any(nx.algorithms.isomorphism.GraphMatcher(Q,F).subgraph_is_monomorphic() for F in FAMILY)
    Q.remove_nodes_from(list(nx.isolates(Q)))
    for i,F in enumerate(FAMILY):
        if nx.is_isomorphic(Q,F):seen.add(i)
assert seen=={0,1,2}
assert nx.is_bipartite(H.subgraph(set(H)-{7}))
assert H.subgraph({1,2,3,4,6}).number_of_edges()==1
assert H.subgraph({0,5,7}).number_of_edges()==1
assert max(dict(H.subgraph({1,2,3,4,6}).degree()).values())==1
assert max(dict(H.subgraph({0,5,7}).degree()).values())==1
# Exact extremal edge objective within the complete-join class.
for k in range(1,101):
    n=6*k
    vals=[m*(n-m)+m-((m+2)//3) for m in range(n+1)]
    assert [m for m,v in enumerate(vals) if v==max(vals)]==[3*k]
    assert max(vals)==9*k*k+2*k
# Positive rational certificate used in the asymptotic cycle comparison.
from math import factorial
S=sum(Fraction((l*(l-1)-1)*7**l,3**l*factorial(l)**2) for l in range(5))
assert S==Fraction(16715,46656)>0
print('All H8 decomposition, two-part, edge-objective, and rational-series checks passed.')
