from functools import lru_cache
from itertools import combinations

# Exact ordinals below omega^2 are pairs (b,t), representing omega*b+t.
def enum(beta, k):
    b,t=beta
    if b==0:
        assert t>0
        return (0,min(k,t-1))
    if k<t:
        return (b,k)
    q,r=divmod(k-t,b)
    return (r,q)

@lru_cache(None)
def F(beta,n):
    if beta==(0,0):
        return frozenset([beta])
    seen=set()
    prev_alpha=None
    prev_level=-1
    k=0
    active=None
    while True:
        seen.add(enum(beta,k))
        alpha=max(seen)
        level=prev_level+1
        required=seen | ({prev_alpha} if prev_alpha is not None else set())
        while not required.issubset(F(alpha,level)):
            level+=1
        if level>n:
            return frozenset([beta]) if active is None else F(active,n)|{beta}
        active=alpha
        prev_alpha,prev_level=alpha,level
        k+=1


def finite_subset_checks():
    ords=[(b,t) for b in range(4) for t in range(9)]
    checked=0
    for beta in ords:
        for n in range(7):
            B=F(beta,n)
            assert beta in B
            assert all(a<=beta for a in B)
            assert B.issubset(F(beta,n+1))
            for a in B:
                assert F(a,n)==frozenset(x for x in B if x<=a)
                checked+=1
    # Every listed predecessor is actually eventually included; compute witnesses.
    max_witness=0
    for beta in ords:
        for a in ords:
            if a<=beta:
                n=0
                while a not in F(beta,n):
                    n+=1
                    assert n<500
                max_witness=max(max_witness,n)
    return checked,max_witness

# Finite induced pieces of the constructed auxiliary poset.
# s_n is ('s',n); t_{alpha,n} is ('t',alpha,n).
def height(x): return x[-1]
def le(x,y):
    if x[0]=='s': return height(x)<=height(y)
    if y[0]=='s': return False
    return height(x)<=height(y) and x[1] in F(y[1],height(y))

def check_poset(ords,levels):
    A=[('s',n) for n in range(levels)]
    A += [('t',a,n) for a in ords for n in range(levels)]
    N=len(A)
    rows=[{j for j,y in enumerate(A) if le(x,y)} for x in A]
    for i in range(N):
        assert i in rows[i]
        for j in rows[i]:
            assert i==j or i not in rows[j]
            assert rows[j].issubset(rows[i])
    # Check the proof's fixed-height common-upper-bound implication.
    triples=0
    for n in range(levels):
        for gamma in ords:
            lower=[a for a in ords if a in F(gamma,n)]
            for a in lower:
                for b in lower:
                    assert a in F(b,n) or b in F(a,n)
                    triples+=1
    # Actually find a common upper bound for every pair, allowing extra levels.
    max_level=0
    for x in A:
        for y in A:
            ts=[z[1] for z in (x,y) if z[0]=='t']
            if not ts:
                z=('s',max(height(x),height(y)))
            else:
                beta=max(ts)
                m=max(height(x),height(y))
                while not all(a in F(beta,m) for a in ts): m+=1
                z=('t',beta,m)
                max_level=max(max_level,m)
            assert le(x,z) and le(y,z)
    return N,triples,max_level

def exhaustive_finite_dcpo():
    A=[('s',n) for n in range(2)] + [('t',(0,a),n) for a in range(3) for n in range(2)]
    N=len(A)
    subsets=[set(i for i in range(N) if mask>>i&1) for mask in range(1,1<<N)]
    def below(i,j): return le(A[i],A[j])
    def directed(S):
        return all(any(below(i,k) and below(j,k) for k in S) for i in S for j in S)
    def chain(S): return all(below(i,j) or below(j,i) for i in S for j in S)
    dirs=[S for S in subsets if directed(S)]
    chains=[S for S in subsets if chain(S)]
    def sup(S):
        ub=[j for j in range(N) if all(below(i,j) for i in S)]
        least=[j for j in ub if all(below(j,k) for k in ub)]
        assert len(least)==1
        return least[0]
    ds=[(D,sup(D)) for D in dirs]
    cs=[(C,sup(C)) for C in chains]
    rels=[]
    for tests in (cs,ds):
        rel={(a,b) for a in range(N) for b in range(N)
             if all(not below(b,s) or any(below(a,c) for c in C) for C,s in tests)}
        rels.append(rel)
    order={(a,b) for a in range(N) for b in range(N) if below(a,b)}
    assert rels[0]==rels[1]==order
    # Enumerate all directed lower sets and check the finite versions of T.
    ideals=[D for D in dirs if all(j in D for i in D for j in range(N) if below(j,i))]
    for D in ideals:
        TD={p for C,s in cs if C.issubset(D) for p in range(N) if below(p,s)}
        assert TD==D
    return N,len(subsets),len(chains),len(dirs),len(ideals)

if __name__=='__main__':
    print('F: coherence identities checked, largest covering witness:',finite_subset_checks())
    print('Auxiliary poset: size, fixed-height checks, upper-bound level:',
          check_poset([(b,t) for b in range(3) for t in range(5)],4))
    print('Exhaustive finite dcpo: size, subsets, chains, directed sets, ideals:',exhaustive_finite_dcpo())
