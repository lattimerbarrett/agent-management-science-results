import sympy as s
A,Ap,dprime,eps,v,p,q=s.symbols('A Ap dprime eps v p q', real=True)
b=1+eps*Ap*dprime
Yh=(-eps*A*dprime)*(Ap*v)+(b*v)*A+(p/2)*q+(q/2)*p
YD=(-eps*A*dprime)*dprime+2*b*v*v+p*p+q*q
print('Yh-h:',s.simplify(Yh-(A*v+p*q)))
print('YD:',s.expand(YD))
# Boundary interpolation: at a tangential critical point normal derivatives
# interpolate linearly, so opposite signs force a boundary critical point.
a,c=s.symbols('a c', real=True)
t=s.symbols('t', real=True)
print('zero of interpolated normal derivative:',s.solve((1-t)*a+t*c,t))
