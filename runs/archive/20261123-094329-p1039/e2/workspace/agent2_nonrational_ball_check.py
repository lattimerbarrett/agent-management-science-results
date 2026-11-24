"""Checked explicit strongly pseudoconvex non-rationally-convex balls.
This does NOT prove that their complements are non-Oka.
"""
import sympy as s
from fractions import Fraction as Q
z,b,A=s.symbols('z b A', nonzero=True)
h=(s.exp(s.I*A*z*b)-1)/(s.I*A*z)
assert s.simplify(s.diff(h,b)-s.exp(s.I*A*z*b))==0
assert s.simplify(s.diff(h,z,b)-s.I*A*b*s.exp(s.I*A*z*b))==0
# Smoothness at zero from globally convergent series:
# h=bar(z) sum_{k>=0} (i A |z|²)^k/(k+1)!
t=s.symbols('t')
assert s.limit((s.exp(s.I*A*t)-1)/(s.I*A*t),t,0)==1
# At a graph point q=|w-h|² the Levi matrix has determinant |h_barz|²=1.
a,c=s.symbols('a c',real=True)
B=s.Matrix([[a*a+c*c+1,-a-s.I*c],[-a+s.I*c,1]])
assert s.simplify(B.det())==1
# For R=2, A=2pi<7: |h_z|<=A R²/2<14, trace B<198.
# Thus lambda_min(B)>1/198.
# On |w-h|<=epsilon, the sole zz correction has norm<=2 epsilon A R<28 epsilon.
epsilon=Q(1,10000)
assert 28*epsilon < Q(1,198)
# rho = |w-h(z)|² + sum(Im u)² + delta (|z|²+sum(Re u)²)-epsilon².
# Here delta=epsilon²/R² and every rho<=0 has |z|<=R, |w-h|<=epsilon.
delta=epsilon**2/4
assert delta < epsilon**2
# p=(1/2,0,0) has |h(1/2)|²=2/pi² > 2/(22/7)².
assert 2/Q(22,7)**2 + delta/4-epsilon**2 > 0
print('Exact graph derivative, Levi determinant and strict-Levi margin checks passed.')
print('epsilon=',epsilon,'delta=',delta,'Levi lower bound >',Q(1,198)-28*epsilon)
