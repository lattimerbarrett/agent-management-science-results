import sympy as s
from pathlib import Path
f,g,lam,eps,r,u0,delta0=s.symbols('f g lam eps r u0 delta0')
u=u0+f/lam
delta=delta0+eps*r*r-f*f-eps*g*g
J=s.Matrix([u,delta]).jacobian([f,g])
assert s.factor(J.det()) == -2*eps*g/lam
R=s.Integer(2); B=s.Integer(4)
e=s.Rational(1,100); l=s.Rational(1,20); rr=s.Rational(1,200)
margin=s.factor(1+e*rr**2-(1+e)*l*l*B*B-e*R*R)
assert margin>0
assert s.Rational(1,10)+10*s.Rational(1,100)<1 # bidisc contraction
assert -2*e*rr/l !=0
print('Positive real-part margin:',margin)
print('Jacobian determinant at chosen center:',-2*e*rr/l)
x,y,t,h=s.symbols('x y t h', real=True)
# G(u,delta)=(-delta exp(2iu), exp(u)); t=Im u and eta=h>=0.
rho=(x*x+y*y)*s.exp(-4*t)+2*x*s.exp(-2*t)+h
assert s.diff(rho,h)==1
assert s.simplify(s.diff(rho,x)-2*x*s.exp(-4*t))==2*s.exp(-2*t)
