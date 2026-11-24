from functools import lru_cache
from itertools import product, combinations, permutations
from math import comb, prod
from fractions import Fraction
import numpy as np
import time

# Ideals of an inclusion poset, represented as bit masks.
def ideals_of(sets):
    N=len(sets)
    comparable=[sum(1<<j for j,b in enumerate(sets)
                    if a&b==a or a&b==b) for a in sets]
    down=[sum(1<<j for j,b in enumerate(sets) if a&b==b) for a in sets]
    result=[]
    def rec(candidates,I):
        result.append(I)
        while candidates:
            bit=candidates&-candidates; candidates-=bit
            i=bit.bit_length()-1
            rec(candidates&~comparable[i],I|down[i])
    rec((1<<N)-1,0)
    return result

# Number of intersecting upsets of B_m = lambda(m+1).
def intersecting_upsets(m):
    sets=sorted(range(1,1<<m),key=lambda x:(x.bit_count(),x))
    closed=[sum(1<<j for j,b in enumerate(sets)
                if a&b==a or a&b==b or a&b==0) for a in sets]
    @lru_cache(maxsize=4000000)
    def rec(mask):
        if not mask: return 1
        bit=mask&-mask; i=bit.bit_length()-1
        return rec(mask^bit)+rec(mask&~closed[i])
    answer=rec((1<<len(sets))-1)
    rec.cache_clear()
    return answer

# For a six-element standard example S, count ideals of S x T.
def standard_example_product_ideals(J):
    C=np.array([[sum(K&(A&B)==K for K in J) for B in J] for A in J],
               dtype=np.int64)
    return int(np.sum((C@C)*C))

# Exact D(7), using B_7 = B_3 x B_4.
def dedekind7():
    J=ideals_of(list(range(16))); n=len(J); index={A:i for i,A in enumerate(J)}
    le=np.array([[A&B==A for B in J] for A in J],dtype=np.int64)
    meet=np.array([[index[A&B] for B in J] for A in J])
    interval_size=le@le
    answer=0
    for b in range(n):
        Cfull=interval_size[b,meet]
        for a in range(n):
            if not le[b,a]: continue
            inside=np.flatnonzero(le[b,:]&le[:,a])
            C=Cfull[np.ix_(inside,inside)]
            answer+=int(np.sum((C@C)*C))
    return answer

# Ordered symmetric-chain decomposition with the alternate-diamond property.
def chains(n):
    answer=[[0]]
    for i in range(n):
        bit=1<<i; new=[]
        for C in answer:
            if len(C)>1: new.append([x|bit for x in C[:-1]])
            new.append(C+[C[-1]|bit])
        answer=new
    return answer

