from itertools import combinations
from functools import lru_cache
from pathlib import Path

# Faces encoded as integer masks; a pure complex by its facet masks.
def bits(x):
    while x:
        b=x&-x; yield b; x-=b

def subfaces(x):
    s=x
    while True:
        yield s
        if s==0: break
        s=(s-1)&x

def maximal(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

@lru_cache(None)
def kd_order(fs,k):
    if len(fs)==1: return fs
    size=fs[0].bit_count()
    if any(f.bit_count()!=size for f in fs): return None
    faces=set().union(*(set(subfaces(f)) for f in fs))
    for s in sorted(faces):
        if not s or s.bit_count()>k+1: continue
        dfs=maximal(g for g in faces if g&s!=s)
        if not dfs or any(g.bit_count()!=size for g in dfs): continue
        lfs=maximal(f^s for f in fs if f&s==s)
        do=kd_order(dfs,k)
        if do is None: continue
        lo=kd_order(lfs,k)
        if lo is not None: return do+tuple(s|g for g in lo)
    return None

def skel(fs,size):
    return maximal(s for f in fs for s in subfaces(f) if s.bit_count()<=size)

def check():
    n=5; k=1; count=0; skeletons=0; cone_steps=0
    facets=[sum(1<<v for v in c) for c in combinations(range(n),3)]
    for state in range(1,1<<len(facets)):
        fs=tuple(sorted(f for i,f in enumerate(facets) if state>>i&1))
        order=kd_order(fs,k)
        if order is None: continue
        count+=1
        for i in range(1,len(order)+1):
            assert kd_order(tuple(sorted(order[:i])),k) is not None
        for size in range(1,4):
            assert kd_order(skel(fs,size),k) is not None
            skeletons+=1
        link=skel(fs,2)
        link_order=kd_order(link,k)
        new=1<<n
        current=set(fs)
        for f in link_order:
            current.add(new|f)
            assert kd_order(tuple(sorted(current)),k) is not None
            cone_steps+=1
    return dict(pure_2_complexes_tested=(1<<len(facets))-1,k_decomposable=count,skeleton_checks=skeletons,cone_addition_checks=cone_steps)
def relative_cone_check():
    n=5;k=0;count=0
    facets=[sum(1<<v for v in c) for c in combinations(range(n),3)]
    edges=[sum(1<<v for v in c) for c in combinations(range(n),2)]
    for state in range(1,1<<len(facets)):
        fs=tuple(sorted(f for i,f in enumerate(facets) if state>>i&1))
        if kd_order(fs,k) is None: continue
        base=set(skel(fs,2));missing=[e for e in edges if e not in base]
        for extra in range(1<<len(missing)):
            ls=tuple(sorted(base|{e for i,e in enumerate(missing) if extra>>i&1}))
            if kd_order(ls,k) is None: continue
            gamma=tuple(sorted(set(fs)|{(1<<n)|e for e in ls}))
            if kd_order(gamma,k) is None: return 'COUNTEREXAMPLE',fs,ls
            count+=1
    return count
if __name__=='__main__':
    Path('workspace/agent2_structural_checks.py').write_text(Path(__file__).read_text())
    print(check())
    print('relative cone',relative_cone_check())
