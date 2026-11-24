"""Exact checks for saturated-ladder fractional obstruction.
T_m has m disjoint five-vertex paths; a_i b_j edges for i<j.
Support excludes four vertices in each end block.
All checks use integer arithmetic and complete maximal-independent enumeration.
"""
import networkx as nx
from fractions import Fraction

def template(m):
    G=nx.Graph()
    G.add_nodes_from((i,r) for i in range(m) for r in range(5))
    G.add_edges_from(((i,r),(i,r+1)) for i in range(m) for r in range(4))
    G.add_edges_from(((i,0),(j,4)) for i in range(m) for j in range(i+1,m))
    return G

def oddthird(G):
    F=nx.Graph()
    F.add_nodes_from(G)
    F.add_edges_from(G.edges())
    for a in G:
        for b in G[a]:
            for c in G[b]:
                for d in G[c]:
                    assert a!=d, "triangle in G"
                    F.add_edge(a,d)
    return F

def support(m):
    return {(0,0),(m-1,4)} | {(i,r) for i in range(1,m-1) for r in range(5)}

def check(m):
    G=template(m)
    F=oddthird(G)
    U=support(m)
    J=F.subgraph(U)
    alpha=max(map(len,nx.find_cliques(nx.complement(J))))
    assert len(U)==5*m-8
    assert alpha==m-1,(m,alpha)
    # Every supported independent set weighs at most 1 with weight 1/(m-1).
    return m,len(G),len(U),alpha,Fraction(len(U),alpha)

if __name__=='__main__':
    for m in range(3,10):print(check(m))
