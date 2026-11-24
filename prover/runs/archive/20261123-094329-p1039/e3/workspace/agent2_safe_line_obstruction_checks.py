import sympy as s
r=s.Rational(1,10)
delta=r**4
a2=3+delta
assert 2<a2<8 # c=sqrt(2/a2) satisfies 1/2<c<1
q=s.symbols('q',nonnegative=True)
rho_f=s.expand(a2+2*q+(q-1)**2-4)
assert rho_f==delta+q**2
assert s.simplify((r+r*r)/(1-r*r))==s.Rational(1,9)
assert s.simplify(r*r*(1+s.Rational(1,9)))==s.Rational(1,90)
assert s.Rational(1,90)<r/2
# The exact squared angular loss on the boundary is 2r^4.
assert delta+r**4==2*r**4
print('PASS: actual-candidate holomorphic safe-line obstruction constants.')
