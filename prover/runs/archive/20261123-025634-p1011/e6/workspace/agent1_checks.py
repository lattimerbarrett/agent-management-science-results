import sympy as s
from pathlib import Path
n=s.symbols('n', integer=True, positive=True)
r,e,t,q=s.symbols('r e t q', positive=True)
a=(n-2)/2
D=e**2+r**2
# Exact logarithmic radial derivatives of U=(e/D)^a.
logder=-2*a*r/D
lap_ratio=s.factor(s.diff(logder,r)+logder**2+(n-1)*logder/r)
assert s.simplify(lap_ratio+n*(n-2)*e**2/D**2)==0
# At |x|=1, q=|xi|^2 and t=x dot xi.
Db=e**2+1+q-2*t
boundary_ratio=s.factor(-2*a*(1-t)/Db+a)
assert s.simplify(boundary_ratio-a*(e**2+q-1)/Db)==0
# Coefficient identities for conformal change ghat=phi^(4/(n-2)) g.
c=(n-2)/(4*(n-1))
assert s.simplify(2*c*2*(n-1)/(n-2)-1)==0
assert s.simplify(c*4*n*(n-1)-n*(n-2))==0
# Infinitesimal normal deformation of a unit sphere: tracefree shape
# variation is minus tracefree spherical Hessian. Local nonzero TF Hessian
# in dimension m=n-1 for bump z1^2 has eigenvalue difference 2.
for dim in range(3,101):
    m=dim-1
    Hess=s.diag(2,*([0]*(m-1)))
    TF=Hess-s.eye(m)*s.trace(Hess)/m
    assert TF != s.zeros(m)
print('PASS: symbolic bubble interior equation for all symbolic n.')
print('PASS: symbolic Robin residual on the unit ball.')
print('PASS: conformal mean-curvature coefficient and scalar normalization.')
print('PASS: nonumbilic local deformation algebra for n=3,...,100.')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_checks.py').write_text(Path('scratchpad.py').read_text())
