"""Exact lambda(k+1) as intersecting upsets on B_k (Shannon restriction).
An intersecting upset U of subsets of [k] determines a self-dual upset on
[k+1]: F restricted to sets not containing k+1 is U, and its other choices
are forced by complement. This is monotone iff U is intersecting.
The recurrence selects an undecided nonempty set A. Include A: force all
supersets, forbid all disjoint sets. Exclude A: forbid all subsets.
Previously forced/forbidden sets cannot conflict since every remaining
available set has no forbidden superset or included disjoint set.
Empty upset is counted, but empty set itself is never available.
"""
from functools import lru_cache

def lambda_next(k):
    vals=list(range(1,1<<k)); n=len(vals)
    up=[]; down=[]; dis=[]
    for a in vals:
        up.append(sum(1<<i for i,b in enumerate(vals) if a&b==a))
        down.append(sum(1<<i for i,b in enumerate(vals) if a&b==b))
        dis.append(sum(1<<i for i,b in enumerate(vals) if not a&b))
    @lru_cache(None)
    def count(state):
        if not state:
            return 1
        ids=[i for i in range(n) if state>>i&1]
        i=max(ids,key=lambda i:min((up[i]&state).bit_count()+(dis[i]&state).bit_count(),(down[i]&state).bit_count()))
        return count(state&~(up[i]|dis[i]))+count(state&~down[i])
    return count((1<<n)-1)

if __name__=='__main__':
    got=[lambda_next(k) for k in range(1,7)]
    assert got==[2,4,12,81,2646,1422564]
    print('lambda(2)..lambda(7) =',got)
