"""Self-contained exact certificate checks for b(d,k)=d-2. Python 3, standard library only."""
from itertools import combinations
from functools import lru_cache
import os,pickle

def allfaces(F):
    return {frozenset(c) for i in range(len(F)+1) for c in combinations(F,i)}

def facets_normalize(facets):
    fs=set(map(frozenset,facets))
    return frozenset(f for f in fs if not any(f<g for g in fs))

@lru_cache(None)
def kdecomp(fs,k):
    fs=facets_normalize(fs)
    if len(fs)==1:return True
    sizes={len(f) for f in fs}
    if len(sizes)!=1:return False
    q=next(iter(sizes))
    faces=set().union(*(allfaces(f) for f in fs))
    for sig in sorted((s for s in faces if 0<len(s)<=k+1),key=lambda s:(len(s),sorted(s))):
        dele=facets_normalize(s for s in faces if not sig<=s)
        if any(len(f)!=q for f in dele):continue
        link=facets_normalize(f-sig for f in fs if sig<=f)
        if kdecomp(dele,k) and kdecomp(link,k):return True
    return False

"""Explicit upper-bound completion and independent recursive recognition.
Run tests via test_upper(). Facets are frozensets; labels sortable integers.
"""
from itertools import combinations
from functools import lru_cache


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


SEED={'n': 10, 'triangles': [[0, 5, 8], [1, 3, 7], [1, 2, 5], [1, 2, 9], [2, 8, 9], [1, 6, 9], [0, 1, 8], [0, 3, 8], [3, 7, 9], [5, 7, 8], [0, 2, 9], [0, 2, 3], [0, 1, 6], [2, 3, 4], [4, 5, 8], [1, 3, 6], [0, 1, 4], [5, 6, 7], [4, 5, 9], [1, 5, 7], [3, 4, 6], [0, 2, 6], [2, 6, 8], [2, 6, 7], [1, 2, 3], [3, 4, 9], [4, 6, 8], [0, 5, 6], [5, 7, 9], [1, 4, 9], [0, 7, 9], [1, 4, 7], [2, 4, 7], [3, 7, 8], [2, 5, 8], [3, 5, 6]], 'collapse': [[[0, 4], [0, 1, 4]], [[0, 7], [0, 7, 9]], [[0, 9], [0, 2, 9]], [[1, 8], [0, 1, 8]], [[0, 1], [0, 1, 6]], [[3, 5], [3, 5, 6]], [[6, 9], [1, 6, 9]], [[1, 6], [1, 3, 6]], [[3, 6], [3, 4, 6]], [[4, 6], [4, 6, 8]], [[4, 8], [4, 5, 8]], [[4, 5], [4, 5, 9]], [[5, 9], [5, 7, 9]], [[6, 8], [2, 6, 8]], [[7, 9], [3, 7, 9]], [[3, 9], [3, 4, 9]], [[3, 4], [2, 3, 4]], [[2, 4], [2, 4, 7]], [[2, 7], [2, 6, 7]], [[2, 6], [0, 2, 6]], [[0, 2], [0, 2, 3]], [[0, 3], [0, 3, 8]], [[0, 6], [0, 5, 6]], [[0, 5], [0, 5, 8]], [[2, 3], [1, 2, 3]], [[1, 3], [1, 3, 7]], [[3, 7], [3, 7, 8]], [[4, 7], [1, 4, 7]], [[1, 4], [1, 4, 9]], [[1, 7], [1, 5, 7]], [[1, 5], [1, 2, 5]], [[1, 2], [1, 2, 9]], [[2, 5], [2, 5, 8]], [[2, 8], [2, 8, 9]], [[5, 6], [5, 6, 7]], [[5, 7], [5, 7, 8]]], 'tree': [[7, 8], [4, 9], [2, 9], [5, 8], [6, 7], [3, 8], [0, 8], [1, 9], [8, 9]]}
"""Checked lower seed and explicit edge-decomposition certificate audit.
No recognition heuristic: checks every step in a prescribed decomposition.
"""
from itertools import combinations
from collections import Counter
import json
from pathlib import Path

def simplex_skeleton(W,q):
    return {frozenset(c) for c in combinations(sorted(W),q)}

def audit_seed():
    data=SEED
    n=data['n'];tris=set(map(frozenset,data['triangles']))
    edges=set(map(frozenset,combinations(range(n),2)))
    assert len(tris)==36
    assert all(sum(t<=frozenset(q) for t in tris)<=2 for q in combinations(range(n),4))
    for ee,tt in data['collapse']:
        e,t=map(frozenset,(ee,tt))
        assert t in tris and e in edges and e<t
        assert sum(e<=s for s in tris)==1
        tris.remove(t);edges.remove(e)
    assert not tris and edges==set(map(frozenset,data['tree']))
    reached={0}
    while True:
        nxt=reached|{v for e in edges if e&reached for v in e}
        if nxt==reached:break
        reached=nxt
    assert len(reached)==n and len(edges)==n-1
    return data

