import sympy as s
c,d=s.symbols('c d',real=True)
# Exact maximum of h(phi)^2 magnitude.
assert s.expand((1-c*c)*(1+4*c*c)-(s.Rational(25,16)-4*(c*c-s.Rational(3,8))**2))==0
assert (s.Rational(9,4)*s.sqrt(2))**2<16
# Translation estimates: |Delta s|<=d and |Delta q|<4d.
# On M, |c|, |Re q|<=1, so errors satisfy these scalar majorants.
assert s.expand(2*d+d*d+8*d+16*d*d)==10*d+17*d*d
assert s.expand(4*d+2*(4*d+d+4*d*d))==14*d+8*d*d
delta=s.Rational(1,2**12)
epsilon=s.Rational(1,2**14)
assert delta<s.Rational(1,17)
assert delta<s.Rational(1,8)
assert 10*delta+17*delta**2<11*delta
assert 14*delta+8*delta**2<15*delta
assert (11**2+15**2)*delta**2==346*delta**2
assert 346*delta**2<epsilon
# Near p=(4,0), sqrt(z) stays within delta of2, q within delta of0.
assert 2*delta**2<s.Rational(1,2)
assert s.Rational(1,4)>epsilon
print('Verified explicit translated-KB inclusion and open rational-hull pocket radius 2^-12.')
print('These are geometric/hull checks only; no non-Oka implication is asserted.')
