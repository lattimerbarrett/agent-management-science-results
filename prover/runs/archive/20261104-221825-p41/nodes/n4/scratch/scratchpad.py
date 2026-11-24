from functools import lru_cache
from itertools import combinations

def subs(f):
    s=tuple(f)
    return [frozenset(c) for r in range(len(s)+1) for c in combinations(s,r)]

def canon(fs):
    fs=set(fs)
    return frozenset(f for f in fs if not any(f<g for g in fs))

@lru_cache(None)
def kd(fs,k):
    if len(fs)==1:return True
    sizes={len(f) for f in fs}
    if len(sizes)!=1:return False
    n=next(iter(sizes))
    faces=set().union(*(set(subs(f)) for f in fs))
    for s in faces:
        if not s or len(s)>k+1:continue
        deletion=canon(g for g in faces if not s<=g)
        if any(len(g)!=n for g in deletion):continue
        link=canon(g-s for g in fs if s<=g)
        if kd(deletion,k) and kd(link,k):return True
    return False

@lru_cache(None)
def shell(fs):
    if len(fs)==1:return True
    d=len(next(iter(fs)))-1
    for f in fs:
        rest=fs-{f}
        inter=canon(f&g for g in rest)
        if all(len(h)==d for h in inter) and shell(rest):return True
    return False

for n,d in [(4,1),(5,2),(5,3),(6,2)]:
    allf=[frozenset(c) for c in combinations(range(n),d+1)]
    diffs=[]
    for mask in range(1,1<<len(allf)):
        fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
        a,b=kd(fs,d),shell(fs)
        if b and len(fs)>1:
            for f in fs:
                rest=fs-{f}
                inter=canon(f&g for g in rest)
                if all(len(h)==d for h in inter) and shell(rest):
                    # The restriction face consists of vertices opposite
                    # those boundary ridges that occur in the preceding complex.
                    sigma=frozenset(v for v in f if f-{v} in inter)
                    faces=set().union(*(set(subs(g)) for g in fs))
                    deletion=canon(g for g in faces if not sigma<=g)
                    link=canon(g-sigma for g in fs if sigma<=g)
                    assert sigma and deletion==rest and link==frozenset([f-sigma]), (fs,f,sigma,deletion,rest)
                    break
        if a!=b:
            diffs.append((fs,a,b));break
    print(n,d,'differences',diffs,'cases',2**len(allf)-1,flush=True)
