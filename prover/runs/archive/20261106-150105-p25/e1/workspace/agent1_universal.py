import itertools
import networkx as nx
def universal(k):
    vs=[x for x in itertools.product(range(3),repeat=k) if x.count(0)==1 and 1 in x]
    H=nx.Graph(); H.add_nodes_from(vs)
    for x,y in itertools.combinations(vs,2):
        if all(abs(a-b)==1 or a==b==2 for a,b in zip(x,y)): H.add_edge(x,y)
    return H
