import sympy as s
from pathlib import Path
u,v,p,q,a=s.symbols('u v p q a', real=True)
f=u*v+p*q
Y=s.Matrix([a,(1-a/u)*v,p/2,q/2])
assert s.simplify(sum(s.diff(f,z)*Y[i] for i,z in enumerate([u,v,p,q]))-f)==0
Dnegative=u*u+v*v+p*p+q*q
YD=s.expand(sum(s.diff(Dnegative,z)*Y[i] for i,z in enumerate([u,v,p,q])))
expected=2*u*a+2*(1-a/u)*v*v+p*p+q*q
assert s.simplify(YD-expected)==0
# On u>=0, a=0, squared distance to forward null ray omits u².
Dpositive=v*v+p*p+q*q
assert s.simplify(sum(s.diff(Dpositive,z)*Y[i] for i,z in enumerate([u,v,p,q])).subs(a,0)-(2*v*v+p*p+q*q))==0
# Explicit same-level arc on the two spheres.
t=s.symbols('t', real=True)
x=s.Matrix([s.sin(t),0,s.cos(t)])
y=s.Matrix([s.sin(t),0,-s.cos(t)])
assert s.trigsimp(x.dot(x)-1)==0 and s.trigsimp(y.dot(y)-1)==0
assert x[2]+y[2]==0
assert s.trigsimp(x.diff(t).dot(x.diff(t))+y.diff(t).dot(y.diff(t)))==2
# General capsule normal form and smooth coefficients (no division by A).
A=s.Function('A')(u); d=s.Function('d')(u); eps=s.symbols('eps', positive=True)
f_general=A*v+p*q
D_general=d+v*v+p*p+q*q
a_general=-eps*A*s.diff(d,u)
b_general=1+eps*s.diff(A,u)*s.diff(d,u)
Y_general=s.Matrix([a_general,b_general*v,p/2,q/2])
assert s.simplify(sum(s.diff(f_general,z)*Y_general[i] for i,z in enumerate([u,v,p,q]))-f_general)==0
assert s.simplify(sum(s.diff(D_general,z)*Y_general[i] for i,z in enumerate([u,v,p,q]))-(-eps*A*s.diff(d,u)**2+2*b_general*v*v+p*p+q*q))==0

print('Arc and expanding-vector-field identities verified.')
