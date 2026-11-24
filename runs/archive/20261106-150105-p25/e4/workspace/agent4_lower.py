"""Exact, executable checks for the lower-bound construction."""
import itertools
from fractions import Fraction
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix

def subdivision(F, orientation=None):
    """Return S(F), vertex types 0/1/2, and labels in V(F)."""
    G=nx.Graph(); typ={}; lab={}
    for u in F:
        v=('v',u); G.add_node(v); typ[v]=0; lab[v]=u
    for j,(u,v) in enumerate(F.edges()):
        if orientation is not None and orientation[j]: u,v=v,u
        a=('a',j); b=('b',j)
        G.add_edges_from([(('v',u),a),(a,b),(b,('v',v))])
        typ[a]=1; typ[b]=2; lab[a]=u; lab[b]=v
    return G,typ,lab

def kneser(m,k):
    sets=list(itertools.combinations(range(m),k)); F=nx.Graph(); F.add_nodes_from(sets)
    for S,T in itertools.combinations(sets,2):
        if set(S).isdisjoint(T): F.add_edge(S,T)
    return F

def construction(m,k,L=1):
    F=kneser(m,k); G,typ,lab=subdivision(F)
    for t in range(3):
        big=[('pool',t,i,j) for i in range(m) for j in range(L)]
        small=[('leaf',t,j) for j in range(k*L)]
        G.add_edges_from(itertools.product(big,small))
    for v in typ:
        G.add_edges_from((v,('pool',typ[v],i,j)) for i in lab[v] for j in range(L))
    return F,G

def odd_closed_walks(G,length):
    A=nx.to_scipy_sparse_array(G,dtype=np.int64,format='csr')
    P=A.copy()
    for _ in range(length-1): P=P@A
    return int(P.diagonal().sum())

def check_symbolic_local_rule():
    # Every core walk of length <=3 involves at most four original labels.
    # All orientations are included; completing the underlying graph to K4
    # cannot remove the walk. The checks concern only same-type endpoints.
    F=nx.complete_graph(4)
    count=0
    for orient in itertools.product((False,True),repeat=6):
        S,typ,lab=subdivision(F,orient)
        for start in S:
            frontier=[start]
            for length in range(1,4):
                frontier=[v for u in frontier for v in S[u]]
                if length in (1,3):
                    for end in frontier:
                        if typ[start]==typ[end]:
                            assert F.has_edge(lab[start],lab[end])
                            count+=1
    return count

def check_instance(m,k,L):
    F,G=construction(m,k,L)
    expected=3*(m+k)*L+F.number_of_nodes()+2*F.number_of_edges()
    assert len(G)==expected
    assert min(dict(G.degree()).values())>=k*L
    assert odd_closed_walks(G,3)==0
    assert odd_closed_walks(G,5)==0
    return len(G),G.number_of_edges(),min(dict(G.degree()).values())

def choose_parameters(h,c):
    """h=|H|, rational 0<=c<1/9. Output explicit k,m,L."""
    c=Fraction(c)
    assert h>=0 and 0<=c<Fraction(1,9)
    k=1
    while Fraction(k,3*(3*k+h))<=c: k+=1
    m=2*k+h
    from math import comb
    core=comb(m,k)+2*(comb(m,k)*comb(m-k,k)//2)
    L=1
    if c:
        # (k-3c(m+k))L >= c*core.
        ratio=c*core/(k-3*c*(m+k))
        L=max(1,(ratio.numerator+ratio.denominator-1)//ratio.denominator)
    assert Fraction(k*L,3*(m+k)*L+core)>=c
    # Lovasz's Kneser theorem: chi(KG(m,k))=m-2k+2=h+2>h.
    return k,m,L

if __name__=='__main__':
    print('symbolic same-type odd-walk checks:',check_symbolic_local_rule())
    for args in [(3,1,1),(5,2,1),(6,2,1),(5,2,2)]:
        print('instance',args,'(vertices,edges,min degree)=',check_instance(*args))
    for h,c in [(3,Fraction(1,10)),(10,Fraction(11,100)),(0,Fraction(0))]:
        print('parameters',h,c,choose_parameters(h,c))
