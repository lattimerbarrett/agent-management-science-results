"""Exact checks for elementary boundary Yamabe identities.
These checks do NOT prove compactness or the dimension 20/21 threshold.
"""
import sympy as s
from pathlib import Path
n=s.symbols('n', integer=True, positive=True)
r, lam, t, z=s.symbols('r lam t z', positive=True)
a=(n-2)/2
c=(n-2)/(4*(n-1))
U=(lam/(lam**2+r**2))**a
p=(n+2)/(n-2)
# For radial powers avoid symbolic complex-power ambiguity by factoring U.
logder=-(n-2)*r/(lam**2+r**2)
laplacian_over_U=s.diff(logder,r)+logder**2+(n-1)*logder/r
nonlinearity_over_U=n*(n-2)*lam**2/(lam**2+r**2)**2
assert s.factor(laplacian_over_U+nonlinearity_over_U)==0
# Bubble centered at t e_1 on unit ball. On the boundary x_1=z,
# lambda^2=1-t^2. H=n-1 and B=d_nu+(n-2)/2.
D=lam**2+1-2*t*z+t**2
normal_logder=-(n-2)*(1-t*z)/D
assert s.factor((normal_logder+2*c*(n-1)).subs(lam**2,1-t**2))==0
# The maximum boundary value occurs at e_1 and blows up t -> 1.
base_sq=s.factor((1-t**2)/(2*(1-t))**2)
assert s.factor(base_sq-(1+t)/(4*(1-t)))==0
assert s.limit(base_sq,t,1,dir='-')==s.oo
# Scalar curvature normalization of the PDE.
assert s.factor((1/c)*n*(n-2)-4*n*(n-1))==0
# Constant on unit hemisphere: u^(4/(n-2))=1/4.
assert s.factor(-c*n*(n-1)+n*(n-2)/4)==0
# Ellipsoid F=sum x_j^2/a_j^2-1. At x=a_1 e_1,
# outward principal curvatures k_j=a_1/a_j^2, j>=2.
# Axes (1,2,1,...,1) give unequal curvatures 1/4 and 1.
assert s.Rational(1,4)!=1
# Explicit radial PDE and Robin checks in integer dimensions, without
# symbolic assumptions for nonlinear powers.
for dim in range(3,41):
    exponent=s.Rational(dim-2,2)
    A=s.symbols('A', positive=True)
    u=(A/(A**2+r**2))**exponent
    lap=s.diff(u,r,2)+(dim-1)*s.diff(u,r)/r
    power_over_u=(A/(A**2+r**2))**2
    assert s.simplify(lap/u+dim*(dim-2)*power_over_u)==0
print('PASS: symbolic radial bubble PDE for general n; explicit n=3,...,40.')
print('PASS: exact unit-ball Robin condition lambda^2+|center|^2=1.')
print('PASS: boundary maximum diverges as center tends to unit sphere.')
print('PASS: scalar curvature normalization is 4*n*(n-1).')
print('PASS: unit round hemisphere constant is 2^{-(n-2)/2}.')
print('No compactness or sharp dimension-threshold claim is checked here.')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_elementary_checks.py').write_text(Path(__file__).read_text())