def check_chains(n):
    C=chains(n); owner={x:j for j,A in enumerate(C) for x in A}
    assert len(owner)==1<<n and len(C)==comb(n,n//2)
    for j,A in enumerate(C):
        assert A[0].bit_count()+A[-1].bit_count()==n
        for x,y,z in zip(A,A[1:],A[2:]):
            other=x|(z^y)
            assert owner[other]<j

# Middle-layer and star sizes for the restricted feature poset.
def balanced(d):
    return sorted([d//3+(i<d%3) for i in range(3)])

def lower_exponent(d):
    p=balanced(d)
    if d%2==0:
        W=sum(prod(comb(a,k) for a,k in zip(p,ks))
              for ks in product(*[range(1,a) for a in p]) if sum(ks)==d//2)
        assert W%2==0
        return W//2
    q=p.copy(); q[0]-=1
    return sum(prod(comb(a,k) for a,k in zip(q,ks))
               for ks in product(*[range(a+1) for a in q])
               if sum(ks)==d//2-1
               and all(1<=ks[i]+(i==0)<p[i] for i in range(3)))

# A small seed of self-dual upsets of the restricted feature poset.
def seed_families(groups,count):
    d=sum(map(len,groups)); full=(1<<d)-1
    masks=[sum(1<<i for i in g) for g in groups]
    R=[x for x in range(1<<d) if all(0<x&M<M for M in masks)]
    middle=[x for x in R if x.bit_count()==d//2]
    pairs=[(x,x^full) for x in middle if x<(x^full)]
    answer=[]
    for code in range(count):
        F={x for x in R if x.bit_count()>d//2}
        F.update(pair[(code>>j)&1] for j,pair in enumerate(pairs))
        assert all((x in F) != ((x^full) in F) for x in R)
        assert all(not(x in F and x&y==x) or y in F for x in R for y in R)
        answer.append(F)
    return R,answer

def lex_rows(d,R,families):
    rows=[]
    for i in range(d):
        rows.append(sorted(range(len(families)),key=lambda a:
            tuple(int((x in families[a]) == bool(x>>i&1)) for x in R)))
    return rows

def check_colored(rows,colors):
    d=len(rows); n=len(rows[0]); ranks=[{v:j for j,v in enumerate(R)} for R in rows]
    for a,b in permutations(range(n),2):
        for c in range(3):
            assert any(ranks[j][a]>ranks[j][b] and colors[j][a]==c for j in range(d))
    for a,b,c in permutations(range(n),3):
        assert any(R[a]>max(R[b],R[c]) for R in ranks)

def two_block_seed(count=4):
    d=8; A={0,1,2,3}
    groups0=[{0,1},{2,4,5},{3,6,7}]
    groups1=[{4,5},{6,0,1},{7,2,3}]
    rows_by_block=[]
    for groups in [groups0,groups1]:
        R,F=seed_families(groups,count)
        rows_by_block.append(lex_rows(d,R,F))
    colors=[[next(c for c,g in enumerate(groups0) if j in g)]*count+
            [next(c for c,g in enumerate(groups1) if j in g)]*count for j in range(d)]
    rows=[]
    for j in range(d):
        B0=rows_by_block[0][j]; B1=[v+count for v in rows_by_block[1][j]]
        rows.append(B1+B0 if j in A else B0+B1)
    check_colored(rows,colors)
    return rows,colors

# Check the entire product realizer for Boolean P of dimension t.
def check_product(t,rows,colors):
    n=len(rows[0]); P=list(product(range(2),repeat=t))
    L=[sorted(P,key=lambda p:(p[i],sum(p),p)) for i in range(t)]
    lp=[{p:j for j,p in enumerate(R)} for R in L]
    Q=[(v,) for v in range(n)]+list(combinations(range(n),2))
    elements=list(product(P,Q)); index={x:j for j,x in enumerate(elements)}
    extensions=[]
    for j,R in enumerate(rows):
        rank={v:i for i,v in enumerate(R)}
        def key(x):
            p,B=x; v=max(B,key=lambda v:rank[v]); c=colors[j][v]
            return rank[v],lp[c][p],len(B),B
        extensions.append(sorted(elements,key=key))
    for i in range(3,t):
        extensions.append(sorted(elements,key=lambda x:(lp[i][x[0]],len(x[1]),x[1])))
    N=len(elements); intersection=np.ones((N,N),dtype=bool)
    for R in extensions:
        rank=np.empty(N,dtype=np.int64)
        for i,x in enumerate(R):rank[index[x]]=i
        intersection &= rank[:,None]<=rank[None,:]
    actual=np.array([[all(a<=b for a,b in zip(p,q)) and set(B)<=set(C)
                      for q,C in elements] for p,B in elements],dtype=bool)
    assert np.array_equal(intersection,actual)
    print('Full product check:',t,n,N,len(extensions),flush=True)

if __name__=='__main__':
    start=time.time()
    lam7=intersecting_upsets(6); lam8=intersecting_upsets(7)
    D7=dedekind7()
    J=ideals_of(list(range(1,7)))
    H233=standard_example_product_ideals(J)
    assert (lam7,lam8,D7,H233)==(1422564,229809982112,2414682040998,783558)
    print('Exact counts:',lam7,lam8,D7,H233,flush=True)
    assert 2*H233>lam7
    assert 4*2**36-6*2**15>lam8
    # Verify the two special star calculations directly on the feature sets.
    for d,parts,star,pair in [(9,[3,3,3],36,15),(11,[3,4,4],164,48)]:
        masks=[]; offset=0
        for size in parts:
            masks.append(((1<<size)-1)<<offset); offset+=size
        layer=[x for x in range(1<<d) if x.bit_count()==d//2
               and all(0<x&M<M for M in masks)]
        assert sum(bool(x&1) for x in layer)==star
        if d==9:
            assert max(sum((x>>i&1) and (x>>j&1) for x in layer)
                       for i,j in combinations(range(d),2))==pair
        else:
            assert sum((x&3)==3 for x in layer)==pair
    assert 2**90>D7**2
    assert 2**165-2**48>D7**4
    assert 2**396>D7**8
    assert 2**690>D7**16
    assert [lower_exponent(d) for d in range(10,20)]==[90,164,396,690,1550,2800,6100,11008,23710,42805]
    for d in range(14,20): assert 5*lower_exponent(d)>8*comb(d-2,(d-2)//2)
    assert Fraction(29,32)*Fraction(17,9)>Fraction(8,5)
    assert Fraction(20,11)*(1-Fraction(1,64)-2*(Fraction(11,20)**7+Fraction(1,128)))>Fraction(8,5)
    assert 3**5<2**8
    for n in range(13): check_chains(n)
    rows,colors=two_block_seed()
    for t in [3,4]:check_product(t,rows,colors)
    print('All checks passed; seconds:',round(time.time()-start,2),flush=True)
