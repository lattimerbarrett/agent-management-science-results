"""Explicit upper-bound completion and independent recursive recognition.
Run tests via test_upper(). Facets are frozensets; labels sortable integers.
"""
from itertools import combinations
from functools import lru_cache
from kdecomp_agent4 import kdecomp, facets_normalize, allfaces

@lru_cache(None)
def decomposition(fs,k):
    fs=facets_normalize(fs)
    if len(fs)==1:return None
    q=len(next(iter(fs)))
    faces=set().union(*(allfaces(f) for f in fs))
    for sig in sorted((s for s in faces if 0<len(s)<=k+1),key=lambda s:(len(s),sorted(s))):
        dele=facets_normalize(s for s in faces if not sig<=s)
        if any(len(f)!=q for f in dele):continue
        link=facets_normalize(f-sig for f in fs if sig<=f)
        if kdecomp(dele,k) and kdecomp(link,k):return sig,dele,link
    raise ValueError('not k-decomposable')

def prefix_order(fs,k):
    """Facet ordering whose every prefix is k-decomposable."""
    fs=facets_normalize(fs)
    dec=decomposition(fs,k)
    if dec is None:return list(fs)
    sig,dele,link=dec
    return prefix_order(dele,k)+[sig|f for f in prefix_order(link,k)]

def upper_order(fs,k,extra):
    """d>=2, extra has exactly d-2 fresh vertices."""
    fs=facets_normalize(fs)
    d=len(next(iter(fs)))-1
    V=set().union(*fs)
    assert len(extra)==d-2 and not V.intersection(extra)
    present=set(fs); order=[]
    def add(f):
        f=frozenset(f)
        if f not in present:present.add(f);order.append(f)
    if d==2:
        a=min(V)
        edges={frozenset(e) for f in fs for e in combinations(f,2)}
        reached={a}|{v for v in V if frozenset((a,v)) in edges}
        while reached!=V:
            found=False
            for e in sorted(edges,key=lambda e:tuple(sorted(e))):
                uvs=tuple(e)
                if len(e&reached)==1:
                    u=next(iter(e&reached)); v=next(iter(e-reached))
                    add((a,u,v));edges.add(frozenset((a,v)));reached.add(v)
                    found=True;break
            assert found,'disconnected 1-skeleton'
        for u,v in combinations(sorted(V-{a}),2):add((a,u,v))
    else:
        a=extra[0]
        skel=facets_normalize(frozenset(h) for f in fs for h in combinations(f,d))
        for h in prefix_order(skel,k):add(h|{a})
        for h in upper_order(skel,k,extra[1:]):add(h|{a})
    for f in combinations(sorted(V|set(extra)),d+1):add(f)
    return order

def verify_order(fs,k,order,extra):
    fs=facets_normalize(fs)
    V=set().union(*fs)|set(extra)
    d=len(next(iter(fs)))-1
    assert kdecomp(fs,k)
    for f in order:
        assert f not in fs and len(f)==d+1
        fs=fs|{f}
        assert kdecomp(fs,k),(k,fs,f)
    assert fs==frozenset(map(frozenset,combinations(V,d+1)))

def test_upper():
    from random import Random
    rng=Random(20260401)
    checked=0;steps=0
    allf=list(map(frozenset,combinations(range(5),3)))
    for mask in range(1,1<<len(allf)):
        fs=frozenset(f for j,f in enumerate(allf) if mask>>j&1)
        for k in (1,2):
            if kdecomp(fs,k):
                order=upper_order(fs,k,[]);verify_order(fs,k,order,[])
                checked+=1;steps+=len(order)
    print('Exhaustive dimension2 n<=5:',checked,'k-decomp inputs;',steps,'verified intermediate additions')
    for d,n,trials in [(3,6,40),(4,6,12)]:
        allf=list(map(frozenset,combinations(range(n),d+1)))
        count=0;st=0
        for t in range(trials):
            fs=frozenset(rng.sample(allf,rng.randrange(1,len(allf)+1)))
            if not kdecomp(fs,1):continue
            extra=list(range(n,n+d-2))
            order=upper_order(fs,1,extra)
            verify_order(fs,1,order,extra)
            count+=1;st+=len(order)
        print('Dimension',d,':',count,'random inputs;',st,'verified additions')
if __name__=='__main__':test_upper()
