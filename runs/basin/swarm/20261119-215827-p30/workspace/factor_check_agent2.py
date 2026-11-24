"""Exact exhaustive checks of complementary-factor orthogonality.
Requires SageMath, available as a Python package in the problem environment.
The general proof uses the reciprocal-conjugate identity, not enumeration.
"""
from itertools import combinations
from sage.all import CyclotomicField, PolynomialRing

def check_factors(k):
    assert k >= 1
    K = CyclotomicField(4*k)
    zeta = K.gen()
    R = PolynomialRing(K, 'z')
    z = R.gen()
    roots = [zeta**(2*r+1) for r in range(2*k)]
    U = z**(2*k)+1
    count = 0
    for subset in combinations(range(2*k), k):
        chosen = set(subset)
        p = R.one()
        q = R.one()
        for r,root in enumerate(roots):
            if r in chosen:
                p *= z-root
            else:
                q *= z-root
        assert p*q == U
        qstar = R([q[k-i].conjugate() for i in range(k+1)])
        assert qstar == q[0].conjugate()*q
        inner = sum(p[i]*q[i].conjugate() for i in range(k+1))
        assert (p*qstar)[k] == inner == 0
        count += 1
    return count

if __name__ == '__main__':
    for k in (1,2,3,7):
        print('k =',k,'balanced factorizations checked =',check_factors(k))
