import sympy as s
from pathlib import Path
x,y,u,v,d=s.symbols('x y u v d', real=True)
f=x**3-3*x*y**2+u**2-v**2
g=s.Matrix([s.diff(f,z) for z in (x,y,u,v)])
J=g.jacobian((x,y,u,v))
assert g==s.Matrix([3*x*x-3*y*y,-6*x*y,2*u,-2*v])
assert s.solve(list(g),(x,y,u,v))==[(0,0,0,0)]
for sign in (-1,1):
 p={x:sign*d,y:0,u:0,v:0}
 assert g.subs(p)==s.Matrix([3*d*d,0,0,0])
 assert s.factor(J.det().subs(p))==144*d*d
# xy=0 and x²-y²=d² has exactly x=±d,y=0 for d>0.
print('Checked isolated critical point and two positive-Jacobian preimages: local gradient degree +2.')
Path('workspace/agent3_local_index.py').write_text(Path('scratchpad.py').read_text())
# Ordinary cohomology positive-degree ideal: basis a,b,ab, with a²=b²=0.
# Products represented by exponent pairs, zero if either exponent exceeds 1.
from itertools import product
positive=[(1,0),(0,1),(1,1)]
def nonzero_product(factors):
 return all(sum(f[k] for f in factors)<=1 for k in (0,1))
assert any(nonzero_product(fs) for fs in product(positive,repeat=2))
assert not any(nonzero_product(fs) for fs in product(positive,repeat=3))
print('Checked ordinary cup-length exactly 2, hence standard cup-length lower bound only 3.')
# Exact regular connecting arc in the common critical level of z(p)+z(q).
t=s.symbols('t',real=True)
p=s.Matrix([s.sin(t),0,s.cos(t)])
q=s.Matrix([s.sin(t),0,-s.cos(t)])
e3=s.Matrix([0,0,1])
assert s.simplify(p.dot(p)-1)==0 and s.simplify(q.dot(q)-1)==0
assert p[2]+q[2]==0
gp=e3-p[2]*p; gq=e3-q[2]*q
assert s.trigsimp(gp.dot(gp)+gq.dot(gq))==2*s.sin(t)**2
assert p.subs(t,0)==e3 and q.subs(t,0)==-e3
assert p.subs(t,s.pi)==-e3 and q.subs(t,s.pi)==e3
print('Checked connecting arc lies on level zero, endpoints are two saddles, spatial gradient norm²=2 sin²(t)>0 for 0<t<π.')
Path('workspace/agent3_arc_checks.py').write_text(Path('scratchpad.py').read_text())
S,T,Y,Z=s.symbols('S T Y Z',real=True)
A=1+Y**2+(S+T)**2; B=1+Z**2+(T-S)**2
numer=s.expand(2*(S+T)*B+2*(T-S)*A)
print('Height numerator in stereographic straight-arc coordinates:',s.factor(numer))
# Exploratory check only: tangential criticals on an explicit thin ellipsoid.
import numpy as np
from scipy.optimize import root
h=numer/(A*B)
R=s.Rational(6,5); delta=s.Rational(1,5)
E=S*S/R**2+(T*T+Y*Y+Z*Z)/delta**2
lam=s.symbols('lam')
vs=(S,T,Y,Z)
eqs=[s.diff(h,z)-lam*s.diff(E,z) for z in vs]+[E-1]
fun=s.lambdify((*vs,lam),eqs,'numpy')
hfn=s.lambdify(vs,h,'numpy')
roots=[]
rng=np.random.default_rng(2)
for k in range(150):
 p=rng.normal(size=4); p=p/np.linalg.norm(p)*np.array([float(R),float(delta),float(delta),float(delta)])
 sol=root(lambda q:np.array(fun(*q),dtype=float),np.r_[p,0.1])
 if sol.success and np.linalg.norm(fun(*sol.x))<1e-7 and not any(np.linalg.norm(sol.x-r)<1e-4 for r in roots):roots.append(sol.x)
print('EXPLORATORY ellipsoid tangential critical values and multiplier:',[(round(float(hfn(*r[:4])),6),round(r[4],6)) for r in roots])
