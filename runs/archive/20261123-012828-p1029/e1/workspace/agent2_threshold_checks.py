from fractions import Fraction
from pathlib import Path
import sympy as sp

# Exact scalar checks for the spectral-threshold reduction.
e = sp.symbols('eta', positive=True)
t = e/2
d = e/(2-e)
assert sp.simplify(t+(1-t)*d-e) == 0
assert sp.simplify(d-e/2-e**2/(2*(2-e))) == 0
# For eta>1, tau(b)<=||b||<=1 already excludes the increment.
for denominator in range(1, 101):
    for numerator in range(1, denominator+1):
        eta=Fraction(numerator,denominator)
        threshold=eta/2
        dimlower=eta/(2-eta)
        assert threshold+(1-threshold)*dimlower==eta
        assert dimlower>=eta/2
        assert (2/eta)*threshold==1
print('Exact symbolic identities and 5050 rational parameter cases passed.')

# Noncommuting rational positive increments with a bounded total.
I=sp.eye(2)
b0=sp.Matrix([[1,0],[0,0]])/4
b1=sp.Matrix([[1,1],[1,1]])/8
b2=I/8
B=[b0,b1,b2]
def psd(A):
    assert A==A.T.conjugate()
    assert all(v>=0 for v in A.eigenvals())
for b in B: psd(b)
psd(I-sum(B,sp.zeros(2)))
# Every sign sum is in [-I,I] exactly, even though b0,b1 do not commute.
from itertools import product
for signs in product([-1,1],repeat=len(B)):
    S=sum((s*b for s,b in zip(signs,B)),sp.zeros(2))
    psd(I-S);psd(I+S)
assert b0*b1 != b1*b0
print('Eight exact noncommuting rational sign-sum tests passed.')
# All computations above are self-contained; this script writes no files.
