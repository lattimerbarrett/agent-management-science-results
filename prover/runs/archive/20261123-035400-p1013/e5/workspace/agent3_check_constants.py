from fractions import Fraction as F
import sympy as s
h=s.symbols("h", integer=True, positive=True)
# For h>=3, all coefficients in h=3+u expansion are positive.
u=s.symbols("u", nonnegative=True)
gap=s.expand((500*h*h-(h*h+7*h+3)).subs(h,u+3))
assert all(c>0 for c in s.Poly(gap,u).all_coeffs())
for r in range(2,101):
 for hh in range(r+1,201):
  eta=F(1,1000*r*hh*hh)
  assert (hh*(hh+7)+3)*eta < F(1,2*r)
  assert F(1,r)-4*eta > (hh+1)*eta
print("Exact symbolic positivity certificate:",gap)
print("Finite rational grid verified: 2<=r<=100, r+1<=h<=200")
