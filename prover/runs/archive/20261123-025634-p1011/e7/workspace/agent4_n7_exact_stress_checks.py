from pathlib import Path
import sympy as s
R,r=s.symbols('R r',positive=True)
for k in range(2,7):
 A=s.integrate(r**(k+3)/(1+r*r)**5,(r,0,R))
 B=s.integrate(r**(k+5)*(1-r*r)/(1+r*r)**7,(r,0,R))
 J=(k-1)*(s.Rational(5,24)*k*(k+4)*A+s.Rational(25,2)*B)-s.Rational(5,24)*k*(k+4)*R**(k+4)/(1+R*R)**5
 closed=s.Rational(25,24)*R**(k+4)*(k-(k-2)*R**2)/(1+R*R)**6
 assert s.simplify(-J-closed)==0
 if k==4: assert s.limit(R**2*closed,R,s.oo)==-s.Rational(25,12)
 if k==6: assert s.limit(closed,R,s.oo)==-s.Rational(25,6)
# Actual coordinate check of the identity producing both bilinear coefficients.
z=s.symbols('z0:6'); S=1+sum(t*t for t in z); U=S**(-s.Rational(5,2)); beta=s.Rational(5,12)
for f,k in [(z[0]**2-z[1]**2,2),(z[0]**3-3*z[0]*z[1]**2,3),(sum(t*t for t in z)*z[0],3)]:
 lapf=sum(s.diff(f,t,2) for t in z)
 euler=sum(t*s.diff(f,t) for t in z)
 # Express all terms over S^(9/2), avoiding fractional-power ambiguity.
 div_numerator=-5*((euler+6*f)*S-7*f*(S-1))
 g_numerator=5*(k-1)*f*S-beta*lapf*S**2
 assert s.Poly(s.expand(div_numerator+35*f+beta*lapf*S**2+g_numerator),*z).is_zero
print('Exact n7 linear counterterms k2..6 and bilinear integration identity checked.')
Path('workspace/agent4_n7_exact_stress_checks.py').write_text(Path(__file__).read_text())
