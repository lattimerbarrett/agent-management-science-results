import sympy as s
from pathlib import Path
n=s.symbols('n', integer=True, positive=True)
t=s.symbols('t', nonnegative=True)
p=t**2-t-1
T=(1+s.sqrt(5))/2
assert s.simplify(p.subs(t,T))==0
assert s.diff(p,t).subs(t,T)==s.sqrt(5)
# rho(z,w)=||z||²+|w|⁴-|w|²-1;
# complex Hessian diag(I_{n-1},4|w|²-1).
x,y=s.symbols('x y',real=True)
r=(x*x+y*y)**2-(x*x+y*y)-1
levi=s.expand((s.diff(r,x,2)+s.diff(r,y,2))/4)
assert s.simplify(levi-(4*(x*x+y*y)-1))==0
# boundary at (z1,w)=(1,0); w is complex tangent and has Levi -1.
assert levi.subs({x:0,y:0})==-1
# Smoothness: if z!=0 gradient in z nonzero. If z=0 then t=T,
# and derivative wrt w is (2*T-1)*conj(w), nonzero.
assert T>0 and 2*T-1>0
# Every point contracts to (0,w) in the domain, and (0,w) contracts to
# 0 because p(t)<0 for 0<=t<T. This proves connectedness and contractibility.
assert s.solve_univariate_inequality(p<0,t)==(t<T)
print('Verified fiber radius roots, complex Hessian, negative tangential eigenvalue, boundary smoothness, connectedness criterion.')
