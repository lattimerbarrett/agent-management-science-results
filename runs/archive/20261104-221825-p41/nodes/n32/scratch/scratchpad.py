from itertools import combinations
from functools import lru_cache

def faces_of(facets):
    return frozenset(frozenset(s) for f in facets for r in range(len(f)+1) for s in combinations(f,r))
def facets_of(faces):
    return frozenset(f for f in faces if not any(f<g for g in faces))
@lru_cache(None)
def literal_kdec(C,k):
    facets=facets_of(C)
    if len(facets)==1:return True
    sizes={len(f) for f in facets}
    if len(sizes)!=1:return False
    rank=next(iter(sizes))
    for sigma in C:
        if not sigma or len(sigma)>k+1:continue
        D=frozenset(G for G in C if not sigma<=G)
        L=frozenset(G for G in C if not G&sigma and G|sigma in C)
        if all(len(f)==rank for f in facets_of(D)) and literal_kdec(D,k) and literal_kdec(L,k):
            return True
    return False
@lru_cache(None)
def shell_order(facets):
    if len(facets)==1:return tuple(facets)
    d=len(next(iter(facets)))-1
    for F in facets:
        old=facets-{F}
        intersection=faces_of(old)&faces_of([F])
        if all(len(G)==d for G in facets_of(intersection)):
            order=shell_order(old)
            if order is not None:return order+(F,)
    return None

def audit_shell_certificate(order,k):
    if len(order)==1:return
    F=order[-1];C=faces_of(order);D=faces_of(order[:-1])
    R=frozenset(v for v in F if F-{v} in D)
    assert R and len(R)<=k+1
    literalD=frozenset(G for G in C if not R<=G)
    literalL=frozenset(G for G in C if not G&R and G|R in C)
    assert literalD==D, (order,R,'deletion')
    assert literalL==faces_of([F-R]),(order,R,'link')
    assert all(len(G)==len(F) for G in facets_of(literalD))
    audit_shell_certificate(order[:-1],k)

for n,d in [(5,2),(6,3)]:
    allF=[frozenset(f) for f in combinations(range(n),d+1)]
    shell_count=0
    for mask in range(1,2**len(allF)):
        fs=frozenset(f for i,f in enumerate(allF) if mask>>i&1)
        order=shell_order(fs)
        kd=literal_kdec(faces_of(fs),d)
        assert kd==(order is not None),(fs,kd,order)
        if order is not None:
            audit_shell_certificate(order,d);shell_count+=1
    print('Literal face-family audit:',n,d,'families',2**len(allF)-1,'shellable',shell_count,'no discrepancies',flush=True)
    literal_kdec.cache_clear();shell_order.cache_clear()
import os
print('Workspace directories:',os.listdir('experiments') if os.path.isdir('experiments') else 'unavailable')
