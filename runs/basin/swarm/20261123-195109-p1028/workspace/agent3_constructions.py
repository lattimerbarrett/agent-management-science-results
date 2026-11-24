"""Exact lower-bound constructions for the quartic conjectured formula.
Run as Python; uses networkx and sympy only.
"""
import networkx as nx
import sympy as sp
from fractions import Fraction
EXAMPLES = {('cap', 6): [[0, 3], [0, 4], [1, 5], [1, 2], [1, 3], [1, 4], [2, 5], [2, 4], [2, 3], [3, 5], [4, 5]], ('cap', 7): [[0, 2], [0, 6], [1, 2], [1, 3], [1, 4], [1, 5], [2, 6], [2, 3], [3, 4], [3, 5], [4, 6], [4, 5], [5, 6]], ('cap', 8): [[0, 6], [0, 3], [1, 6], [1, 5], [1, 4], [1, 2], [2, 3], [2, 4], [2, 5], [3, 7], [3, 6], [4, 7], [4, 5], [5, 7], [6, 7]], ('cap', 9): [[0, 4], [0, 5], [1, 3], [1, 6], [1, 7], [1, 2], [2, 3], [2, 7], [2, 6], [3, 4], [3, 5], [4, 8], [4, 5], [5, 8], [6, 8], [6, 7], [7, 8]], ('cap', 10): [[0, 2], [0, 5], [1, 4], [1, 3], [1, 6], [1, 9], [2, 8], [2, 4], [2, 5], [3, 9], [3, 6], [3, 7], [4, 8], [4, 5], [5, 8], [6, 7], [6, 9], [7, 9], [7, 8]], ('bead', 6): [[0, 4], [0, 3], [1, 5], [1, 2], [2, 5], [2, 3], [2, 4], [3, 5], [3, 4], [4, 5]], ('bead', 8): [[0, 7], [0, 3], [1, 2], [1, 6], [2, 4], [2, 5], [2, 6], [3, 4], [3, 7], [3, 5], [4, 6], [4, 7], [5, 6], [5, 7]]}

def resistance(G,s,t):
    if s==t:return sp.Rational(0)
    nodes=list(G); others=[v for v in nodes if v!=t]
    L=sp.zeros(len(others)); ids={v:i for i,v in enumerate(others)}
    for u in others:
        L[ids[u],ids[u]]=G.degree(u)
        for v in G[u]:
            if v!=t:L[ids[u],ids[v]]=-1
    b=sp.zeros(len(others),1);b[ids[s]]=1
    return (L.inv()*b)[ids[s]]

def component(typ,m):
    G=nx.Graph(); G.add_nodes_from(range(m));G.add_edges_from(EXAMPLES[typ,m])
    if typ=='bead':return G,0,1
    vals=[resistance(G,0,v) for v in G]
    return G,0,max(G,key=lambda v:vals[v])

def quartic(n):
    assert n>=15 and n%2
    r=n%5
    other={0:10,1:6,2:7,3:6,4:9}[r]
    G,port,s=component('cap',6)
    bead_sizes=[8] if r==3 else []
    base=6+other-1+sum(m-1 for m in bead_sizes)
    assert n>=base and (n-base)%5==0
    bead_sizes += [6]*((n-base)//5)
    for m in bead_sizes:
        H,a,b=component('bead',m)
        mapping={a:port};cur=max(G)+1
        for v in H:
            if v!=a:mapping[v]=cur;cur+=1
        G.add_edges_from((mapping[x],mapping[y]) for x,y in H.edges())
        port=mapping[b]
    H,a,t=component('cap',other)
    mapping={a:port};cur=max(G)+1
    for v in H:
        if v!=a:mapping[v]=cur;cur+=1
    G.add_edges_from((mapping[x],mapping[y]) for x,y in H.edges())
    return G,s,mapping[t]

def claimed_R(n):
    c={0:sp.Rational(7,5),1:sp.Rational(23,20),2:sp.Rational(149,115),3:sp.Rational(7,5),4:sp.Rational(139,90)}[n%5]
    return sp.Rational(n,4)-c

if __name__=='__main__':
    for m in range(6,11):
        G,s,t=component('cap',m)
        assert sorted(dict(G.degree()).values())==[2]+[4]*(m-1)
        print('cap',m,resistance(G,s,t))
    for n in range(15,66,2):
        G,s,t=quartic(n)
        assert len(G)==n and nx.is_connected(G) and set(dict(G.degree()).values())=={4}
        actual=resistance(G,s,t)
        assert actual==claimed_R(n),(n,actual,claimed_R(n))
        print(n,actual,'tau lower',4*n*actual)
