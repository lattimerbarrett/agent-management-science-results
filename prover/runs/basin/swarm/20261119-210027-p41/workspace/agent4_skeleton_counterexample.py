from functools import lru_cache
from itertools import combinations
import time
L=[(0,1,2),(1,2,6),(0,2,7),(2,4,6),(2,4,5),(1,4,6),(2,3,4),(2,3,7),(0,2,4),(0,1,7),(3,4,5),(1,2,5),(1,3,5),(0,3,7),(3,4,6),(2,3,6),(1,5,7),(3,5,6)]
# Verify listed order is a shelling directly.
old=set()
for i,F in enumerate(L):
    boundary={frozenset(c) for s in range(3) for c in combinations(F,s)}
    intersection=boundary & old
    if i:
        maximal=[T for T in intersection if not any(T<U for U in intersection)]
        assert maximal and all(len(T)==2 for T in maximal)
    old.update(frozenset(c) for s in range(4) for c in combinations(F,s))

n=16
@lru_cache(None)
def vd(fs):
    if len(fs)==1:return True
    for v in range(n):
        yes=tuple(f for f in fs if f>>v&1)
        no=tuple(f for f in fs if not f>>v&1)
        if not yes or not no:continue
        if any(not any((f^(1<<v))&g==(f^(1<<v)) for g in no) for f in yes):continue
        if vd(no) and vd(tuple(sorted(f^(1<<v) for f in yes))):return True
    return False

G=tuple(sorted(sum(1<<v for v in f) for f in L))
assert not vd(G)
R=[tuple(v+8 for v in f) for f in L]
join=tuple(sum(1<<v for v in f+g) for f in L for g in R)
sk=tuple(sorted(set(f^(1<<v) for f in join for v in range(n) if f>>v&1)))
t=time.time();result=vd(sk)
print('Gamma is shellable, nonVD; |facets(skel_4(Gamma*Gamma))|=',len(sk))
print('VD=',result,'cache=',vd.cache_info(),'seconds=',time.time()-t)
assert not result
