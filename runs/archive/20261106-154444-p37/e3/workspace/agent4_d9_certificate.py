"""Exact adaptive colorful tree capacity for d=9; standard Python only."""
from functools import lru_cache
from itertools import combinations
import json

def certificate(n=9):
    parts=[]
    def rec(a,m):
        if len(a)==n:
            if m==2:
                parts.append(tuple(sum(1<<i for i,x in enumerate(a) if x==j) for j in range(3)))
            return
        for x in range(min(m+1,2)+1): rec(a+[x],max(m,x))
    rec([0],0)
    full=(1<<n)-1
    pairs=[sum(1<<v for v in C) for C in combinations(range(n),n//2) if 0 in C]
    # For n odd, all small sides contain point 0 and hence intersect.
    # Two large sides always intersect. A small and large side can be
    # disjoint only when they are the complementary sides of the same pair.
    assert len(set(pairs))==len(pairs)
    assert all(A&B for A in pairs for B in pairs)
    assert all(A&(full^B) for A in pairs for B in pairs if A!=B)
    assert all((full^A)&(full^B) for A in pairs for B in pairs)
    masks=[]
    for A in pairs:
        masks.append(tuple(sum(1<<i for i,P in enumerate(parts) if all(C&g for g in P)) for C in (A,full^A)))
    @lru_cache(None)
    def count(i,state):
        assert state
        if i==len(pairs): return 1
        x,y=masks[i]; a,b=state&x,state&y
        if a and b: return count(i+1,a)+count(i+1,b)
        return count(i+1,state)
    leaves=count(0,(1<<len(parts))-1)
    assert len(parts)==3025 and len(pairs)==56
    assert leaves==234983774257
    return dict(n=n,partitions=len(parts),pairs=len(pairs),leaves=leaves,states=count.cache_info().currsize)
if __name__=='__main__':
    result=certificate(); print(json.dumps(result,indent=2))
