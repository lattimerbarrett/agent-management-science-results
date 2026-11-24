"""Exact finite checker for a proposed lower-bound witness.
It never treats a failed greedy path as proof of non-completability.
The visited-state dynamic program explores EVERY permitted next facet.
"""
from itertools import combinations
from functools import lru_cache
from kdecomp_agent4 import kdecomp

def completion(facets, k, r=0):
    fs=frozenset(map(frozenset,facets))
    assert fs and len({len(f) for f in fs})==1
    assert kdecomp(fs,k)
    V=set().union(*fs)
    A=[('fresh',j) for j in range(r)]
    assert not (set(A)&V)
    q=len(next(iter(fs)))
    U=list(V)+A
    allf=list(map(frozenset,combinations(U,q)))
    pos={f:i for i,f in enumerate(allf)}
    full=(1<<len(allf))-1
    start=sum(1<<pos[f] for f in fs)
    @lru_cache(None)
    def solve(mask):
        if mask==full:return ()
        cur=frozenset(allf[i] for i in range(len(allf)) if mask>>i&1)
        for i,F in enumerate(allf):
            if not mask>>i&1 and kdecomp(cur|{F},k):
                result=solve(mask|(1<<i))
                if result is not None:return (F,)+result
        return None
    out=solve(start)
    return out,solve.cache_info().currsize

if __name__=='__main__':
    # Nontrivial positive test: two tetrahedra glued along a triangle.
    F=[{0,1,2,3},{0,1,2,4}]
    path,states=completion(F,1)
    assert path is not None and len(path)==3
    print('Exact completion verified:',path,'states',states)
