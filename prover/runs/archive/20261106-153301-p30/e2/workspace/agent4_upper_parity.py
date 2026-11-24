"""Exact parity certificates for the two-hyperplane upper bound.
No inference of a matching lower bound is made.
"""
from math import comb

def parity_binom(n,k):
    return int(0 <= k <= n and (k & ~n)==0)

def certify_symbolic_parameters(s):
    assert s >= 3
    n=1 << (s-1)
    j,d=2*n-2,3*n-2
    k=n-2
    assert j+k==d-2 and 2*j-k==d
    assert parity_binom(j,k)==1
    # All monomials potentially surviving at d have k in [n-2,n].
    assert 2*j-d == n-2 and d-j == n
    assert [k for k in range(n-2,n+1) if parity_binom(j,k)] == [n-2,n]
    # In dimension d-1 there is only k=n-1, which is odd.
    assert parity_binom(j,n-1)==0
    return j,d

def direct_expand(s):
    n=1 << (s-1)
    j,d=2*n-2,3*n-2
    out={(j+k,2*j-k):comb(j,k)%2 for k in range(j+1)}
    reduced={p:c for p,c in out.items() if c and max(p)<=d}
    assert reduced=={(d-2,d):1,(d,d-2):1}
    assert not any(c and max(p)<d for p,c in out.items())
    return reduced

if __name__ == '__main__':
    for s in range(3,21):
        j,d=certify_symbolic_parameters(s)
        if s<=10:
            direct_expand(s)
        print(f's={s}, j={j}, d={d}: certified nonzero Euler class')
