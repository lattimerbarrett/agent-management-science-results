import sympy as s
from pathlib import Path
n,L,t,z=s.symbols('n L t z', positive=True)
F=s.Function('F');q=(1-t*t)**(L/s.Integer(2))*F(1-t*t)
op=(1-t*t)*s.diff(q,t,2)-n*t*s.diff(q,t)+(n-L*(L+n-2)/(1-t*t))*q
A=(L-1)/2;B=(L+n)/2;C=L+n/2
expected=(1-t*t)**(L/s.Integer(2))*(4*z*(1-z)*s.diff(F(z),z,2)+4*(C-(A+B+1)*z)*s.diff(F(z),z)-4*A*B*F(z)).subs(z,1-t*t)
assert s.simplify(s.expand(op-expected))==0
# Continuation coefficients A0,B0; outward derivative at pi/2 equals -B0.
# Gamma(-1/2)=-2Gamma(1/2) gives D=-B0/A0.
assert s.simplify(C-A-(L+n+1)/2)==0
assert s.simplify(C-B-L/2)==0
assert s.simplify(C-A-B-s.Rational(1,2))==0
print('Verified all-n/all-L hypergeometric radial Jacobi ODE and endpoint gamma arguments.')
