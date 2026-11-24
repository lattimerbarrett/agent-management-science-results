"""Checks the partial lower construction with three separate cap/support pairs.
For each input F with disjoint-set coloring D[u], form S3(F); attach caps
separately for its three proper vertex parts. Core oddthird coloring uses
D[u] at branches and the opposite branch endpoint at subdivision vertices.
This is a verified c<1/9 partial construction when Kneser graphs are used,
or fully elementary c<1/15 using shift graphs. Not the desired sharp lower.
"""
import networkx as nx
import numpy as np

def construct(F,D,ground):
    C=nx.Graph();part={};col={}
    for u in F:
        C.add_node(('u',u));part[('u',u)]=0;col[('u',u)]=set(D[u])
    for e,(u,v) in enumerate(F.edges()):
        b=('b',e);c=('c',e)
        C.add_edges_from([(('u',u),b),(b,c),(c,('u',v))])
        part[b]=1;part[c]=2;col[b]=set(D[v]);col[c]=set(D[u])
    for a in C:
        for b in C[a]:
            assert not(col[a]&col[b])
            for c in C[b]:
                for d in C[c]:assert not(col[a]&col[d]),(a,d)
    G=C.copy()
    for r in range(3):
        for x in ground:
            cap=('cap',r,x);G.add_edge(cap,('support',r))
            G.add_edges_from((v,cap) for v in C if part[v]==r and x in col[v])
    A=nx.to_numpy_array(G,dtype=np.int64)
    assert np.trace(np.linalg.matrix_power(A,3))==0
    assert np.trace(np.linalg.matrix_power(A,5))==0
    return G

if __name__=='__main__':
    # Petersen graph as KG(5,2)
    import itertools
    vv=list(itertools.combinations(range(5),2))
    F=nx.Graph();F.add_nodes_from(vv)
    F.add_edges_from((u,v) for u,v in itertools.combinations(vv,2) if not(set(u)&set(v)))
    G=construct(F,{u:set(u) for u in F},range(5))
    print('KG(5,2) seed:',len(F),F.number_of_edges(),'augmented',len(G),G.number_of_edges())
    # Shift graph on arcs of [5], fractional 4-coloring by all directed cuts.
    n=5;vv=list(itertools.combinations(range(n),2))
    F=nx.Graph();F.add_nodes_from(vv)
    F.add_edges_from(((i,j),(j,k)) for i,j,k in itertools.combinations(range(n),3))
    ground=range(1<<n)
    D={(i,j):{s for s in ground if (s>>i)&1 and not((s>>j)&1)} for i,j in F}
    assert all(len(x)==(1<<(n-2)) for x in D.values())
    G=construct(F,D,ground)
    print('shift(5) seed:',len(F),F.number_of_edges(),'augmented',len(G),G.number_of_edges())
