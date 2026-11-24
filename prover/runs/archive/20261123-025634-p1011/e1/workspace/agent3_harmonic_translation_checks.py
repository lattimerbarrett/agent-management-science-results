import sympy as s
from pathlib import Path
t,r,m=s.symbols('t r2 m',positive=True)
D=lambda f:s.diff(f,t)+2*t*s.diff(f,r)
Lap=lambda f:s.diff(f,t,2)+4*t*s.diff(f,t,r)+4*r*s.diff(f,r,2)+2*m*s.diff(f,r)
H1=t;H2=t*t-r/m;H3=t**3-3*t*r/(m+2)
H4=t**4-6*t*t*r/(m+4)+3*r*r/((m+4)*(m+2))
a2=2*(m-1)/(m*(m+2));a3=3*m/((m+4)*(m+2))
for H in [H1,H2,H3,H4]:assert s.simplify(Lap(H))==0
assert s.simplify(t*H2-H3-a2*r*H1)==0
assert s.simplify(t*H3-H4-a3*r*H2)==0
for j in range(4):
 b=2*(m-1)/m+2*j*a2
 assert s.simplify(D(r**j*H2)-(2*j*r**(j-1)*H3+b*r**j*H1))==0
 k=2*j*b+6*j*m/(m+2)+4*j*(j-1)*a3
 # Full second derivative includes l0,l2,l4 radial pieces.
 target_l2=k*r**(j-1)*H2
 target_l4=4*j*(j-1)*r**(j-2)*H4
 target_l0=b*(1+2*j/m)*r**j
 assert s.simplify(D(D(r**j*H2))-target_l0-target_l2-target_l4)==0
 assert s.simplify(Lap(r**j*H2)-2*j*(m+2*j+2)*r**(j-1)*H2)==0
# Angular moments on S^(m-1), E[t^(2a)]=(1/2)_a/(m/2)_a.
def av(poly):
 p=s.Poly(s.expand(poly.subs(r,1)),t)
 return s.simplify(sum(co*s.rf(s.Rational(1,2),power[0]//2)/s.rf(m/2,power[0]//2) if power[0]%2==0 else 0 for power,co in p.terms()))
assert s.simplify(av(H1**2)-1/m)==0
assert s.simplify(av(H2**2)-2*(m-1)/(m*m*(m+2)))==0
assert s.simplify(av(H3**2)-6*(m-1)/(m*(m+2)**2*(m+4)))==0
print('PASS: all-m harmonic recurrences, first/second translations, Laplacian and angular norm formulas verified exactly.')
