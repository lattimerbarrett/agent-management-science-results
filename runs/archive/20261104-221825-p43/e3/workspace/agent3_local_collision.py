import sympy as s
from pathlib import Path
z,w,mu=s.symbols('z w mu')
x,y,u,v=s.symbols('x y u v', real=True)
H=s.re((x+s.I*y)**4-mu*(x+s.I*y)**2).expand(complex=True)
# Use real parameter explicitly.
mu=s.symbols('mu', real=True)
H=s.expand(s.re((x+s.I*y)**4-mu*(x+s.I*y)**2)+(u*u-v*v))
assert H == x**4-6*x*x*y*y+y**4-mu*x*x+mu*y*y+u*u-v*v
assert s.expand(H.subs({x:-x,y:-y,u:-u,v:-v})-H)==0
grad=s.Matrix([s.diff(H,t) for t in (x,y,u,v)])
assert grad == s.Matrix([4*x**3-12*x*y*y-2*mu*x,4*y**3-12*x*x*y+2*mu*y,2*u,-2*v])
# For mu>0, solutions are origin and two real-axis points.
# Orthogonal branch x=0 instead gives y^2=-mu/2, impossible over reals.
# x,y both nonzero yields 2x²-6y²=mu and 2y²-6x²=-mu,
# hence x²+y²=0, impossible.
a=s.symbols('a', positive=True)
hess=s.hessian(H,(x,y,u,v))
for xx in [0,a,-a]:
    hh=s.simplify(hess.subs({mu:2*a*a,x:xx,y:0,u:0,v:0}))
    assert s.det(hh)>0
# At mu=0 gradient planar quartic is 4 conjugate(z)^3,
# and planar w quadratic is 2 conjugate(w), degrees -3 and -1.
# Their direct-product Brouwer degree is +3.
print('Even quartic local Hamiltonian verified:', H)
print('For mu>0: three nondegenerate critical points, all gradient index +1.')
print('For mu=0: unique critical point; gradient degree (-3)*(-1)=3.')
print('This checks only a local collision model; NOT a global S2xS2 construction.')
Path('workspace/agent3_local_collision.py').write_text(Path('scratchpad.py').read_text())
