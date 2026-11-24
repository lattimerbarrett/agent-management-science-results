"""Formal noncommutative leading-order check for the square-inequality obstruction.
K is skew adjoint upon interpreting w=z*, and U=exp(sK).
Only the coefficients through s^0 in U diag(1/s+a,0) U* matter.
"""
import sympy as sp
s=sp.Symbol('s', real=True)
a,b,z,w=sp.symbols('a b z w', commutative=False)
I=sp.eye(2)
K=sp.Matrix([[0,-z],[w,0]])
U=I+s*K+s**2*K*K/2
V=I-s*K+s**2*K*K/2
A=U*sp.diag(1/s+a,0)*V
B=sp.diag(0,1/s+b)
H=sp.Matrix([[a,z],[w,b]])
R=A+B-I/s-H
for x in R:
    x=sp.expand(x)
    # Multiplication by s clears all Laurent denominators; the result
    # must have no terms below s^2, i.e. R=O(s).
    p=sp.expand(s*x)
    assert p.coeff(s,0)==0
    assert p.coeff(s,1)==0
print('8 exact noncommutative leading-coefficient assertions passed')
