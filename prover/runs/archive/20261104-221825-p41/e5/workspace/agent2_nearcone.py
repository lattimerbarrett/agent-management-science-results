from itertools import combinations
from functools import lru_cache
from exact_decomp_a4 import complex_from_facets, facets, kd, subfaces

@lru_cache(None)
def witness(C,k):
    fs=facets(C)
    if len(fs)==1:return None
    size=len(next(iter(fs)))
    assert all(len(f)==size for f in fs)
    for s in sorted(C,key=lambda s:(len(s),tuple(sorted(s)))):
        if not s or len(s)>k+1:continue
        D=frozenset(g for g in C if not s<=g)
        if not D or any(len(f)!=size for f in facets(D)):continue
        L=frozenset(g-s for g in C if s<=g)
        if kd(D,k) and kd(L,k):return s,D,L
    raise ValueError('not k-decomposable')

def nearcone_order(C,k):
    fs=facets(C)
    if len(fs)==1:
        f=next(iter(fs))
        return [f-{v} for v in sorted(f)]
    s,D,L=witness(C,k)
    return nearcone_order(D,k)+[s|r for r in nearcone_order(L,k)]

def check(C,k,a):
    order=nearcone_order(C,k)
    d=len(next(iter(facets(C))))-1
    expected={f for f in C if len(f)==d} if d>=0 else set()
    assert len(order)==len(set(order)) and set(order)==expected
    X=C
    for r in order:
        X=X|subfaces(r|{a})
        assert kd(X,k),(C,k,r)
    return len(order)

if __name__=='__main__':
    import json
    results=[]
    for n,d in [(4,1),(5,2),(5,3),(6,3)]:
        Fs=[frozenset(f) for f in combinations(range(n),d+1)]
        count=0; steps=0
        for bits in range(1,1<<len(Fs)):
            C=complex_from_facets([Fs[j] for j in range(len(Fs)) if bits>>j&1])
            for k in range(1,d+1):
                if kd(C,k):
                    steps+=check(C,k,n)
                    count+=1
        results.append(dict(n=n,d=d,complex_parameter_pairs=count,checked_additions=steps))
        print(results[-1],flush=True)
    print(json.dumps(results))
