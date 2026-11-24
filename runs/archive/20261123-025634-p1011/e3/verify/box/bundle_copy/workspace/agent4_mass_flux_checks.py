"""Exact checks of the LINEAR compensated Green/ADM flux coefficients.
Not a proof of the nonlinear low-dimensional blow-up expansion.
"""
import sympy as s
n,d,r,t,A,B=s.symbols('n d r t A B', positive=True)
a=(n-2)/2;b=(n-2)/(2*(n-1));C=4*(n-1)/(n-2)
assert s.simplify(C*b-2)==0
# Fundamental plus radial correction: sphere angular integrals factored out.
G=r**(2-n)+t*r**B
Pr=s.expand(a*G*s.diff(G,r)+r*s.diff(G,r)**2/2)*r**(n-1)
linear=s.expand(Pr).coeff(t,1)
expected=-a*(B+n-2)*r**B
assert s.simplify(linear-expected)==0
# Kelvin mass derivative of w=1+t*R^{-B-n+2} gives exactly P/a.
R=s.symbols('R', positive=True)
w=1+t*R**(-B-n+2)
kelvinflux=s.diff(w,R)*R**(n-1)
assert s.simplify(linear-a*kelvinflux.coeff(t,1).subs(R,1/r))==0
# Radial graph h=t*r^d has Kelvin F=t*R^(2-d).
# Exact mean correction coefficient computed by the hemisphere angular equation.
beta=d+1-n
mean_phi=(n-2)*(d-2)/(2*(n-1)*(d-1))
raw_cross=-a*(beta+n-2)*mean_phi*r**beta
edge_kelvin=s.diff(R**(2-d),R)*R**(n-2)
assert s.simplify(raw_cross-a*b*edge_kelvin.subs(R,1/r))==0
print('PASS: C*b=2, raw Green/Kelvin flux identity, and radial linear-shape counterterm cancellation, all dimensions symbolically.')
