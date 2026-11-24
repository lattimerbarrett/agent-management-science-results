"""Direct vertex-decomposition of codimension<=2 cochordal facet complexes."""
import networkx as nx
from agent3_checker import subsets,deletion_link,verify
from functools import reduce
from operator import or_

def cone_certificate(c,v):
    if c[0]=='simplex':return ('simplex',c[1]|v)
    return ('shed',c[1],cone_certificate(c[2],v),cone_certificate(c[3],v))

def codim2_certificate(facets):
    fs=tuple(sorted(set(facets)))
    assert fs and len({f.bit_count() for f in fs})==1
    if len(fs)==1:return ('simplex',fs[0])
    U=reduce(or_,fs,0);r=fs[0].bit_count();n=U.bit_count()
    assert n-r<=2
    cone=U
    for f in fs:cone&=f
    if cone:
        v=cone&-cone
        c=cone_certificate(codim2_certificate(tuple(f^v for f in fs)),v)
    elif n-r==1:
        v=U&-U
        de,li=deletion_link(fs,v)
        c=('shed',v,codim2_certificate(de),codim2_certificate(li))
    else:
        H=nx.Graph();H.add_nodes_from(subsets(U,1))
        missing={U^f for f in fs}
        H.add_edges_from(tuple(subsets(e,1)) for e in subsets(U,2) if e not in missing)
        assert nx.is_chordal(H)
        v=next(v for v in H if all(H.has_edge(a,b) for a in H[v] for b in H[v] if a!=b))
        de,li=deletion_link(fs,v)
        assert all(f.bit_count()==r for f in de)
        c=('shed',v,codim2_certificate(de),codim2_certificate(li))
    verify(fs,0,c)
    return c
