from itertools import combinations
from functools import lru_cache

def subfaces(f):
    f=tuple(f)
    return frozenset(frozenset(t) for r in range(len(f)+1) for t in combinations(f,r))

def complex_from_facets(facets):
    return frozenset().union(*(subfaces(f) for f in facets))

def facets(C):
    return frozenset(f for f in C if not any(f<g for g in C))

@lru_cache(None)
def kd(C,k):
    fs=facets(C)
    if len(fs)==1: return True
    sizes={len(f) for f in fs}
    if len(sizes)!=1:return False
    size=next(iter(sizes))
    for s in C:
        if not s or len(s)>k+1: continue
        deletion=frozenset(g for g in C if not s<=g)
        if not deletion or any(len(f)!=size for f in facets(deletion)):continue
        link=frozenset(g-s for g in C if s<=g)
        if kd(deletion,k) and kd(link,k):return True
    return False

@lru_cache(None)
def shellable(fs):
    if len(fs)<=1:return True
    sizes={len(f) for f in fs}
    if len(sizes)!=1:return False
    size=next(iter(sizes))
    for f in fs:
        rest=fs-{f}
        C=complex_from_facets(rest)
        intersection=C & subfaces(f)
        if intersection and all(len(g)==size-1 for g in facets(intersection)) and shellable(rest):
            return True
    return False
