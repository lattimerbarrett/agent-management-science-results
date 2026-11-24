import sympy as s
import pathlib
x,y=s.symbols('x y',real=True); z=s.symbols('z')
fprime=s.I*z+(2+2*s.I)+2/z
assert s.simplify(fprime-s.I*(z+1-s.I)**2/z)==0
F=-x*y+2*x-2*y+s.log(x*x+y*y)
grad=[s.factor(s.diff(F,t)) for t in (x,y)]
assert all(g.subs({x:-1,y:1})==0 for g in grad)
H=s.hessian(F,(x,y));assert H.subs({x:-1,y:1})==s.zeros(2)
print('Holomorphic factor:',s.factor(z*fprime));print('Gradient:',grad)
a,b=s.symbols('a b',real=True)
series=s.series(F.subs({x:-1+a*s.Symbol('t'),y:1+b*s.Symbol('t')}),s.Symbol('t'),0,4)
print('Cubic expansion:',series)
# Explicit transition estimates for |eta prime|<=8, epsilon .001, R1000.
eps=s.Rational(1,1000);R=1000
perturb_grad_bound=4*(1+16)
assert 1/eps>2*eps+3+perturb_grad_bound
assert R/2>3+4/R+perturb_grad_bound
print('Inner transition bound:',1/eps,'>',2*eps+3+perturb_grad_bound)
print('Outer transition bound:',R/2,'>',3+4/R+perturb_grad_bound)
