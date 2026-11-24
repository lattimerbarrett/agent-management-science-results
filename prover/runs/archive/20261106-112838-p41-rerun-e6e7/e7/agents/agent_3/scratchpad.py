from pathlib import Path
code=r'''"""Checked lower seed and explicit edge-decomposition certificate audit.
No recognition heuristic: checks every step in a prescribed decomposition.
"""
from itertools import combinations
from collections import Counter
import json
from pathlib import Path

def simplex_skeleton(W,q):
    return {frozenset(c) for c in combinations(sorted(W),q)}

def audit_seed():
    data=json.loads((Path(__file__).parent/'lower_seed_agent3.json').read_text())
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

if __name__=='__main__':
    audit_seed()
    for d in (3,4,5):audit_decomposition(d)
    for d in range(3,11):audit_obstruction(d)
'''
Path('workspace/lower_verified_agent3.py').write_text(code)
import sys
sys.path.insert(0,'workspace')
from lower_verified_agent3 import *
audit_seed()
for d in (3,4,5):audit_decomposition(d)
for d in range(3,11):audit_obstruction(d)
