from itertools import combinations
from functools import lru_cache

def submasks(x):
    y=x
    while True:
        yield y
        if y==0: break
        y=(y-1)&x

def maximal(faces):
    faces=set(faces)
    return tuple(sorted(x for x in faces if not any(x!=y and x&y==x for y in faces)))

def all_faces(facets):
    return frozenset(y for f in facets for y in submasks(f))

@lru_cache(None)
def k_certificate(facets,k):
    facets=tuple(facets)
    if len(facets)==1: return ('simplex',facets[0])
    if not facets: return None
    size=facets[0].bit_count()
    if any(f.bit_count()!=size for f in facets): return None
    faces=all_faces(facets)
    for s in sorted(faces,key=lambda x:(x.bit_count(),x)):
        if not s or s.bit_count()>k+1: continue
        deletion=maximal(f for f in faces if f&s!=s)
        if not deletion or any(f.bit_count()!=size for f in deletion): continue
        link=maximal(f^s for f in facets if f&s==s)
        dc=k_certificate(deletion,k)
        if dc is None: continue
        lc=k_certificate(link,k)
        if lc is not None: return ('shed',s,dc,lc)
    return None

@lru_cache(None)
def shelling(facets):
    facets=tuple(facets)
    if len(facets)==1: return facets
    if not facets: return None
    size=facets[0].bit_count()
    for f in facets:
        rest=tuple(g for g in facets if g!=f)
        intersection=maximal(f&g for g in rest)
        if any(g.bit_count()!=size-1 for g in intersection): continue
        sh=shelling(rest)
        if sh is not None: return sh+(f,)
    return None

def appendable(facets,f):
    size=f.bit_count()
    intersection=maximal(f&g for g in facets)
    return all(g.bit_count()==size-1 for g in intersection)
