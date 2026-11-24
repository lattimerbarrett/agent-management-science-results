import sympy as s
from pathlib import Path

# Exact symbolic checks for the conformal normalization and Euclidean bubbles.
n=s.symbols('n', integer=True, positive=True)
a=(n-2)/2
c=(n-2)/(4*(n-1))
r,lam,R=s.symbols('r lam R', positive=True)
U=(lam/(lam**2+r**2))**a
lap=s.diff(U,r,2)+(n-1)*s.diff(U,r)/r
bubble_res=s.simplify((lap+n*(n-2)*U*(lam/(lam**2+r**2))**2)/U)
assert bubble_res==0
# Scalar curvature transformation: R_h=-c^-1 u^-p L_g u.
assert s.simplify(n*(n-2)/c-4*n*(n-1))==0
# Robin operator on the sphere r=R, whose trace H=(n-1)/R.
robin_ratio=s.factor((s.diff(U,r)+2*c*(n-1)/r*U)/U)
assert s.simplify(robin_ratio-(n-2)*(lam**2-r**2)/(2*r*(lam**2+r**2)))==0
# The centered bubble satisfies Robin on r=R iff lam=R.
assert s.simplify(robin_ratio.subs(r,R).subs(lam,R))==0
# Off-center bubbles on the unit ball: eps^2+|xi|^2=1.
# Let z=x dot xi and b=|xi|^2. At |x|=1,
# (partial_nu U)/U=-(n-2)*(1-z)/(eps^2+1+b-2*z).
eps,b,z=s.symbols('eps b z', positive=True)
ball_res=-(n-2)*(1-z)/(eps**2+1+b-2*z)+(n-2)/2
assert s.simplify(ball_res.subs(b,1-eps**2))==0
# Explicit maximal boundary bubble value for xi=t e1, eps=sqrt(1-t^2).
t=s.symbols('t', positive=True)
base=s.sqrt(1-t**2)/((1-t**2)+(1-t)**2)
assert s.simplify(base**2-(1+t)/(4*(1-t)))==0
# Conformal normal, mean curvature, and product derivatives: t=log(phi).
# N=nu(phi)/phi. H_h=phi^-2/(n-2) [H+2(n-1)/(n-2)*N].
N,H,v,dv,phi=s.symbols('N H v dv phi', real=True)
left=dv+2*c*(H+2*(n-1)/(n-2)*N)*v
right=dv+N*v+2*c*H*v
assert s.simplify(left-right)==0
# Bulk conformal covariance, using Delta_h v=phi^-4/(n-2)
# [Delta_g v + 2 phi^-1 grad(phi).grad(v)].
Dphi,Dv,G,Rg=s.symbols('Dphi Dv G Rg')
left_bulk=Dv+2*G/phi-c*(Rg-Dphi/(c*phi))*v
right_bulk=(phi*Dv+v*Dphi+2*G-c*Rg*phi*v)/phi
assert s.simplify(left_bulk-right_bulk)==0
results={
'bubble_residual':str(bubble_res),
'round_scalar_curvature':str(s.factor(n*(n-2)/c)),
'ball_robin_ratio':str(robin_ratio),
'boundary_covariance_residual':str(s.simplify(left-right)),
'bulk_covariance_residual':str(s.simplify(left_bulk-right_bulk)),
}
print(results)
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_normalization_checks.py').write_text(Path('scratchpad.py').read_text())
