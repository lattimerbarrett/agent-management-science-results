"""Independent exact checks for the 8-vertex counterexample.
Uses NetworkX only for finite embedding checks; cycle arithmetic is integer/rational.
Run: python workspace/agent2_counterexample_checks.py
"""
import networkx as nx
from fractions import Fraction
from math import factorial
from itertools import product

EDGES=[(0,4),(0,6),(0,7),(1,6),(1,7),(2,6),(2,7),(3,4),(3,5),(4,7),(5,7),(6,7)]
H=nx.Graph();H.add_nodes_from(range(8));H.add_edges_from(EDGES)

def contains(G,H=H):
    return nx.algorithms.isomorphism.GraphMatcher(G,H).subgraph_is_monomorphic()

def template(a,b):
    G=nx.complete_bipartite_graph(a,b)
    for j in range(a//3):G.add_edges_from([(3*j,3*j+1),(3*j+1,3*j+2)])
    if a%3==2:G.add_edge(a-2,a-1)
    return G

def conv(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def qpoly(a):
    q=[1]
    for j in range(a//3):q=conv(q,[1,9,7,1])
    if a%3==1:q=conv(q,[1,1])
    elif a%3==2:q=conv(q,[1,4,1])
    return q

def cycles_exact(a,b):
    q=qpoly(a)
    c=b*(q[1]-a)//2
    for k in range(2,min(a,b)+1):
        c+=q[k]*factorial(b)//factorial(b-k)*factorial(k-1)//2
    return c

def cycles_dfs(G):
    # Every cycle is counted twice by fixing its least vertex as start.
    total=0
    for root in G:
        def rec(path,seen):
            ans=int(len(path)>=3 and G.has_edge(path[-1],root))
            for nxt in G[path[-1]]:
                if nxt>root and nxt not in seen:
                    ans+=rec(path+[nxt],seen|{nxt})
            return ans
        total+=rec([root],{root})
    return total//2

def f(n):
    return max(a*(n-a)+(2*a)//3 for a in range(n+1))

def checks():
    assert nx.is_tree(H.subgraph(range(7)))
    assert nx.is_bipartite(H.subgraph(range(7)))
    # H embeds in an apex joined to K_{3,4}; every H-free neighborhood avoids K_{3,4}.
    Q=nx.complete_bipartite_graph(3,4);Q.add_node(7);Q.add_edges_from((7,v) for v in range(7))
    assert contains(Q)
    C=10;N=10000;K=24
    assert N//2-40*100-40==960
    assert N//6-1>4*K
    assert N//2-C-2-2*K>=5
    assert 6*(10**8-N)>N*(N-1)//2
    assert not nx.is_bipartite(H)
    patterns=[({7,4,5,6},{0,1,2,3}),({4,6,7,3},{0,1,2,5}),({0,6,7,3},{1,2,4,5})]
    for A,B in patterns:
        assert not H.subgraph(B).number_of_edges()
    assert sorted(dict(H.subgraph(patterns[0][0]).degree()).values())==[1,1,1,3]
    assert sorted(dict(H.subgraph(patterns[1][0]).degree()).values())==[1,1,2,2]
    assert sorted(dict(H.subgraph(patterns[2][0]).degree()).values())==[0,2,2,2]
    assert list(H.subgraph({6,7,3}).edges())==[(6,7)]
    assert list(H.subgraph({0,4,1,2,5}).edges())==[(0,4)]
    # Enumerate every possible single-part defect and certify no P3-factor embedding.
    for mask in range(1<<8):
        A={v for v in H if mask>>v&1};B=set(H)-A
        if H.subgraph(B).number_of_edges():continue
        F=H.subgraph(A)
        assert any(len(C)>=4 or F.subgraph(C).number_of_edges()>=3 for C in nx.connected_components(F))
    for a,b in [(3,5),(4,4),(5,3),(6,3),(4,5)]:
        assert not contains(template(a,b)),(a,b)
    for a in range(1,6):
        for b in range(1,5):
            assert cycles_exact(a,b)==cycles_dfs(template(a,b)),(a,b)
    for n in range(1,401):
        t=(n*n)//4
        assert Fraction(n,3)-2<=f(n)-t<=Fraction(n,3)+1
        if n>=2:assert f(n)-f(n-1)>=Fraction(n,2)-4
        if n%6==0:
            m=n//2
            vals=[a*(n-a)+(2*a)//3 for a in range(n+1)]
            assert vals[m]==max(vals) and vals.count(max(vals))==1
    # Rigorous rational certificate for S1>S0, z=7/3.
    z=Fraction(7,3)
    lower=sum(z**(j+2)/Fraction(factorial(j)*factorial(j+2)) for j in range(3))
    upper=sum(z**j/Fraction(factorial(j)**2) for j in range(3))
    upper+=z**3/Fraction(factorial(3)**2)/(1-z/Fraction(4**2))
    assert lower==Fraction(21217,3888)
    assert upper==Fraction(67849,13284)
    assert lower-upper==Fraction(55709,159408)>0
    print('All independent finite embedding, arithmetic, cycle-DFS and rational-tail checks passed.')
    print('Certified limiting gap >',lower-upper)
    for m in [6,12,30,60,120]:
        c0=cycles_exact(m,m);c1=cycles_exact(m+1,m-1)
        print('m=',m,'imbalanced/balanced exact ratio=',float(Fraction(c1,c0)))

if __name__=='__main__':checks()
