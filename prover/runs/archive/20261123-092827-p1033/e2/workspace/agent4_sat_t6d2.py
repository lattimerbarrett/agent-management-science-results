import itertools,time,z3
T=6;N=24
cores=[sum(1<<v for v in range(4*i,4*i+4)) for i in range(T)]
E=[]
for i,X in enumerate(cores):
    E.extend((X|(1<<a)|(1<<b),i) for a,b in itertools.combinations([v for v in range(N) if not X>>v&1],2))
for typ in ['same','different']:
    x=[z3.Bool(f'{typ}_{i}') for i in range(len(E))]
    s=z3.Solver();s.set(timeout=120000)
    seed=cores[0]|1<<4|1<<(5 if typ=='same' else 8)
    s.add(x[next(i for i,(e,g) in enumerate(E) if e==seed)])
    for i,(e,g) in enumerate(E):
        for j in range(i):
            if not e&E[j][0]:s.add(z3.Or(z3.Not(x[i]),z3.Not(x[j])))
        for v in range(N):
            if e>>v&1:s.add(z3.Implies(x[i],z3.Or([x[j] for j,(f,h) in enumerate(E) if e&f==1<<v])))
    for C in itertools.combinations(range(N),5):
        mask=sum(1<<v for v in C)
        s.add(z3.Or([x[j] for j,(e,g) in enumerate(E) if not e&mask]))
    ans=s.check();print(typ,ans)
    assert ans==z3.unsat
