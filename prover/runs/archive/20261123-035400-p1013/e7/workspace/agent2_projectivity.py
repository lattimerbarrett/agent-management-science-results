"""Computational certificates for tensor-clique projectivity used in realization."""
from itertools import product
from collections import Counter
import networkx as nx

def tensor_clique(r,k):
    V=list(product(range(r),repeat=k))
    G=nx.Graph();G.add_nodes_from(V)
    G.add_edges_from((x,y) for ii,x in enumerate(V) for y in V[ii+1:] if all(a!=b for a,b in zip(x,y)))
    return G

def verify(r,k):
    G=tensor_clique(r,k)
    indeps=list(nx.find_cliques(nx.complement(G)))
    alpha=max(map(len,indeps))
    maxima={frozenset(S) for S in indeps if len(S)==alpha}
    fibers={frozenset(v for v in G if v[i]==c) for i in range(k) for c in range(r)}
    assert alpha==r**(k-1)
    assert maxima==fibers
    # Tensor spectrum, including multiplicities, and uniqueness of first level.
    ev=Counter()
    from math import comb
    for s in range(k+1):ev[(-1)**s*(r-1)**(k-s)]+=comb(k,s)*(r-1)**s
    assert min(ev)==-(r-1)**(k-1)
    assert ev[min(ev)]==k*(r-1)
    assert sum(ev.values())==r**k
    return len(G),len(indeps),len(maxima)

if __name__=='__main__':
    for r,k in [(3,2),(3,3),(4,2),(5,2)]:
        print(r,k,verify(r,k))
