import sympy as s
z,zb,w,wb=s.symbols('z zb w wb')
rho=(z*zb-1)**2+(s.sqrt(3)+w)*(s.sqrt(3)+wb)-4
r=-rho
R=s.expand(r+r*r)
h=-s.sqrt(3)*w+3*w*w
hb=-s.sqrt(3)*wb+3*wb*wb
P=s.Poly(s.expand(R-h-hb-2*z*zb-5*w*wb),z,zb,w,wb)
C=s.simplify(sum(abs(c) for mon,c in P.terms()))
print('sum absolute remainder coefficients =',C)
assert C==15+16*s.sqrt(3)
assert C<43
# For ||(z,w)||<=1/100 and conjugate variables interpreted genuinely,
# |P| <= C/100 * (|z|^2+|w|^2) < 0.43 ||(z,w)||^2.
# Also |r| <= 2 sqrt(3)|w|+|w|^2+2|z|^2+|z|^4 < 1/20.
d=s.Rational(1,100)
bound=2*s.sqrt(3)*d+3*d*d+d**4
assert bound<s.Rational(1,20)
print('Certified remainder factor <',s.Rational(43,100))
print('Certified |r| < 1/20, so r and r+r^2 have identical signs.')
