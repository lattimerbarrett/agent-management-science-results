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

for n,d in [(5,2),(6,3)]:
    allf=[frozenset(c) for c in combinations(range(n),d+1)]
    checked=0
    discrepancies=[]
    for mask in range(1,1<<len(allf)):
        fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
        if len(fs)==1 or not shell(fs):continue
        for f in fs:
            rest=fs-{f}
            if not shell(rest):continue
            checked+=1
            intersection=canon(f&g for g in rest)
            bad=[g for g in intersection if len(g)!=d]
            if bad:
                g=bad[0]
                oldlink=canon(h-g for h in rest if g<=h)
                newlink=f-g
                oldvertices=set().union(*oldlink)
                discrepancies.append((fs,f,g,oldlink,newlink,oldvertices&newlink))
                break
        if discrepancies:break
    print('n,d=',n,d,'shellable pairs checked=',checked,'discrepancies=',discrepancies,flush=True)
