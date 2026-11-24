"""Exact arithmetic verification of the upper-bound Euler polynomial.
The arbitrary-s proof uses (1+t)^(2M-2) = sum_{r=0}^{M-1} t^(2r)
over F_2 when M is a power of two.
"""
from math import comb

def verify(s):
    assert s >= 3
    M = 1 << (s-1)
    j, d = 2*M-2, 3*M-2
    # Product (1+t)^j in F_2[t], represented as an integer bitset.
    polynomial = 1
    for bit in range(j.bit_length()):
        if (j >> bit) & 1:
            polynomial ^= polynomial << (1 << bit)
    expected = sum(1 << (2*r) for r in range(M))
    assert polynomial == expected
    r = M
    xexp, yexp = j+r, 2*j-r
    assert (xexp,yexp)==(d,d-2)
    assert max(xexp,yexp)<=d
    assert (polynomial >> r)&1
    assert comb(j,r)%2 == 1
    # Enumerate all monomials surviving the truncated cohomology ring.
    survivors=[(j+r,2*j-r) for r in range(j+1)
               if ((polynomial>>r)&1) and max(j+r,2*j-r)<=d]
    assert survivors == [(d-2,d),(d,d-2)]
    return j,d,survivors

if __name__=='__main__':
    for s in range(3,13):
        print(s,verify(s))
