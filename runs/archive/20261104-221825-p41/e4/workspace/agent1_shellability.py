"""Exact shelling checker and constructive equivalence with d-decomposability.
No completion theorem is assumed here.
"""
from functools import lru_cache
from itertools import combinations
from agent3_checker import subsets,certificate,verify

def faces(facets):
    return set(g for f in facets for g in subsets(f))

def restriction(previous,facet):
    new=set(subsets(facet))-faces(previous)
    if not new:return None
    mins=[x for x in new if not any(y!=x and y&x==y for y in new)]
    if len(mins)!=1:return None
    r=mins[0]
    assert new=={g for g in subsets(facet) if g&r==r}
    return r

def verify_shelling(order):
    assert order and len(set(order))==len(order)
    assert len({f.bit_count() for f in order})==1
    for i,f in enumerate(order):
        assert restriction(order[:i],f) is not None
    return True

@lru_cache(None)
def shelling(facets):
    if len(facets)==1:return facets
    for f in facets:
        prev=tuple(g for g in facets if g!=f)
        if restriction(prev,f) is None:continue
        order=shelling(prev)
        if order is not None:return order+(f,)
    return None

def shelling_to_decomposition(order):
    verify_shelling(order)
    if len(order)==1:return ('simplex',order[0])
    r=restriction(order[:-1],order[-1])
    assert r and all(f&r!=r for f in order[:-1])
    return ('shed',r,shelling_to_decomposition(order[:-1]),('simplex',order[-1]^r))

def decomposition_to_shelling(cert):
    if cert[0]=='simplex':return (cert[1],)
    _,s,dc,lc=cert
    de=decomposition_to_shelling(dc)
    li=decomposition_to_shelling(lc)
    order=de+tuple(s|f for f in li)
    verify_shelling(order)
    return order

def test(nmax=5):
    tested=shellable_count=0
    for n in range(1,nmax+1):
      for rank in range(1,n+1):
        universe=tuple(sum(1<<i for i in c) for c in combinations(range(n),rank))
        for mask in range(1,1<<len(universe)):
            fs=tuple(f for i,f in enumerate(universe) if mask>>i&1)
            order=shelling(fs)
            cert=certificate(fs,rank-1)
            assert (order is None)==(cert is None),(fs,order,cert)
            tested+=1
            if cert is not None:
                shellable_count+=1
                verify(fs,rank-1,shelling_to_decomposition(order))
                back=decomposition_to_shelling(cert)
                assert set(back)==set(fs)
    return tested,shellable_count

if __name__=='__main__':
    print('Tested complexes and shellable complexes:',test())
