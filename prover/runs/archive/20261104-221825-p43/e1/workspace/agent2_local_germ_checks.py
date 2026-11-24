import sympy as s
from pathlib import Path
x,y,u,v,a=s.symbols('x y u v a', real=True)
f=x**3-3*x*y**2+u**2-v**2-3*a**2*x
grad=s.Matrix([s.diff(f,t) for t in (x,y,u,v)])
assert grad == s.Matrix([3*x*x-3*y*y-3*a*a,-6*x*y,2*u,-2*v])
for sign in [-1,1]:
    p={x:sign*a,y:0,u:0,v:0}
    assert grad.subs(p)==s.zeros(4,1)
    h=s.hessian(f,(x,y,u,v)).subs(p)
    assert h==s.diag(6*sign*a,-6*sign*a,2,-2)
    assert s.simplify(h.det()-144*a*a)==0
# At a=0 the first two gradient equations imply x=y=0 over reals:
# xy=0, x²=y², hence x²+y²=0.
# Planar gradient on the unit circle is 3(cos2t,-sin2t), winding -2.
t=s.symbols('t',real=True)
planar=grad[:2,0].subs({a:0,x:s.cos(t),y:s.sin(t)})
assert s.trigsimp(planar[0]-3*s.cos(2*t))==0
assert s.trigsimp(planar[1]+3*s.sin(2*t))==0
assert s.diag(2,-2).det()==-4
print('Verified gradient equations, two index-2 perturbation criticals, and isolated germ index (-2)*(-1)=+2.')
# Generic capsule field (all signs handled by explicitly stated inequalities).
q, vv, ss, tt, eps = s.symbols('q vv ss tt eps', real=True)
A=s.Function('A')(q)
d=s.Function('d')(q)
aa=-eps*A*s.diff(d,q)
bb=1+eps*s.diff(A,q)*s.diff(d,q)
h=A*vv+ss*tt
D=d+vv**2+ss**2+tt**2
Y=s.Matrix([aa,bb*vv,ss/2,tt/2])
variables=(q,vv,ss,tt)
Yh=sum(Y[i]*s.diff(h,variables[i]) for i in range(4))
YD=sum(Y[i]*s.diff(D,variables[i]) for i in range(4))
assert s.simplify(Yh-h)==0
expected=-eps*A*s.diff(d,q)**2+2*bb*vv**2+ss**2+tt**2
assert s.simplify(YD-expected)==0
# Radial flattening: chi>=0 and chi'<=0 imply psi'>0.
r=s.symbols('r', positive=True)
chi=s.Function('chi')(r)
psi=r*s.exp(-chi/r**2)
assert s.simplify(s.diff(psi,r)/psi-(1/r-s.diff(chi,r)/r**2+2*chi/r**3))==0
# In the flat region chi=1, verify several derivatives vanish at the origin.
for k in range(9):
    assert s.limit(s.diff(r*s.exp(-1/r**2),r,k),r,0,dir='+')==0
print('Verified generic capsule Yh=h and positive-sum YD identity; radial flattening derivative and flatness through order 8.')
Path('workspace/agent2_local_germ_checks.py').write_text(Path(__file__).read_text())
