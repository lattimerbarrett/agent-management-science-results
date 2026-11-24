from itertools import combinations, product
from math import comb, sqrt


def construction(t):
    # |X_i|=i, with indices i=1,...,t.
    cores=[]
    p=0
    for i in range(1,t+1):
        cores.append(frozenset(range(p,p+i)))
        p+=i
    groups=[]
    for i in range(t):
        groups.append([cores[i] | frozenset(z)
                       for z in product(*[tuple(x) for x in cores[i+1:]])])
    return cores,groups,p


def witness(cores,C):
    # The largest completely covered block has size h.
    h=max([i+1 for i,X in enumerate(cores) if X <= C],default=0)
    i=next(i for i in range(h,len(cores)) if not (cores[i]&C))
    F=set(cores[i])
    for X in cores[i+1:]:
        F.add(next(iter(X-C)))
    assert not(F&C)
    return i,frozenset(F)


def check_rainbow_lemma(cores,groups):
    R=max(len(F-cores[i]) for i,G in enumerate(groups) for F in G)
    D=set();chosen=[]
    # One pass constructs a maximal rainbow matching of residuals.
    for i,G in enumerate(groups):
        for F in G:
            residual=F-cores[i]
            if D.isdisjoint(residual):
                chosen.append((i,F,residual))
                D.update(residual)
                break
    m=len(chosen)
    charges=0
    for a,(i,F,A) in enumerate(chosen):
        for j,G,B in chosen[:a]:
            assert A.isdisjoint(B)
            assert F&G
            assert (A&cores[j]) or (B&cores[i])
    for i,F,A in chosen:
        charges += sum(bool(A&cores[j]) for j,G,B in chosen if j!=i)
    assert comb(m,2) <= charges <= m*R
    assert m<=2*R+1
    cover=D | {next(iter(cores[i])) for i,F,A in chosen}
    assert all(cover&F for G in groups for F in G)
    assert len(cover)<=m*(R+1)<=(2*R+1)*(R+1)
    return m,len(cover)


if __name__=='__main__':
    for t in range(2,7):
        cores,groups,n=construction(t)
        family=[F for G in groups for F in G]
        assert len(family)==len(set(family))
        assert all(len(F)==t for F in family)
        assert all(X for X in cores)
        assert all(not(cores[i]&cores[j]) for i in range(t) for j in range(i))
        assert all(cores[i]<=F for i,G in enumerate(groups) for F in G)
        assert all(F&G for i,F in enumerate(family) for G in family[:i])
        table=[set(G) for G in groups]
        tested=0
        for c in combinations(range(n),t-1):
            C=frozenset(c)
            i,F=witness(cores,C)
            assert F in table[i]
            tested+=1
        assert tested==comb(n,t-1)
        cover={next(iter(X)) for X in cores}
        assert all(cover&F for F in family)
        cost=sum(t-len(X) for X in cores)
        assert cost==comb(t,2)
        check_rainbow_lemma(cores,groups)
        # Check the lemma on every nonempty subfamily of groups as well.
        for bits in range(1,1<<t):
            I=[i for i in range(t) if bits>>i&1]
            check_rainbow_lemma([cores[i] for i in I],[groups[i] for i in I])
        print(f't={t}, |V|={n}, |F|={len(family)}, cost={cost}, '
              f'noncovers of size t-1 checked={tested}')

# Small, finite SAT experiments; these do not replace an asymptotic proof.
def finite_search(a,k,extra=0,timeout=10000):
    import z3
    t=len(a);n=sum(k-r for r in a)+extra
    cs=[];p=0
    for r in a:
        cs.append(sum(1<<j for j in range(p,p+k-r)));p+=k-r
    edges=[]; labels=[]
    for i,r in enumerate(a):
        for R in combinations([v for v in range(n) if not(cs[i]>>v&1)],r):
            edges.append(cs[i]|sum(1<<v for v in R));labels.append(i)
    if len(edges)>4000:return 'large',len(edges)
    xs=[z3.Bool('x'+str(i)) for i in range(len(edges))]
    s=z3.Tactic('sat').solver();s.set(timeout=timeout)
    for i,A in enumerate(edges):
        for j,B in enumerate(edges[:i]):
            if A&B==0:s.add(z3.Or(z3.Not(xs[i]),z3.Not(xs[j])))
    for C0 in combinations(range(n),t-1):
        C=sum(1<<v for v in C0)
        s.add(z3.Or([x for x,E in zip(xs,edges) if not C&E]))
    ans=s.check()
    if ans==z3.sat:
        mod=s.model(); fam=[(i,E) for x,i,E in zip(xs,labels,edges) if z3.is_true(mod.eval(x))]
        print('FOUND',a,k,extra,cs,fam,flush=True)
        import pickle
        pickle.dump((a,k,extra,cs,fam),open('small_found.pkl','wb'))
    return str(ans),len(edges)

