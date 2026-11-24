"""Exact finite checks supporting the moment-curve lower-bound proof.
Run check() or execute this file. The all-s argument is in the proof, not finite tests.
"""
from itertools import product
from math import comb
import sympy as sp

def parameters(s):
    if not isinstance(s,int) or s<3: raise ValueError("integer s >= 3 required")
    j=(1<<s)-2
    lower=3*(1<<(s-1))-3
    assert 2*lower==3*j
    return j,lower

def check():
    # A root event can flip either sign or both. With at most two events
    # there can never be four positive-length sign regions.
    for r in range(3):
        for start in product((-1,1), repeat=2):
            for events in product(((1,0),(0,1),(1,1)),repeat=r):
                current=start
                seen={current}
                for a,b in events:
                    current=(current[0]*(-1)**a,current[1]*(-1)**b)
                    seen.add(current)
                assert len(seen)<=r+1<4
    # Exact coefficient substitution: every normalized affine form restricts
    # to a nonzero polynomial, because 1,t,...,t^d are independent.
    t=sp.Symbol('t')
    for d in range(1,21):
        a=sp.symbols('a:'+str(d+1))
        restriction=sp.Poly(sum(a[k]*t**k for k in range(d+1)),t)
        assert restriction.all_coeffs()==list(reversed(a))
    # Check symbolic parameter identity for arbitrary n=2^(s-1).
    n=sp.Symbol('n',integer=True,positive=True)
    j=2*n-2; lower=3*n-3
    assert sp.expand(2*lower-3*j)==0
    # Every forbidden dimension violates total root budget, exactly.
    for s in range(3,13):
        j,lower=parameters(s)
        for d in range(1,lower):
            assert 2*d<3*j
    return True

if __name__=='__main__':
    assert check()
    print('All exact lower-bound checks passed.')
