import sympy as s
from pathlib import Path
# Tangential positivity can be promoted to full positivity by changing a
# defining function r to r+C*r**2. In coordinates dr proportional to dz2,
# this adds a positive rank-one normal term to its complex Hessian.
a,c,x,y=s.symbols('a c x y', real=True)
T=(x*x+y*y)/a-c+1
H=s.Matrix([[a,x+s.I*y],[x-s.I*y,c+T]])
assert s.simplify(H.det()-a)==0
assert s.simplify(H[1,1]-(x*x+y*y)/a-1)==0
print('Rank-one normal correction: H11=a>0 and det(H)=a>0.')
# Explicit nonpseudoconvex compact example, to audit orientation signs.
# rho=(|z1|^2-1)^2+|z2|^2-4; q=(0,sqrt(3)).
z,zb,w,wb=s.symbols('z zb w wb')
rho=(z*zb-1)**2+(s.sqrt(3)+w)*(s.sqrt(3)+wb)-4
assert s.simplify(rho.subs({z:0,zb:0,w:0,wb:0}))==0
assert s.diff(rho,z,zb).subs({z:0,zb:0,w:0,wb:0})==-2
assert s.diff(rho,w).subs({z:0,zb:0,w:0,wb:0})==s.sqrt(3)
r=-rho
rp=s.expand(r+r*r)
h=-s.sqrt(3)*w+3*w*w
hb=-s.sqrt(3)*wb+3*wb*wb
remainder=s.expand(rp-h-hb-2*z*zb-5*w*wb)
assert all(sum(m)>=3 for m,k in s.Poly(remainder,z,zb,w,wb).terms())
print('Explicit orientation check: Levi_K(e1)=-2; exterior Levi(e1)=+2.')
print('After r -> r+r^2: quadratic Hermitian part diag(2,5).')
print('Holomorphic support quadratic h=-sqrt(3)*w+3*w^2.')
print('Remainder has degree >=3:', remainder)
# Quantitative bound: for R=||(z,w)||<=delta<1, every monomial
# of degree d>=3 has absolute value <=delta**(d-2)*R**2.
delta=s.Rational(1,1000)
B=sum(s.Abs(k).subs(s.sqrt(3),2) for m,k in s.Poly(remainder,z,zb,w,wb).terms())
assert B*delta < 1
assert 3*delta**2+delta**4+4*delta < 1
print('Certified radius delta=', delta, '; remainder <=', B*delta, '*R^2.')
print('Thus on exterior in this ball, Re(h)<=-R^2/2, with exact rational bounds.')
