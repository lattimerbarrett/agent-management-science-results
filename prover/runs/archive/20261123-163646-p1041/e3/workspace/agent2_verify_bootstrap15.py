"""Exact checks for the unconditional m14/m15 bootstrap and constantQ15 proof.
Not a codeword enumeration. StrictKT and numericKTA are explicitly external.
"""
from fractions import Fraction
from math import comb
from itertools import combinations,product

def rank(vs):
    piv={}
    for v in vs:
        while v:
            j=v.bit_length()-1
            if j not in piv:piv[j]=v;break
            v^=piv[j]
    return len(piv)

def verify():
    for m in (14,15):
        K=(1<<(m-10))-1;N=1<<m
        for w in (322,326,330,334):
            avg=Fraction(w)-2*comb(w,2)*Fraction(K,N-1)+4*comb(w,3)*Fraction(K*(K-1),(N-1)*(N-2))
            assert avg<256
            print('cubic projection',m,w,avg,float(avg))
    # Fiber Bonferroni for every occupancy in largest starting kernel.
    for t in range(33):assert t%2<=t-2*comb(t,2)+4*comb(t,3)
    for k in range(2,6):
        assert Fraction((1<<k)*167,(1<<(k+1))-1)<96
        # Every k-vector in dimension k+1 is decomposable: enumerate every
        # hyperplane via its covector and compute its Pluecker coordinates.
        n=k+1;seen=set()
        for ell in range(1,1<<n):
            rows=[v for v in range(1,1<<n) if (v&ell).bit_count()%2==0]
            B=[]
            for v in rows:
                if rank(B+[v])>len(B):B.append(v)
            assert len(B)==k
            pl=0
            for omitted in range(n):
                cols=[j for j in range(n) if j!=omitted]
                mat=[sum(((v>>j)&1)<<a for a,j in enumerate(cols)) for v in B]
                if rank(mat)==k:pl|=1<<omitted
            assert pl==ell
            seen.add(pl)
        assert len(seen)==(1<<n)-1
        # All k-fibers exactly obey the odd/even projection formula and
        # the nonzero-XOR half-characters identity (largest k5 has2^32
        # subsets, so use ALL subsets for k<=4 and all moment vectors k5).
        for v in range(1<<k):
            assert sum((v&ell).bit_count()%2 for ell in range(1,1<<k))==((1<<(k-1)) if v else 0)
        if k<=4:
            for mask in range(1<<(1<<k)):
                F=[x for x in range(1<<k) if mask>>x&1]
                v=0
                for x in F:v^=x
                for ell in range(1,1<<k):
                    c=sum((x&ell).bit_count()%2 for x in F)
                    wt=(c%2)+((len(F)-c)%2)
                    assert wt==(1 if len(F)%2 else 2*((v&ell).bit_count()%2))
        if k>=3:
            assert 128+Fraction(1<<(k-1),(1<<k)-1)*206<256
    # Classical numeric coefficient gaps suffice for the 2D anisotropic case.
    allowed=(64,96,112,120,124,126,128,136,144,148,152,154,156,158)
    triples=set()
    for ww in product(allowed,repeat=3):
        if sum(ww)<=334 and sum((w//2)%2 for w in ww)==1 and 64 not in ww:
            triples.add(tuple(sorted(ww)))
    assert triples=={(96,96,126),(96,112,126)}
    assert 3*126>334
    # Exterior ambient reduction: a common nonzero5-form essentialspace
    # forces the support sum dimension<=12, forbidding an external vector.
    assert 8+9-5==12<13
    assert 8-3<6
    # LemmaA convolution coset lowerbound and LemmaD punctured bounds.
    assert (1<<(14-7))-1==127
    assert 128+2*127>334
    assert 334-256<96 and 334-256-64<32
    assert 12<13<=14
    # ALL numerical three-flat intersection possibilities for weight256.
    sizes=(0,1,2,4,8,16,32)
    for p,q,r,t in product(sizes,repeat=4):
        if t>min(p,q,r) or p+q+r-2*t!=64:continue
        if t>=2:continue # actual common period
        if t==1:
            assert sorted((p,q,r))==[2,32,32]
            assert 5+5-7>0 # contradicts singleton commonintersection
        else:
            assert sorted((p,q,r)) in ([0,32,32],[16,16,32])
            logs=sorted((a.bit_length()-1 for a in (p,q,r) if a),reverse=True)
            assert logs[0]+logs[1]-7>=2
    for w in (96,112,120):assert w-64>=32
    assert 7+8-5+1==11
    # Final three first derivatives: average<272 and no allowed256..272interior.
    assert 128+Fraction(2,3)*206<272
    print('PASS: all bootstrap arithmetic, ALL hyperplanes/Pluecker vectors,')
    print('ALL fibers throughdim4, ambient exterior bound, triple256 cases, and final gaps.')

if __name__=='__main__':verify()
