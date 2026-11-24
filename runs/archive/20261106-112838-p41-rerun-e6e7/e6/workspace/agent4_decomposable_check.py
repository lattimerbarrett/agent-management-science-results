from functools import lru_cache
from itertools import combinations

def subs(s):
    x=s
    while True:
        yield x
        if not x: break
        x=(x-1)&s

def faces(facets):
    return frozenset(g for f in facets for g in subs(f))

def maximal(fs):
    return tuple(sorted(g for g in fs if not any(g != h and g & h == g for h in fs)))

def pure(facets):
    return bool(facets) and len({f.bit_count() for f in facets}) == 1

@lru_cache(None)
def kd(facets,k):
    if len(facets)==1: return True
    fs=faces(facets)
    dim=facets[0].bit_count()-1
    for s in fs:
        if not s or s.bit_count()>k+1: continue
        dele=maximal(frozenset(g for g in fs if g&s!=s))
        if not pure(dele) or dele[0].bit_count()!=dim+1: continue
        link=maximal(frozenset(g^s for g in fs if g&s==s))
        if kd(dele,k) and kd(link,k): return True
    return False

@lru_cache(None)
def shell(facets):
    if len(facets)==1:return True
    d=facets[0].bit_count()-1
    for f in facets:
        rest=tuple(g for g in facets if g!=f)
        inter=maximal(faces(rest)&frozenset(subs(f)))
        if pure(inter) and inter[0].bit_count()==d and shell(rest):return True
    return False

if __name__=='__main__':
    from pathlib import Path
    Path('workspace/agent4_decomposable_check.py').write_text(Path(__file__).read_text())
    for n,d in [(5,2),(5,3)]:
        allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
        N=0;S=0
        for a in range(1,1<<len(allf)):
            fac=tuple(sorted(allf[j] for j in range(len(allf)) if a>>j&1))
            ss=shell(fac); kk=kd(fac,d)
            assert ss==kk,(n,d,fac,ss,kk)
            N+=1;S+=ss
        print('n=',n,'d=',d,'families=',N,'shellable= d-decomposable=',S)
