"""Exact finite k-decomposability and completion certificate checker.
Faces/facets are integer bitmasks; empty simplex has sole facet 0.
"""
from functools import lru_cache
from itertools import combinations

def subsets(mask, size=None):
    bits=[1<<i for i in range(mask.bit_length()) if mask>>i&1]
    sizes=range(len(bits)+1) if size is None else [size]
    for s in sizes:
        for c in combinations(bits,s):
            yield sum(c)

def maximal(faces):
    fs=set(faces)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

def deletion_link(facets,sigma):
    deletion=[]; link=[]
    for f in facets:
        if f&sigma==sigma:
            link.append(f^sigma)
            deletion.extend(f^b for b in subsets(sigma,1))
        else:
            deletion.append(f)
    return maximal(deletion),maximal(link)

@lru_cache(None)
def certificate(facets,k):
    facets=tuple(sorted(facets))
    if not facets: return None
    rank=facets[0].bit_count()
    if any(f.bit_count()!=rank for f in facets): return None
    if len(facets)==1: return ('simplex',facets[0])
    faces=set(s for f in facets for n in range(1,min(k+1,rank)+1) for s in subsets(f,n))
    for s in sorted(faces,key=lambda s:(s.bit_count(),s)):
        de,li=deletion_link(facets,s)
        if any(f.bit_count()!=rank for f in de): continue
        dc=certificate(de,k)
        if dc is None: continue
        lc=certificate(li,k)
        if lc is not None: return ('shed',s,dc,lc)
    return None

def verify(facets,k,cert):
    facets=tuple(sorted(facets))
    assert facets and len({f.bit_count() for f in facets})==1
    if cert[0]=='simplex':
        assert facets==(cert[1],)
        return True
    assert cert[0]=='shed'
    s=cert[1]
    assert 1<=s.bit_count()<=k+1 and any(f&s==s for f in facets)
    de,li=deletion_link(facets,s)
    assert len({f.bit_count() for f in de})==1
    assert de[0].bit_count()==facets[0].bit_count()
    verify(de,k,cert[2]);verify(li,k,cert[3])
    return True

def completion(facets,k,vertices=None):
    facets=tuple(sorted(facets))
    if vertices is None:
        vertices=0
        for f in facets: vertices|=f
    rank=facets[0].bit_count()
    allfacets=tuple(subsets(vertices,rank))
    @lru_cache(None)
    def search(fs):
        cert=certificate(fs,k)
        if cert is None: return None
        if len(fs)==len(allfacets): return ()
        for f in allfacets:
            if f in fs:continue
            nxt=tuple(sorted(fs+(f,)))
            tail=search(nxt)
            if tail is not None:return (f,)+tail
        return None
    return search(facets)