def lazy_search(t,k,r,pattern=0,seconds=120):
    import z3,time,pickle
    started=time.monotonic()
    ranks=[r]*t if isinstance(t,int) else t
    t=len(ranks);cs=[];p=0
    for rank in ranks:
        cs.append(sum(1<<v for v in range(p,p+k-rank)));p+=k-rank
    n=p
    m=(cs[1]&-cs[1]).bit_length()-1
    mm=(cs[2]&-cs[2]).bit_length()-1
    fixed=cs[0]|(1<<m)|(1<<(m+1 if pattern==0 else mm))
    edges=[];labels=[]
    for i in range(t):
        for R in combinations([v for v in range(n) if not(cs[i]>>v&1)],ranks[i]):
            E=cs[i]|sum(1<<v for v in R)
            if E&fixed:edges.append(E);labels.append(i)
    xs=[z3.Bool('x'+str(i)) for i in range(len(edges))]
    s=z3.Tactic('sat').solver();s.set(timeout=60000,phase='always_true')
    s.add(xs[edges.index(fixed)])
    for i,A in enumerate(edges):
        for j,B in enumerate(edges[:i]):
            if not A&B:s.add(z3.Or(z3.Not(xs[i]),z3.Not(xs[j])))
    print('LAZY initialized',t,k,r,pattern,len(edges),flush=True)
    allmask=(1<<len(edges))-1
    avoid=[sum(1<<i for i,E in enumerate(edges) if not(E>>v&1)) for v in range(n)]
    total=0
    def add_noncover(C):
        bits=allmask
        for v in range(n):
            if C>>v&1:bits &= avoid[v]
        clause=[]
        while bits:
            lo=bits&-bits;clause.append(xs[lo.bit_length()-1]);bits-=lo
        s.add(z3.Or(clause))
    for C0 in combinations([v for v in range(n) if fixed>>v&1],t-1):
        add_noncover(sum(1<<v for v in C0))
    for iteration in range(100000):
        if time.monotonic()-started>seconds:break
        ans=s.check()
        if ans!=z3.sat:
            print('LAZY END',t,k,r,pattern,ans,'constraints',total,flush=True);return str(ans)
        mod=s.model();fam=[E for x,E in zip(xs,edges) if z3.is_true(mod.eval(x))]
        ys=[z3.Bool('y'+str(v)) for v in range(n)]
        cov=z3.Solver();cov.set(timeout=20000)
        cov.add(z3.PbLe([(y,1) for y in ys],t-1))
        for E in fam:cov.add(z3.Or([ys[v] for v in range(n) if E>>v&1]))
        count=0
        for z in range(500):
            ca=cov.check()
            if ca!=z3.sat:break
            cm=cov.model();C=sum(1<<v for v in range(n) if z3.is_true(cm.eval(ys[v])))
            add_noncover(C);count+=1
            cov.add(z3.Or([z3.Not(ys[v]) for v in range(n) if C>>v&1]))
        if not count and ca==z3.unsat:
            print('LAZY FOUND',t,k,r,pattern,len(fam),flush=True)
            pickle.dump((cs,edges,labels,fam),open(f'lazy_found_{t}_{k}_{pattern}.pkl','wb'))
            return 'FOUND'
        total+=count
        print('LAZY',iteration,'family',len(fam),'new constraints',count,'total',total,'time',round(time.monotonic()-started,2),flush=True)
    print('LAZY TIMEOUT',t,k,r,pattern,flush=True)

for ranks,pattern in [([2,2,2,2,3,3],0),([2,3,2,2,2,3],0),([2,2,2,2,3,3],1),([2,2,3,2,2,3],1),([2,3,3,2,2,2],1)]:
    print('RANKS',ranks,pattern,flush=True)
    lazy_search(ranks,6,2,pattern,seconds=180)

