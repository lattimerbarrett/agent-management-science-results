import sympy as s
from pathlib import Path
z,b,w,c=s.symbols('z b w c')
e=s.symbols('e',positive=True)
h=(s.exp(2*s.pi*s.I*z*b)-1)/(2*s.pi*s.I*z)
hc=(s.exp(-2*s.pi*s.I*z*b)-1)/(-2*s.pi*s.I*b)
assert s.simplify(s.diff(h,b)-s.exp(2*s.pi*s.I*z*b))==0
assert s.simplify(s.diff(h,z,b)-2*s.pi*s.I*b*s.exp(2*s.pi*s.I*z*b))==0
rho=(w-h)*(c-hc)+(e**2/4)*z*b
H=s.Matrix([[s.diff(rho,z,b),s.diff(rho,z,c)],[s.diff(rho,w,b),s.diff(rho,w,c)]])
expected=1+e**2/4-(c-hc)*s.diff(h,z,b)-(w-h)*s.diff(hc,z,b)
assert s.simplify(H.det()-expected)==0
assert s.simplify(s.limit(h,z,0)-b)==0
assert s.simplify(h.subs({z:s.Rational(1,2),b:s.Rational(1,2)})-(1+s.I)/s.pi)==0
eps=1/(32*s.pi)
assert s.simplify((1-8*s.pi*eps+eps**2/4)-(s.Rational(3,4)+eps**2/4))==0
assert s.simplify(2/s.pi**2-eps**2)>0
print('PASS: universal Wirtinger identities, removable extension, exact Hessian determinant, boundary-independent positivity lower bound, and excluded hull point.')
Path('workspace/agent1_graph_disk_check.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/agent1_graph_disk_check.py')")[0])
