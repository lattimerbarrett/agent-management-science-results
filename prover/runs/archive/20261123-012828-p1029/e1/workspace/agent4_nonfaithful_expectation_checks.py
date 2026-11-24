import sympy as s
from pathlib import Path
plus=s.ones(2)/2
I2=s.eye(2)
L=6
def tensor(xs):
    a=s.ones(1)
    for b in xs:a=s.kronecker_product(a,b)
    return a
Q={n:tensor([plus if n<j<=2*n else I2 for j in range(1,L+1)]) for n in range(1,4)}
I=s.eye(2**L)
for n,q in Q.items():
    assert q*q==q
    assert all(q[j,j]==s.Rational(1,2**n) for j in range(2**L))
    assert s.trace(q)/2**L==s.Rational(1,2**n)
    # A first-n-coordinate diagonal generator commutes with q_n.
    Z=tensor([s.diag(1,-1) if j==n else I2 for j in range(1,L+1)])
    assert Z*q==q*Z
r=I-(I-Q[2])*(I-Q[3])
assert r*r==r
assert s.trace(r)/2**L==s.Rational(5,16)
assert s.trace(I-r)/2**L==s.Rational(11,16)
for n in [2,3]:
    assert 2**n*s.trace(Q[n]*r)/2**L==1
print('Exact 64x64 tensor checks passed; finite join trace=5/16, complement=11/16')