def audit_decomposition(d=3):
    """Every facet/ridge in the prescribed construction is checked explicitly.
    Link simplex-core property certifies VD by the elementary core lemma.
    """
    data=audit_seed();n=data['n'];q=d+1
    blocks=[frozenset(range(v*d,(v+1)*d)) for v in range(n)]
    tree=set(map(frozenset,data['tree']))
    first=min(tree,key=lambda e:tuple(sorted(e)))
    present=simplex_skeleton(set().union(*(blocks[v] for v in first)),q)
    ridges=Counter(h for f in present for h in map(frozenset,combinations(f,d)))
    V=set().union(*(blocks[v] for v in first));reached=set(first)
    vertex_steps=edge_steps=0
    def add_facets(new):
        nonlocal present,ridges
        assert not (new&present)
        for f in new:
            assert len(f)==q
            for h in map(frozenset,combinations(f,d)):ridges[h]+=1
        present|=new
    # Expanded tree is vertex-decomposable, witnessed by clone additions.
    while len(reached)<n:
        choices=[(next(iter(e&reached)),next(iter(e-reached))) for e in tree if len(e&reached)==1]
        u,v=min(choices);old=frozenset()
        for x in sorted(blocks[v]):
            link_vertices=blocks[u]|old
            new={h|{x} for h in simplex_skeleton(link_vertices,d)}
            assert all((f-{x}) in ridges for f in new)
            assert {f-{x} for f in new}==simplex_skeleton(link_vertices,d)
            add_facets(new);V.add(x);old=old|{x};vertex_steps+=1
        reached.add(v)
    # Reverse elementary free-edge collapses.
    for ee,tt in reversed(data['collapse']):
        a,b=ee;c=next(iter(set(tt)-set(ee)))
        A,B,C=blocks[a],blocks[b],blocks[c]
        allowed=set()
        region=simplex_skeleton(A|B|C,q)
        for x in sorted(A):
            for y in sorted(B):
                e=frozenset((x,y));allowed.add(e)
                new={f for f in region if e<=f and all(frozenset((aa,bb)) in allowed for aa in f&A for bb in f&B)}
                assert new and not(new&present)
                # Deletion of e is EXACTLY previous complex, including all faces.
                assert all((f-{x}) in ridges and (f-{y}) in ridges for f in new)
                link={f-e for f in new}
                assert all(len(h)==d-1 for h in link)
                # Independently check the simplex-C join/truncation description.
                outside={h-C for h in link}
                expected=set()
                for h in outside:
                    for z in combinations(sorted(C),d-1-len(h)):
                        expected.add(h|frozenset(z))
                assert expected==link
                add_facets(new);edge_steps+=1
    # Independently generate initial blowup complex from its 36 triangles.
    expected=set()
    for tri in data['triangles']:
        expected|=simplex_skeleton(set().union(*(blocks[v] for v in tri)),q)
    assert present==expected
    assert set().union(*present)==set(range(n*d))
    print('d=',d,':',len(present),'facets;',vertex_steps,'vertex and',edge_steps,'edge decomposition steps audited')
    return present

def audit_obstruction(d):
    """Exhaust all possible relevant OLD block-count patterns, not just samples."""
    data=audit_seed();tris=set(map(frozenset,data['triangles']));n=data['n']
    checked=0
    # Old support >=5 admits no old-supported ridge; support <=2 is allowed.
    for s in (3,4):
        for ss in combinations(range(n),s):
            S=frozenset(ss)
            if s==3 and S in tris:continue
            def compositions(total,length,prefix=()):
                if length==0:
                    if total==0:yield prefix
                    return
                for c in range(1,min(d,total-length+1)+1):
                    yield from compositions(total-c,length-1,prefix+(c,))
            for old_size in range(4,d+2):
                for counts in compositions(old_size,s):
                    R={v for v,c in zip(ss,counts) if c==1 and (len(S-{v})<=2 or S-{v} in tris)}
                    assert len(R)<=2
                    checked+=1
    print('d=',d,':',checked,'forbidden-support count patterns checked (covers every r<=d-3)')


if __name__=="__main__":
    test_upper()
    for d in (3,4,5): audit_decomposition(d)
    for d in range(3,11): audit_obstruction(d)
