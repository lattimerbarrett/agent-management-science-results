from itertools import combinations
from z3 import Solver, Bool, Or, Not, sat

def check(t,rs,k=None,extra=0):
    if k is None:k=t
    blocks=[]; n=0
    for r in rs:
        blocks.append(set(range(n,n+k-r))); n+=k-r
    n+=extra
    full=(1<<n)-1
    edges=[]; groups=[]
    for i,(X,r) in enumerate(zip(blocks,rs)):
        xm=sum(1<<x for x in X)
        avail=[x for x in range(n) if x not in X]
        ids=[]
        for R in combinations(avail,r):
            ids.append(len(edges)); edges.append(xm|sum(1<<x for x in R))
        groups.append(ids)
    s=Solver(); s.set(timeout=40000)
    vs=[Bool('e%d'%j) for j in range(len(edges))]
    for ids in groups:s.add(Or([vs[j] for j in ids]))
    for i,E in enumerate(edges):
        for j in range(i):
            if not E&edges[j]:s.add(Or(Not(vs[i]),Not(vs[j])))
    for C in combinations(range(n),t-1):
        cm=sum(1<<c for c in C)
        s.add(Or([vs[j] for j,E in enumerate(edges) if not E&cm]))
    ans=s.check()
    print(t,rs,k,extra,'n',n,'edges',len(edges),str(ans),flush=True)
    if ans==sat:
        m=s.model()
        print([[list(x for x in range(n) if edges[j]>>x&1) for j in ids if bool(m.eval(vs[j]))] for ids in groups],flush=True)
check(6,(2,2,2,2,2,2))
