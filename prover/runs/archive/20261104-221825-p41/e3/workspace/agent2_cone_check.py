from itertools import combinations
from functools import lru_cache

def canonical(fs):
    fs=set(map(frozenset,fs))
    return tuple(sorted((tuple(sorted(f)) for f in fs if not any(f<g for g in fs)),key=lambda x:(len(x),x)))
def faces(F):
    return {frozenset(s) for f in F for r in range(len(f)+1) for s in combinations(f,r)}
@lru_cache(None)
def kd(F,k):
    if len(F)==1:return True
    if len({len(f) for f in F})!=1:return False
    S=faces(F); size=len(F[0])
    for sig in sorted(S,key=lambda x:(len(x),sorted(x))):
        if not sig or len(sig)>k+1:continue
        de=canonical(s for s in S if not sig<=s)
        if not de or any(len(f)!=size for f in de):continue
        li=canonical(s-sig for s in S if sig<=s)
        if kd(de,k) and kd(li,k):return True
    return False

def universal_cone(d,n,B):
    return canonical([(-1,)+s for s in combinations(range(n),d)]+list(B))

# Exhaustively check arbitrary-family cone lemma on small cases.
checks=0
for d,n in [(1,4),(2,4),(2,5),(3,5)]:
    old=list(combinations(range(n),d+1))
    for bits in range(1<<len(old)):
        B=[f for j,f in enumerate(old) if bits>>j&1]
        assert kd(universal_cone(d,n,B),0),(d,n,B)
        checks+=1
print('Universal-cone arbitrary-family lemma: checked',checks,'families as vertex decomposable')
old=list(combinations(range(6),4)); found=0
for bits in range(1,1<<len(old)):
    F=canonical(f for j,f in enumerate(old) if bits>>j&1)
    if not kd(F,3):continue
    G=canonical(s for f in F for s in combinations(f,3))
    if not kd(G,0):
        print('Non-VD skeleton',F,G);found+=1;break
print('nonVD found',found)
import pathlib
pathlib.Path('workspace/agent2_cone_check.py').write_text(pathlib.Path('scratchpad.py').read_text())
