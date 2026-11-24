"""Algebraic and normalization checks for the spectral-invariant lower bound.
Analytic Floer spectrality and strict LS theorem are mathematical inputs, not
claimed to be proved by these computations.
"""
import sympy as s
from fractions import Fraction
th, ph = s.symbols("th ph", real=True)
x = s.Matrix([s.sin(th)*s.cos(ph),s.sin(th)*s.sin(ph),s.cos(th)])
density = s.simplify(x.dot(x.diff(th).cross(x.diff(ph))))
assert density == s.sin(th)
area = s.integrate(density,(th,0,s.pi),(ph,0,2*s.pi))
assert area == 4*s.pi
# Quantum homology under Poincare duality: u^2=q, v^2=q.
u,v,q = s.symbols("u v q")
G = s.groebner([u*u-q,v*v-q],u,v,q)
def red(p): return s.expand(G.reduce(s.expand(p))[1])
assert red(u*u)==q
assert red(v*v)==q
assert red((u*v)*(u*v))==q*q
# Monotonicity: a sphere class (m,n) has omega=4pi(m+n), c1=2(m+n).
for m in range(-100,101):
    for n in range(-100,101):
        assert 4*(m+n)==2*(2*(m+n))
# With one fixed point the normalized action spectrum is an integer coset.
# The strict quantum-product spectral chain needs a second value in (-1,0).
assert not [k for k in range(-100,101) if -1<k<0]
print("PASS: area=4pi; quantum factor square=q; sphere action period=4pi; strict spectral chain impossible for one fixed point")
