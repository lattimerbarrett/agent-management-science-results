import sympy as s
from pathlib import Path
r,e,d,th,A,B=s.symbols('r e d th A B',positive=True)
f=A*(r*s.cos(th))**2/2-A*(r*s.sin(th))**2/2+B*r*r*s.cos(th)*s.sin(th)
assert s.simplify(s.integrate(s.expand_trig(f),(th,0,2*s.pi)))==0
beta=s.Rational(1,4);a=s.Rational(1,2);m=2
assert beta*(m-2*a)/2==s.Rational(1,8)
assert beta**2/2-beta/2==-s.Rational(3,32)
for num,den,power in [(r**3,(1+r)**3,0),(r**3,(1+r)**2,1),(r*r,(1+r)**2,0),(r**4,(1+r)**4,0)]:
 P=s.Poly(s.expand(r**power*den-num),r)
 assert all(co>=0 for co in P.all_coeffs())
assert s.integrate(r**3/(1+r)**5,(r,0,s.oo))==s.Rational(1,4)
R=d/e
assert s.simplify(e*R-d)==0
assert s.simplify(e**2*R**2-d**2)==0
print('n3 exact graph Pohozaev coefficients, tracefree angular cancellation, all radial error bounds checked.')
