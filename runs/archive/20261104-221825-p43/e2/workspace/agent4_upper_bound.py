import sympy as s
from pathlib import Path
x,y,z,a,b,c=s.symbols('x y z a b c', real=True)
p=s.Matrix([x,y,z]); v=s.Matrix([a,b,c]); X=s.Matrix([-y,x,0])
# Given x.v=0 and |x|^2=1, omega(X,v) = dz(v).
omega=s.expand(p.dot(X.cross(v)))
identity=s.expand(omega-c - (c*(x*x+y*y+z*z-1)-z*(x*a+y*b+z*c)))
assert identity == 0
# Choose angular speed pi: the time-one map is the half-turn.
R=s.diag(-1,-1,1)
assert R.T*R == s.eye(3)
assert R.det()==1
# Fixed-point ideal on one sphere: x=y=0 and z^2=1.
G=s.groebner(list((R-s.eye(3))*p)+[p.dot(p)-1],x,y,z)
assert list(G)==[x,y,z**2-1]
solutions=s.solve(list(G),(x,y,z))
assert set(solutions)=={(0,0,-1),(0,0,1)}
fixed=[(u,v) for u in solutions for v in solutions]
assert len(fixed)==4
# Tangent maps at poles are -I_2, hence no eigenvalue 1 (optional).
assert (s.diag(-1,-1)-s.eye(2)).det()==4
print('omega(X_z,v)-dz(v) vanishes modulo sphere/tangency constraints:',identity==0)
print('One-factor fixed ideal Groebner basis:',list(G))
print('Product fixed points:',fixed)
Path('workspace/agent4_upper_bound.py').write_text(Path('scratchpad.py').read_text())
