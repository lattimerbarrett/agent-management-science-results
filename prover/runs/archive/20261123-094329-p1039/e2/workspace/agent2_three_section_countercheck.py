"""Entire function with arbitrarily many affine sections and disconnected zero fiber.
Explicit r=3 check; the general formula is given in the adjacent proof text.
"""
import sympy as s
z,w=s.symbols('z w')
roots=[-1,0,1]
P=z**3-z
L=s.Rational(3,2)*z**2-1
B=s.exp(s.I*s.pi+(-s.log(2)-s.I*s.pi)*z**2)
W=w+L
f=z-P*W
factors=[s.cancel(P/(z-a))*W-1 for a in roots]
g=B*s.prod(factors)
for a in roots:
    assert s.simplify(f.subs(z,a)-a)==0
    assert s.simplify(g.subs(z,a)-w)==0
    assert s.simplify(s.diff(f,z).subs({z:a,w:0}))==0
# Polynomial identity explains f restricted to the jth component is constant a_j.
for a,Fj in zip(roots,factors):
    assert s.expand((z-a)*Fj+(f-a))==0
# Distinct zero components cannot meet: the two factor ideals contain1.
for i in range(3):
    for j in range(i):
        G=s.groebner([factors[i],factors[j]],w,z)
        assert list(G)==[1]
print('Verified: f(a,w)=a, g(a,w)=w for a=-1,0,1; g^-1(0) has3 disjoint graph components.')
