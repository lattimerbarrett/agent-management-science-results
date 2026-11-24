from functools import lru_cache

def intersecting_upsets(n):
    # Minimal members of an intersecting upset form an antichain
    # of nonempty sets which is pairwise intersecting, and conversely.
    vertices=list(range(1,1<<n));N=len(vertices)
    adj=[sum(1<<j for j,y in enumerate(vertices) if x!=y and (x&y==x or x&y==y or not(x&y))) for x in vertices]
    @lru_cache(None)
    def f(S):
        if not S:return 1
        degmax=-1;v=None;isolated=0;T=S
        while T:
            b=T&-T;T-=b;x=b.bit_length()-1
            d=(adj[x]&S).bit_count()
            if d==0:isolated|=b
            elif d>degmax:degmax=d;v=x
        if isolated:return (1<<isolated.bit_count())*f(S^isolated)
        return f(S^(1<<v))+f(S&~((1<<v)|adj[v]))
    return f((1<<N)-1),f.cache_info()


"""Exact D(7) certificate via Boolean-lattice ideals and crown maps.
No stored Dedekind numbers are inputs.
"""
import itertools, numpy as np, time

def ideals_B4():
    down=[sum(1<<y for y in range(16) if y&x==y) for x in range(16)]
    return [mask for mask in range(1<<16) if all(not(mask>>x&1) or mask&down[x]==down[x] for x in range(16))]

def compute_D7():
    L=ideals_B4(); assert len(L)==168
    answer=0; intervals=0; cubes=0
    for T in L:
        Q=[x for x in L if x&T==x]
        union=np.bitwise_or(np.array(Q,dtype=np.uint64)[:,None],np.array(Q,dtype=np.uint64)[None,:])
        C=np.zeros((len(Q),len(Q)),dtype=np.int64)
        for z in Q:C+=(union & np.uint64(z))==union
        for B in Q:
            inds=[i for i,x in enumerate(Q) if x&B==B]
            M=C[np.ix_(inds,inds)]
            # sum M_xy M_yz M_zx = trace(M^3); entries are nonnegative
            answer+=int(np.sum((M@M)*M.T))
            intervals+=1;cubes+=len(inds)**3
    return answer,intervals,cubes


"""Exact lower count for d=9 safe-set construction."""
import itertools

def d9_certificate():
    groups=[set(range(0,3)),set(range(3,6)),set(range(6,9))]
    V=[frozenset(S) for S in itertools.combinations(range(9),4) if all(set(S)&g for g in groups)]
    I=[S for S in V if 0 in S]
    J=[S for S in V if 0 not in S]
    assert len(I)==36 and len(J)==45
    N=[sum(1<<i for i,S in enumerate(I) if not(S&T)) for T in J]
    sums=[];counts=[]
    for r in range(4):
        total=0;count=0
        for ids in itertools.combinations(range(len(J)),r):
            if all(J[i]&J[j] for i,j in itertools.combinations(ids,2)):
                U=0
                for i in ids: U|=N[i]
                total+=1<<(36-U.bit_count());count+=1
        sums.append(total);counts.append(count)
    return counts,sums


from math import comb
from fractions import Fraction

def coefficients(groups, special=False):
    out=[1]
    for j,g in enumerate(groups):
        p=[0]+[comb(g-1,i-1) if special and j==0 else comb(g,i) for i in range(1,g)]+[0]
        q=[0]*(len(out)+g)
        for a,x in enumerate(out):
            for b,y in enumerate(p): q[a+b]+=x*y
        out=q
    return out

def exponent(d):
    groups=sorted([d//3+(i<d%3) for i in range(3)])
    if d%2==0: return coefficients(groups)[d//2]//2
    return coefficients(groups,True)[d//2]

def check():
    # finite cases of binomial lemma, and exact rational uniform estimates
    for d in [14,15,16,17,19]:
        assert 5*exponent(d)>8*comb(d-2,(d-2)//2)
    even=Fraction(17,9)*Fraction(29,32)
    odd=Fraction(20,11)*(1-Fraction(1,64)-2*(Fraction(11,20)**7+Fraction(1,128)))
    assert even>Fraction(8,5) and odd>Fraction(8,5)
    assert 2**8>3**5
    for d in range(14,501):
        assert 5*exponent(d)>8*comb(d-2,(d-2)//2)
    print('Binomial lemma: finite exceptions and uniform rational estimates verified; additional d14..500 sanity checks passed.')
    print('Uniform estimates:',even,odd)
    print('Small capacities:',[(d,exponent(d)) for d in range(9,14)])


def run_all():
    lam7=intersecting_upsets(6)[0]
    D7=compute_D7()[0]
    assert lam7==1422564 and D7==2414682040998
    print('lambda7=',lam7,'D7=',D7)
    check()
    D=D7
    for d in range(10,14):
        D=D*(D+1)//2
        assert D<2**exponent(d)
    counts,sums=d9_certificate()
    assert sum(sums)>D7+1
    print('d9 certificate=',sum(sums))
    from agent3_lower_checks import check_standard_example
    assert check_standard_example()[0]==48
    exec(compile(open('workspace/agent4_root_doubling.py').read(),'root.py','exec'),{})
    assert 2*783558>lam7+1
    exec(compile(open('workspace/agent4_hansel.py').read(),'hansel.py','exec'),{})
    exec(compile(open('workspace/agent4_embedding.py').read(),'embedding.py','exec'),{})
    print('ALL CHECKS PASSED')
if __name__=='__main__':run_all()
