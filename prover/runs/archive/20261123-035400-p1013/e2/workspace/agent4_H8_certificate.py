"""Independent exact finite checks for the H8 obstruction."""
import networkx as nx
from collections import defaultdict
from math import factorial
from fractions import Fraction

H=nx.from_graph6_bytes(b'GE`cFs')

def contains(G,F):
    return nx.algorithms.isomorphism.GraphMatcher(G,F).subgraph_is_monomorphic()

def p3_cycles(a,b):
    Q={(0,0):1,(1,1):3,(2,2):3,(2,1):4,(3,3):1,(3,2):4,(3,1):2}
    P={(0,0):1}
    for T in [Q]*(a//3)+[{(0,0):1,(1,1):1}]*(a%3):
        R=defaultdict(int)
        for (v,k),c in P.items():
            for (w,j),d in T.items():R[v+w,k+j]+=c*d
        P=R
    twice=sum(c*factorial(k-1)*factorial(b)//factorial(b-k) for (v,k),c in P.items() if 1<=k<=b and v+k>=3)
    assert twice%2==0
    return twice//2

def template(a,b):
    G=nx.complete_bipartite_graph(a,b)
    for v in range(0,a-2,3):G.add_edges_from([(v,v+1),(v+1,v+2)])
    return G

def brute_cycles(G):
    ans=0
    for v in G:
        def dfs(path,seen):
            nonlocal ans
            for w in G[path[-1]]:
                if w==v and len(path)>=3:ans+=1
                elif w>v and w not in seen:dfs(path+[w],seen|{w})
        dfs([v],{v})
    assert ans%2==0
    return ans//2

if __name__=='__main__':
    assert nx.is_bipartite(H.subgraph(set(H)-{7}))
    assert not nx.is_bipartite(H)
    D=[nx.star_graph(3),nx.path_graph(4),nx.cycle_graph(3)]
    # Every possible independent ordinary side leaves one forbidden internal graph.
    for mask in range(1<<8):
        A={v for v in H if mask>>v&1}
        if H.subgraph(A).number_of_edges()==0:
            assert any(contains(H.subgraph(set(H)-A),F) for F in D)
    # Explicit two-internal-edge embedding partition.
    assert set(H.subgraph({7,0,5}).edges())=={(0,7)}
    assert set(H.subgraph({1,2,3,4,6}).edges())=={(1,3)}
    for a in range(1,8):
        for b in range(1,8):
            if a+b<=10:
                assert p3_cycles(a,b)==brute_cycles(template(a,b))
                assert not contains(template(a,b),H)
    q=Fraction(7,3);K=20
    A=sum((q**k/Fraction(factorial(k)**2) for k in range(K+1)),Fraction())
    B=sum((q**(k+2)/Fraction(factorial(k)*factorial(k+2)) for k in range(K+1)),Fraction())
    nextA=q**(K+1)/factorial(K+1)**2
    tailA=nextA/(1-q/Fraction((K+2)**2))
    assert B>A+tailA
    print('All H8 local certificates, finite subgraph tests and exact cycle checks passed.')
    print('Limiting cycle constants: balanced',float(A),'shifted',float(B))
    for m in [24,30,60]:
        E=p3_cycles(m,m);F=p3_cycles(m+1,m-1)
        assert F>E
        print('m=',m,'ratio shifted / balanced=',float(Fraction(F,E)))
