"""Exhaustively check shelling-prefix completion in small simplex skeleta.
A state is a set of facets. Each arrow adds one facet using the exact
pure-codimension-one intersection criterion for shelling.
"""
from itertools import combinations
from functools import lru_cache
import json, time

def check(d,n):
    facets = [sum(1 << v for v in f) for f in combinations(range(n),d+1)]
    m=len(facets); full=(1<<m)-1
    @lru_cache(None)
    def intersection_type(s,j):
        # Return maximal faces of (union of old simplices) intersect simplex j.
        f=facets[j]
        intersections={f & facets[i] for i in range(m) if (s>>i)&1}
        return tuple(g for g in intersections
                     if not any(g != h and (g & h)==g for h in intersections))
    def appends(s,j):
        if s==0: return True
        maximal=intersection_type(s,j)
        return bool(maximal) and all(g.bit_count()==d for g in maximal)
    shellable=bytearray(1<<m); shellable[0]=1
    predecessor={}
    edges=0
    for s in range(1<<m):
        if not shellable[s]: continue
        missing=full^s
        while missing:
            b=missing&-missing; missing-=b; j=b.bit_length()-1
            if appends(s,j):
                edges+=1
                t=s|b
                if not shellable[t]: predecessor[t]=(s,j)
                shellable[t]=1
    extends=bytearray(1<<m); extends[full]=1
    successor={}
    for s in range(full-1,-1,-1):
        if not shellable[s]: continue
        missing=full^s
        while missing:
            b=missing&-missing; missing-=b; j=b.bit_length()-1
            if extends[s|b] and appends(s,j):
                extends[s]=1; successor[s]=j; break
    bad=[s for s in range(1<<m) if shellable[s] and not extends[s]]
    assert not bad, (d,n,bad[:3])
    # Recover a shelling of every state and a completion preserving it.
    # Then check every step again from the actual ordered list, and verify
    # that every newly visited intermediate state is shellable.
    verified_orderings=0
    for s in range(1,1<<m):
        if not shellable[s]: continue
        prefix=[]; t=s
        while t:
            t,j=predecessor[t]; prefix.append(j)
        prefix.reverse()
        order=prefix[:]; t=s
        while t!=full:
            j=successor[t]; order.append(j); t|=1<<j
        assert len(order)==m and len(set(order))==m
        t=0
        for j in order:
            assert appends(t,j)
            t|=1<<j
            assert shellable[t]
        assert sum(1<<j for j in prefix)==s
        verified_orderings+=1
    return dict(d=d,n=n,facets=m,pure_nonempty_complexes=full,
                shellable_nonempty=sum(shellable)-1,
                shelling_prefix_edges=edges,
                completed_and_rechecked_orderings=verified_orderings)

if __name__=='__main__':
    # Publish this independently executable checker alongside its results.
    from pathlib import Path
    Path('workspace/agent2_shelling_completion.py').write_text(Path(__file__).read_text())
    results=[]
    for d,n in [(1,5),(2,5),(3,5),(3,6),(4,6)]:
        t=time.time(); result=check(d,n); result['seconds']=round(time.time()-t,3)
        results.append(result); print(json.dumps(result),flush=True)
    with open('workspace/agent2_shelling_completion_results.json','w') as f:
        json.dump(results,f,indent=2)
