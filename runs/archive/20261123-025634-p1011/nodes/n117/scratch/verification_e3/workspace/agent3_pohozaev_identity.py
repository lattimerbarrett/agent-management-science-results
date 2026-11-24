"""Exact algebra in the Euclidean critical Robin Pohozaev identity.
This verifies the identity, NOT the needed uniform blow-up expansion.
"""
import sympy as s
n=s.symbols('n',positive=True,integer=True)
a=n*(n-2);q=2*n/(n-2);b=(n-2)/(2*(n-1))
# Divergence of stress current plus conformal correction.
G,F=s.symbols('G F') # G=|grad u|^2, F=u^q
assert s.simplify((1-n/2)*G+n*a/q*F+(n-2)/2*(G-a*F))==0
# On Robin boundary, decompose x.grad u = xT.gradT u +(x.nu)du.
H,U,S,T,X,dh=s.symbols('H U S T X dh')
# S=|gradT u|^2, T=xT.gradT u, X=x.nu; du=-bHU.
du=-b*H*U
original=(T+X*du)*du-X*(S+du**2)/2+a/q*X*F+(n-2)/2*U*du
expanded=-b*H*U*T+b*b*H*H*U*U*X/2-X*S/2+a/q*X*F-(n-2)*b*H*U*U/2
assert s.simplify(original-expanded)==0
# Integrate -b/2 H xT.grad(U^2); use divT xT=(n-1)-H X.
integrated=b*s.Rational(1,2)*(dh+(n-1)*H-H*H*X)*U*U+b*b*H*H*U*U*X/2-X*S/2+a/q*X*F-(n-2)*b*H*U*U/2
claimed=b*s.Rational(1,2)*(dh+H+(b-1)*H*H*X)*U*U+X*(a/q*F-S/2)
assert s.simplify(integrated-claimed)==0
print('Critical Euclidean Robin Pohozaev divergence and boundary coefficients checked exactly.')
