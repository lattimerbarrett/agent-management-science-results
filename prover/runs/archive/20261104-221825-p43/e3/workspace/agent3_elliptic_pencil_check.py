import sympy as s
from pathlib import Path
t,a,b,c,x,y=s.symbols('t a b c x y')
f=a*t*t;g=t*(b+c*t**4)
Delta=s.expand(4*f**3+27*g**2)
assert s.expand(Delta-t*t*(27*b*b+(54*b*c+4*a**3)*t**4+27*c*c*t**8))==0
# Exact order-four action on base; multipliers satisfy x^3,y^2 weight i.
lamx=-s.I
lamy=s.sqrt(2)*(-1-s.I)/2
assert s.simplify(lamy**2-s.I)==0
P=y*y-x**3-f*x-g
trans=s.expand(P.subs({t:s.I*t,x:lamx*x,y:lamy*y}, simultaneous=True)-s.I*P)
assert trans==0
# Generic concrete a=b=c=1 gives 8 simple, nonzero residual roots.
D0=s.Poly((Delta/t**2).subs({a:1,b:1,c:1}),t)
assert s.gcd(D0,D0.diff()).degree()==0
assert D0.eval(0)!=0 and D0.degree()==8
# Infinity vanishing orders: u^4 f(1/u),u^6 g(1/u).
u=s.symbols('u')
finf=s.expand(u**4*f.subs(t,1/u));ginf=s.expand(u**6*g.subs(t,1/u))
assert finf==a*u*u and ginf==b*u**5+c*u
print('Weierstrass discriminant:',Delta)
print('a=b=c=1: eight simple nonzero discriminant roots, type-II vanishing orders at0/infinity.')
print('Exact base-order4 Weierstrass automorphism verified.')
print('This is a geometric candidate only, not a Hamiltonian map with two fixed points.')
Path('workspace/agent3_elliptic_pencil_check.py').write_text(Path('scratchpad.py').read_text())
