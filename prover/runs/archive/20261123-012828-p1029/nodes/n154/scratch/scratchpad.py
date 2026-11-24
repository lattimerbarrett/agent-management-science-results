import sympy as s
eta=s.symbols('eta', positive=True)
c=2*eta
print('Scaling factor:',c)
print('Scaled endpoint increment:',s.simplify(c*s.Rational(1,2)))
u=s.symbols('u', real=True)
print('Two-increment upper-bound certificate:',s.expand((u-eta)+(1-u-eta)))
print('Thus endpoint scaling covers 0 < eta <= 1/2, and the certificate excludes eta > 1/2.')
