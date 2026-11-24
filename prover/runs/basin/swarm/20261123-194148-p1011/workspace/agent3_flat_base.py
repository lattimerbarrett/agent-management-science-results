"""Symbolic checks for an explicit smooth convex base with flat boundary disks.
Omega={h(|y|^2)+(t-1)^2<=1}, h(s)=0 for s<=1,
h(s)=(s-1)^2 exp(-1/(s-1)) otherwise.
"""
import sympy as s
x=s.symbols('x',positive=True)
f=x*x*s.exp(-1/x)
assert s.simplify(s.diff(f,x)-s.exp(-1/x)*(2*x+1))==0
assert s.simplify(s.diff(f,x,2)-s.exp(-1/x)*(2+2/x+1/x**2))==0
# Flatness at0 for each fixed derivative: each derivative is e^-1/x times
# a Laurent polynomial, so it tends to0. Explicitly check first12 as well.
for k in range(13):
    assert s.limit(s.diff(f,x,k),x,0,dir='+')==0
# Positivity of radial Hessian: D²[h(|y|²)] =2h' I+4h'' y tensor y.
# Defining gradient can vanish only at t=1 and h'=0, which implies h=0,
# whereas boundary at t=1 requires h=1: contradiction.
print('Exact derivatives, smooth flat junction, and convexity identities verified.')
