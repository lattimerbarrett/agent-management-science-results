"""Exact colorful decision-tree certificate for exceptional d=11."""
from functools import lru_cache
from itertools import combinations
import json

def certificate():
    n=11; full=(1<<n)-1
    base=(sum(1<<i for i in range(4)),sum(1<<i for i in range(4,8)),sum(1<<i for i in range(8,11)))
    parts={tuple(sorted(base))}
    for u in range(n):
        for v in range(u+1,n):
            p=list(base)
            a=next(j for j,g in enumerate(p) if g>>u&1)
            b=next(j for j,g in enumerate(p) if g>>v&1)
            if a!=b:
                p[a]^=(1<<u)|(1<<v); p[b]^=(1<<u)|(1<<v)
            parts.add(tuple(sorted(p)))
    parts=sorted(parts)
    assert len(parts)==41
    assert all(sorted(g.bit_count() for g in P)==[3,4,4] for P in parts)
    pairs=[sum(1<<v for v in C) for C in combinations(range(n),n//2) if 0 in C]
    assert len(pairs)==210
    # All small sides contain 0; all large sides have size6>11/2.
    assert all(A&B for A in pairs for B in pairs)
    assert all(A&(full^B) for A in pairs for B in pairs if A!=B)
    assert all((full^A)&(full^B) for A in pairs for B in pairs)
    masks=[tuple(sum(1<<i for i,P in enumerate(parts) if all(C&g for g in P)) for C in (A,full^A)) for A in pairs]
    @lru_cache(None)
    def count(i,state):
        assert state
        if i==len(pairs):return 1
        x,y=masks[i]; a,b=state&x,state&y
        if a and b:return count(i+1,a)+count(i+1,b)
        return count(i+1,state)
    N=count(0,(1<<len(parts))-1)
    assert N==70147797197254365921174683698968834468206262353920
    D7=2414682040998
    assert N>D7**4
    return dict(d=n,partitions=len(parts),pairs=len(pairs),states=count.cache_info().currsize,leaves=N,D7fourthpower=D7**4)
if __name__=='__main__':print(json.dumps(certificate(),indent=2))
