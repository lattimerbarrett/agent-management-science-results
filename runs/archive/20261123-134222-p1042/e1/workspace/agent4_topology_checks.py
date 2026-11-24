"""Exhaustive combinatorial checks of topology lemmas, not homology claims."""
from itertools import product,combinations
import json

def check(m):
    cap=(2,2,2,m-5)
    top=[]
    for w in product(range(4),repeat=m):
        counts=tuple(w.count(i) for i in range(4))
        if all(counts[i]<=cap[i] for i in range(4)):
            top.append(w)
    ridges=set()
    for w in top:
        deficit=[cap[i]-w.count(i) for i in range(4)]
        assert sorted(deficit)==[0,0,0,1]
        r=deficit.index(1)
        j=w.index(r)
        ridge=w[:j]+(-1,)+w[j+1:]
        assert ridge not in ridges
        ridges.add(ridge)
        extensions=[]
        for s in range(4):
            v=ridge[:j]+(s,)+ridge[j+1:]
            if all(v.count(i)<=cap[i] for i in range(4)):
                extensions.append(v)
        assert extensions==[w]
    missing=0
    for cols in combinations(range(m),3):
        for colors in product(range(4),repeat=3):
            counts=[colors.count(i) for i in range(4)]
            if all(counts[i]<=cap[i] for i in range(4)):
                continue
            missing+=1
            assert len(set(colors))==1
            r=colors[0]
            assert cap[r]==2
            newcol=next(j for j in range(m) if j not in cols)
            s=(r+1)%4
            for pair in combinations(range(3),2):
                tri=[(colors[k],cols[k]) for k in pair]+[(s,newcol)]
                assert len({j for _,j in tri})==3
                assert all(sum(1 for c,_ in tri if c==i)<=cap[i] for i in range(4))
    return dict(m=m,top_faces=len(top),distinct_free_ridges=len(ridges),missing_triangles_coned=missing)
if __name__=='__main__':
    result=[check(m) for m in range(7,10)]
    print(json.dumps(result,indent=2))
    from pathlib import Path
    Path('workspace/agent4_topology_checks.json').write_text(json.dumps(result,indent=2))
