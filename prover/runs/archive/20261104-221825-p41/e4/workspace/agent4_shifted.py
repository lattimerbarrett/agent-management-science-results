import itertools

def facets_complex(facets):
    return {frozenset(t) for f in facets for r in range(len(f)+1) for t in itertools.combinations(f,r)}

def maxfaces(C):
    return [f for f in C if not any(f<g for g in C)]

def witness_shifted(C):
    facets=maxfaces(C)
    assert len({len(f) for f in facets})==1
    W=set().union(*C)
    if len(facets)==1:
        return ('simplex',tuple(sorted(facets[0])))
    n=max(W)
    D={f for f in C if n not in f}
    L={f-{n} for f in C if n in f}
    assert all(len(f)==len(facets[0]) for f in maxfaces(D))
    return ('shed',n,witness_shifted(D),witness_shifted(L))

def verify(C,w):
    if w[0]=='simplex':
        assert C==facets_complex([w[1]])
        return
    _,v,a,b=w
    assert frozenset([v]) in C
    D={f for f in C if v not in f}
    L={f-{v} for f in C if v in f}
    assert len({len(f) for f in maxfaces(C)})==1
    assert {len(f) for f in maxfaces(D)}=={len(next(iter(maxfaces(C))))}
    verify(D,a);verify(L,b)

