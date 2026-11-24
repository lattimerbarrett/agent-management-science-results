"""Exact shellability SAT on a fixed facet family; positive outputs verified."""
from functools import lru_cache
import z3
from agent1_shellability import verify_shelling,restriction
from agent1_boundary_fill import fill_certificate
from agent3_checker import verify

@lru_cache(None)
def shelling_sat(fs,timeout=30000):
    n=len(fs)
    assert fs and len({f.bit_count() for f in fs})==1
    if n==1:return fs
    t=[z3.Int('t'+str(i)) for i in range(n)]
    s=z3.Solver();s.set(timeout=timeout)
    s.add(z3.Distinct(t),*[z3.And(x>=1,x<=n) for x in t])
    for i,F in enumerate(fs):
        bits=[1<<v for v in range(F.bit_length()) if F>>v&1]
        rp={v:z3.Or([t[h]<t[i] for h,H in enumerate(fs) if h!=i and H&(F^v)==F^v]) for v in bits}
        for j,G in enumerate(fs):
            if i==j:continue
            s.add(z3.Implies(t[j]<t[i],z3.Or([rp[v] for v in bits if not G&v])))
    result=s.check()
    if result==z3.unknown:raise TimeoutError(s.reason_unknown())
    if result==z3.unsat:return None
    model=s.model();order=tuple(fs[i] for i in sorted(range(n),key=lambda i:model[t[i]].as_long()))
    verify_shelling(order)
    return order

def shelling_to_kcertificate(order):
    rank=order[0].bit_count();k=max(0,rank-2)
    c=('simplex',order[0]);previous=(order[0],)
    for F in order[1:]:
        R=restriction(previous,F)
        assert R is not None and R
        if R.bit_count()<=k+1:c=('shed',R,c,('simplex',F^R))
        else:c=fill_certificate(tuple(sorted(previous)),k,c,F)
        previous=previous+(F,)
    verify(tuple(sorted(order)),k,c)
    return c
