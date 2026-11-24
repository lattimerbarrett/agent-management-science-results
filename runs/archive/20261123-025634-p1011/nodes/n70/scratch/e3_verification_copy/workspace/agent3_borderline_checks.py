"""Exact coefficient checks for the borderline even-dimensional shape model.
This is NOT a uniform nonlinear blow-up expansion.
"""
import sympy as s
d,j=s.symbols('d j',real=True)
n=2*d
# Delta(P_ell r^(2j))=2j(2ell+2j+n-3) P_ell r^(2j-2)
ell=d-2*j
c=s.expand(1-d+j*(2*ell+2*j+n-3)/(n-1))
assert s.simplify(c-(1-d+j*(4*d-2*j-3)/(2*d-1)))==0
f=lambda x:x*(4*d-2*x-3)
# On 0<=j<=d/2 and d>2, f is increasing and f(j)<=f(d/2).
assert s.simplify(s.diff(f(j),j).subs(j,d/2)-(2*d-3))==0
assert s.factor((d-1)*(2*d-1)-f(d/2))==(d-2)*(d-1)/2
assert s.simplify(c.subs({d:2,j:1}))==0
assert s.simplify(c.subs({d:2,j:0}))==-1
# V=r^(1-d) phi, n=2d: Laplacian angular coefficient is -(d-1)^2.
power=1-d
assert s.expand(power*(power+n-2)+(d-1)**2)==0
# Dirichlet-energy radial exponent is -1, potential-energy exponent -3.
assert s.expand(2*(power-1)+(n-1))==-1
assert s.expand(2*power-4+(n-1))==-3
print('Borderline shape forcing nonzero except radial quadratic gauge; positive logarithmic energy exponents checked.')
