"""Exact F_2 Euler polynomial certificate for the two-hyperplane upper bound.
All coefficients are computed, not presumed. Run this file directly for checks.
"""
from math import comb

def truncated_euler_polynomial(j, d):
    # (x*y*(x+y))**j in F2[x,y]/(x**(d+1), y**(d+1)).
    # Frobenius: (x+y)**j = product_{bit k of j}(x**(2**k)+y**(2**k)).
    support = {(j,j)}
    bit = 1
    remaining = j
    while remaining:
        if remaining & 1:
            new = set()
            for a,b in support:
                for monomial in ((a+bit,b), (a,b+bit)):
                    if monomial[0] <= d and monomial[1] <= d:
                        if monomial in new:
                            new.remove(monomial)
                        else:
                            new.add(monomial)
            support = new
        remaining >>= 1
        bit <<= 1
    return support

def upper_certificate(s):
    assert s >= 3
    m = (1 << (s-1))-1
    j, d = 2*m, 3*m+1
    k=m-1
    assert k & ~j == 0 # Lucas criterion; all bits of k occur in j.
    assert (j+k,2*j-k)==(d-2,d)
    assert (j-k, j+k) == (m+1,3*m-1)
    support=truncated_euler_polynomial(j,d)
    assert support == {(d-2,d),(d,d-2)}
    # At one dimension lower, this particular Euler obstruction vanishes.
    assert not truncated_euler_polynomial(j,d-1)
    if s <= 12:
        assert comb(j,k) % 2 == 1
        direct={(j+i,2*j-i) for i in range(j+1)
                if comb(j,i)%2 and j+i<=d and 2*j-i<=d}
        assert direct == support
    return j,d,support

if __name__ == '__main__':
    for s in range(3,15):
        print(s, upper_certificate(s))
