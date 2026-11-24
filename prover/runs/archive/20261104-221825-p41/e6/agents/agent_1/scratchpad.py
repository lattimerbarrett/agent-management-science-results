from pathlib import Path
code='''from itertools import combinations, product
from collections import Counter
from math import comb

ORDER = "135 013 157 358 368 348 134 258 257 036 268 267 167 017 168 027 018 048 024 367 023 147 246 245 124 058 056 478".split()
K = [frozenset(map(int,s)) for s in ORDER]

def subs(S,r):
    return map(frozenset,combinations(S,r))

def verify():
    seen={frozenset()}; restrictions=[]
    for j,F in enumerate(K):
        assert F not in seen
        new=[s for r in (1,2,3) for s in subs(F,r) if s not in seen]
        minimal=[s for s in new if not any(t<s for t in new)]
        if j:
            assert len(minimal)==1 and len(minimal[0])<=2
            restrictions.append(minimal[0])
        else: restrictions.append(F)
        for r in range(4):seen.update(subs(F,r))
    assert sum(len(s)==2 for s in seen)==36
    histogram=Counter(sum(t in seen for t in subs(Q,3))
                      for Q in combinations(range(9),4))
    assert histogram=={0:27,1:30,2:69}

    # Four clones per old vertex, pure rank-four expansion.
    facets={S for F in K for S in subs([4*v+i for v in F for i in range(4)],4)}
    initial=set(facets)
    triangles={t for F in initial for t in subs(F,3)}
    edges={e for F in initial for e in subs(F,2)}
    assert len(edges)==630
    blocked=0
    for Q in combinations(range(36),4):
        if frozenset(Q) not in initial:
            assert sum(t in triangles for t in subs(Q,3))<=2
            blocked+=1

    ridges=Counter(t for F in facets for t in subs(F,3))
    steps=0
    for F,R in reversed(list(zip(K,restrictions))[1:]):
        blocks=[range(4*v,4*v+4) for v in sorted(R)]
        for tup in product(*blocks):
            sigma=frozenset(tup)
            removed={G for G in facets if sigma<=G}
            assert removed
            link={G-sigma for G in removed}
            vertices=set().union(*link)
            # Exactly a uniform skeleton, hence vertex-decomposable.
            assert all(len(H)==4-len(sigma) for H in link)
            assert len(link)==comb(len(vertices),4-len(sigma))
            # These are precisely the possible stranded faces of deletion.
            for G in removed:
                for x in sigma:assert ridges[G-{x}]>=2
            facets-=removed
            for G in removed:
                for t in subs(G,3):ridges[t]-=1
            steps+=1
    vertices=set().union(*facets)
    assert len(facets)==comb(len(vertices),4)
    return len(K),dict(histogram),len(initial),steps,len(facets),blocked

if __name__=="__main__":print(verify())
'''
Path('workspace/final_lower_certificate.py').write_text(code)
exec(code)