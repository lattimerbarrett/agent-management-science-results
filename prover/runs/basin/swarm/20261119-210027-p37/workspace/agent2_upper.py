"""Exact finite checks for the mixed-coordinate product upper bound."""
from itertools import combinations,product

def maximal_intersecting(k):
    # Choose one from every complementary pair, test upwardness/intersection.
    full=(1<<k)-1
    reps=[a for a in range(1<<k) if a<(full^a)]
    ans=[]
    for bits in product((0,1),repeat=len(reps)):
        F=frozenset((a if b==0 else full^a) for a,b in zip(reps,bits))
        if all(a&b for a in F for b in F): ans.append(F)
    return ans

def lex_ranks(families,k):
    full=(1<<k)-1
    reps=[a for a in range(1<<k) if a<(full^a)]
    ranks=[]
    for i in range(k):
        def key(F):
            return tuple(int(bool(((a if a in F else full^a)>>i)&1)) for a in reps)
        order=sorted(range(len(families)),key=lambda j:key(families[j]))
        ranks.append([order.index(j) for j in range(len(families))])
    return ranks

def suitable(ranks):
    n=len(ranks[0])
    return all(any(R[a]>max(R[b],R[c]) for R in ranks)
               for a in range(n) for b,c in combinations([v for v in range(n) if v!=a],2))

def pair_separating(ranks,parts):
    n=len(ranks[0])
    return all(any(ranks[i][a]>ranks[i][b] for i in part)
               for part in parts for a in range(n) for b in range(n) if a!=b)

def check_embedding(ranks,parts,t=3,m=2):
    # Embedding for P=[m]^t; other P follow by restriction.
    assert len(parts)<=t
    assert sorted(i for part in parts for i in part)==list(range(len(ranks)))
    assert suitable(ranks) and pair_separating(ranks,parts)
    n=len(ranks[0]); Q=[(a,) for a in range(n)]+list(combinations(range(n),2))
    points=list(product(product(range(m),repeat=t),Q))
    def image(p,A):
        out=list(p[len(parts):])
        for j,part in enumerate(parts):
            out.extend(m*max(ranks[i][a] for a in A)+p[j] for i in part)
        return tuple(out)
    imgs=[image(*x) for x in points]
    for h,(p,A) in enumerate(points):
        for j,(q,B) in enumerate(points):
            assert (all(a<=b for a,b in zip(p,q)) and set(A)<=set(B)) == all(a<=b for a,b in zip(imgs[h],imgs[j]))
    return len(points),len(imgs[0])

if __name__=='__main__':
    for k in range(1,5):
        F=maximal_intersecting(k)
        assert len(F)==[1,2,4,12][k-1]
        ranks=lex_ranks(F,k)
        if len(F)>=3:
            assert suitable(ranks)
            print('checked',k,len(F),check_embedding(ranks,[list(range(k))]))


def truncated_cube_product_ideals(a,b):
    """Counts all ideals of (B_a minus endpoints) x (B_b minus endpoints)."""
    from functools import lru_cache
    X=list(product(range(1,(1<<a)-1),range(1,(1<<b)-1)))
    N=len(X);lo=[];hi=[]
    for x,y in X:
        lo.append(sum(1<<i for i,(z,w) in enumerate(X) if z&x==z and w&y==w))
        hi.append(sum(1<<i for i,(z,w) in enumerate(X) if z&x==x and w&y==y))
    @lru_cache(None)
    def rec(mask):
        if not mask:return 1
        bits=[i for i in range(N) if mask>>i&1]
        i=max(bits,key=lambda j:(mask&lo[j]).bit_count()*(mask&hi[j]).bit_count())
        return rec(mask&~lo[i])+rec(mask&~hi[i])
    answer=rec((1<<N)-1)
    return answer,rec.cache_info().currsize

def check_gluing_masks():
    # P=(012,345,67), U=(0,3,6,7); Q chosen with pair in U-complement.
    P=(0b00000111,0b00111000,0b11000000)
    U=0b11001001;Uc=255^U
    # Uc={1,2,4,5}; take Qpair={1,2}, remaining groups each hit Uc.
    Q=(0b00000110,0b00011001,0b11100000)
    assert sum(P)==255 and sum(Q)==255
    assert P[2]&U==P[2] and Q[0]&Uc==Q[0]
    assert all(U&x for x in P) and all(Uc&x for x in Q)
    count,states=truncated_cube_product_ideals(3,3)
    assert count==783558
    assert 2*count>1422564+1
    return count,states


def check_variable_embedding(ranks,colors,t=3,m=2):
    """colors[i][a] is a P coordinate assigned at vertex a in Q coordinate i."""
    n=len(ranks[0]);s=len(ranks)
    assert suitable(ranks)
    assert all(any(ranks[i][a]>ranks[i][b] and colors[i][a]==j for i in range(s))
               for a in range(n) for b in range(n) if a!=b for j in range(t))
    Q=[(a,) for a in range(n)]+list(combinations(range(n),2))
    X=list(product(product(range(m),repeat=t),Q))
    def image(p,A):
        return tuple(max(m*ranks[i][a]+p[colors[i][a]] for a in A) for i in range(s))
    Y=[image(*x) for x in X]
    for u,(p,A) in enumerate(X):
        for v,(q,B) in enumerate(X):
            assert (all(a<=b for a,b in zip(p,q)) and set(A)<=set(B))==all(a<=b for a,b in zip(Y[u],Y[v]))
    return len(X),s
