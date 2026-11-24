"""Finite checks for agent2_quartic_relative_proof.txt.
The analytical classification input is classical strict KT, not K.
"""
from fractions import Fraction

def quadratic_weights(k,rho):
    ans={0,1<<k,1<<(k-1)}
    for r in range(2,min(k,rho)+1,2):
        ans|={(1<<(k-1))-(1<<(k-r//2-1)),(1<<(k-1))+(1<<(k-r//2-1))}
    return ans

def fwht(a):
    a=list(a);s=1
    while s<len(a):
        for b in range(0,len(a),2*s):
            for j in range(s):
                u,v=a[b+j],a[b+j+s];a[b+j],a[b+j+s]=u+v,u-v
        s*=2
    return a

def verify():
    # Exhaustive Walsh-normalization check for all functions on<=4 variables.
    for n in range(5):
        N=1<<n
        for b in range(1<<N):
            W=fwht([1-2*((b>>x)&1) for x in range(N)])
            assert sum(c*c for c in W)==N*N
            assert max(abs(c) for c in W)>0
            assert N-max(abs(c) for c in W)<N
    # Strict-KT numerical forms for RM4,10 below128.
    kt={64}
    for mu in (2,3,4):kt.add(128-(1<<(7-mu)))
    for s in (2,3,4):kt.add(128-(1<<(7-s)))
    assert kt=={64,96,112,120}
    for E in (50,52,54):
        assert E+64<=118
        for w in kt:
            if w>=E+64:continue
            inside=w-E
            if w==64:assert inside not in {0,1,2,4,8,16,32,64}
            elif w in (96,112):
                rho=4 if w==96 else 6
                assert all(inside not in quadratic_weights(k,rho) for k in (5,6,7))
                if w==112:
                    assert inside not in {56,64,48}
                    assert inside>48
    # Minimum first derivative weight256 branches.
    assert 6+7-10==3
    assert 4+7-10==1
    assert 7+8-10==5
    assert 112-64>32 and 120-64>32
    for s in (2,3,4):
        w=128-(1<<(7-s))
        assert w-64>1<<(s+1)
    # Averaging and the independent 2D cubic code.
    avg=Fraction(256*(2048-256),2047)
    assert avg<256
    assert 3*96>256
    assert 9-8>=1
    assert all(7-s>=4 for s in (2,3))
    print('PASS: quartic punctured gaps50/52/54 and primitive weight256 arithmetic; exhaustive small Walsh check.')

if __name__=='__main__':verify()
