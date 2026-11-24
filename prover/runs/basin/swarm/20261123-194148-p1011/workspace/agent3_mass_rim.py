"""Exact radial primitive matching Robin Pohozaev to the boundary ADM rim.
For a general graph replace F by its angular average f; nonconstant
angular modes integrate to zero at linear order. Identity holds on annuli.
"""
import sympy as s
r,n=s.symbols('r n',positive=True)
f=s.Function('f')(r)
beta=(n-2)/(2*(n-1));K=(n-2)**2/(4*(n-1))
H=s.diff(f,r,2)+(n-2)/r*s.diff(f,r)
integrand=beta/2*(H+r*s.diff(H,r))*r**(2-n)-(n-2)**2/2*(r*s.diff(f,r)-f)*r**(-n)
primitive=beta/2*H*r**(3-n)+K*r**(2-n)*(s.diff(f,r)-2*f/r)
assert s.simplify(s.diff(primitive,r)-integrand)==0
# The first primitive term is precisely the tangential Robin rim term.
# Kelvin: R=1/r, b(R)=R^2 f(1/R), so db/dR=-f'(r)+2f(r)/r.
R=s.symbols('R',positive=True)
b=R**2*s.Function('f')(1/R)
assert s.simplify(s.diff(b,R).subs(R,1/r)-(-s.diff(f,r)+2*f/r))==0
print('Exact Robin-linear-bulk primitive and Kelvin rim coefficient verified.')
