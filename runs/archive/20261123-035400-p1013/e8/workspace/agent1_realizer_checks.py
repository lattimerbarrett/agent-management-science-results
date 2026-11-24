from itertools import product
import networkx as nx
import numpy as np

def product_graph(r,m):
    verts=list(product(range(r),repeat=m))
    G=nx.Graph();G.add_nodes_from(verts)
    G.add_edges_from((u,v) for j,u in enumerate(verts) for v in verts[:j] if all(a!=b for a,b in zip(u,v)))
    return G

def check_dictators(r,m):
    G=product_graph(r,m)
    target=r**(m-1)
    maximum=[]
    for c in nx.find_cliques(nx.complement(G)):
        assert len(c)<=target
        if len(c)==target: maximum.append(frozenset(c))
    dictators={frozenset(v for v in G if v[j]==a) for j in range(m) for a in range(r)}
    assert set(maximum)==dictators
    eigen=np.linalg.eigvalsh(nx.to_numpy_array(G))
    assert abs(eigen[0]+(r-1)**(m-1))<1e-7
    # Multiplicity of the least eigenvalue, the one-coordinate eigenspace.
    assert sum(abs(x-eigen[0])<1e-7 for x in eigen)==m*(r-1)
    return len(G),len(maximum)

if __name__=='__main__':
    for r,m in [(3,1),(3,2),(3,3),(4,2),(5,2)]:
        print(r,m,check_dictators(r,m))
