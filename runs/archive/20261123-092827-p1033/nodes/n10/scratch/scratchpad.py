import itertools, z3, time, json

def check(t,k,rs, timeout=3000):
    blocks=[]; n=0
    for r in rs:
        blocks.append(set(range(n,n+k-r))); n+=k-r
    if sum(__import__('math').comb(n-len(b),r) for b,r in zip(blocks,rs))>20000:return None
    edges=[]; groups=[]
    U=set(range(n))
    for i,(b,r) in enumerate(zip(blocks,rs)):
        for a in itertools.combinations(sorted(U-b),r):
            edges.append(sum(1<<x for x in b.union(a)));groups.append(i)
    vs=[z3.Bool('e'+str(j)) for j in range(len(edges))]
    s=z3.Solver();s.set(timeout=timeout)
    for i in range(t):s.add(z3.Or([v for v,g in zip(vs,groups) if g==i]))
    for i,e in enumerate(edges):
        for j in range(i):
            if not e&edges[j]:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
    for c in itertools.combinations(range(n),t-1):
        mask=sum(1<<x for x in c)
        s.add(z3.Or([v for v,e in zip(vs,edges) if not mask&e]))
    ans=s.check()
    if ans==z3.sat:
        m=s.model();out={'t':t,'k':k,'rs':rs,'blocks':[sorted(b) for b in blocks], 'edges':[(g,[x for x in range(n) if e>>x&1]) for v,e,g in zip(vs,edges,groups) if z3.is_true(m.eval(v))]}
        print('FOUND',out,flush=True);json.dump(out,open('counterexample.json','w'));return out
    print(t,k,rs,len(edges),ans,flush=True)
    return None

# targeted run
check(6,6,(2,2,2,2,2,2),timeout=20000)
