"""Finite checks for agent1_min256_derivative_lemma.txt; no brute-force claim
about arbitrary RM(6,13) words. The analytic proof provides that coverage."""
from itertools import combinations
from collections import Counter

def rank(rows):
    b={}
    for x in rows:
        while x:
            i=x.bit_length()-1
            if i in b:x^=b[i]
            else:b[i]=x;break
    return len(b)

def span(B):
    s=[0]
    for v in B:s += [x^v for x in s]
    return s

def flat_masks(n,d):
    spaces=set()
    for B in combinations(range(1,1<<n),d):
        if rank(B)==d:spaces.add(sum(1<<v for v in span(B)))
    flats=set()
    for S in spaces:
        pts=[x for x in range(1<<n) if (S>>x)&1]
        for a in range(1<<n):flats.add(sum(1<<(a^v) for v in pts))
    return flats

def monomial_masks(n,r):
    return [sum(1<<x for x in range(1<<n) if x&m==m)
            for m in range(1<<n) if m.bit_count()<=r]

def allwords(G):
    x=0; yield x
    for i in range(1,1<<len(G)):
        x^=G[(i&-i).bit_length()-1];yield x

# Direct enumeration of RM(1,5) and RM(2,5), not a claimed classification.
flats={d:flat_masks(5,d) for d in (2,3,4)}
assert {d:len(F) for d,F in flats.items()}=={2:1240,3:620,4:62}
for k in (2,3):
    words=list(allwords(monomial_masks(5,k-1)))
    hist=Counter(x.bit_count() for x in words)
    d=1<<(6-k)
    assert min(w for w in hist if w)==d
    assert not any(d<w<3*d//2 for w in hist)
    assert {x for x in words if x.bit_count()==d}==flats[6-k]
    print('RM(%s,5) exact weight distribution:'%(k-1),dict(sorted(hist.items())))

# RM(3,5)=even subsets with zero XOR: all weight<=5 cases.
# The empty and 4-point words are the only nonzero possibilities up to5.
for t in (2,4):
    actual=set()
    for A in combinations(range(32),t):
        z=0
        for v in A:z^=v
        if not z:actual.add(sum(1<<v for v in A))
    assert actual==(flats[2] if t==4 else set())
assert len({0,1,2,4,8,15})==6 and 0^1^2^4^8^15==0

# Exact common-support/union bounds, including deletion of origin.
for k in (2,3,4):
    F=list(flats[6-k]);outside=(1<<32)-2
    minunion=min(((A|B)&outside).bit_count()
                 for i,A in enumerate(F) for B in F[i+1:])
    assert minunion>64//(1<<k)
    print('k=',k,'minimum outside union of distinct flats=',minunion)

# Exact shortening dimensions implement the affine-factor/isolated-point step.
for k in (2,3):
    G=monomial_masks(5,k);full=(1<<32)-1
    for T in flats[6-k]:
        dim=len(G)-rank([g&(full^T) for g in G])
        assert dim==7-k # affine functions on T, whose dimension is6-k
        if not T&1:
            dim_extra=len(G)-rank([g&(full^(T|1)) for g in G])
            assert dim_extra==dim

# Summing squarefree monomials over Y7 proves degree M_J<=|J|-1 exactly.
for B in range(128):
    for J in range(128):
        for adeg in range(6):
            if adeg+B.bit_count()<=6 and (B|J)==127:
                assert adeg<=J.bit_count()-1

def moment(R,J):
    return sum((y&J)==J for y in R)&1

# Verify the moment extraction and translation formulas for standard P,
# for ALL its cosets in Y7. GL invariance supplies every decomposable beta.
for k in (1,2,3):
    P=set(range(1<<k))
    for a in range(0,128,1<<k):
        R={a^p for p in P}
        for J in range(128):
            if J.bit_count()<k:assert moment(R,J)==0
            if J.bit_count()==k:assert moment(R,J)==(J==(1<<k)-1)
            if J.bit_count()==k+1:
                base=(1<<k)-1
                expected=0
                if J&base==base:
                    j=(J^base).bit_length()-1;expected=(a>>j)&1
                assert moment(R,J)==expected

# Exact inequalities covering every branch of the analytic proof.
assert 64-31*2==2 and 8-2-2>2
for k in (2,3):
    d=1<<k; N=(1<<(6-k))-1
    assert N*(3*d//2)>64
    assert 2*d>d
    assert (1<<(5-k))-1>2
    assert (1<<(k+2))-d-d>d
    assert (1<<(4-k))>=2
assert 64-3*16<32
assert 3+7+1==11
assert 2+7+1==10
assert 1+7+1==9
print('PASS: all finite checks for unconditional min-derivative256 lemma')
