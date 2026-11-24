import sympy as s
from fractions import Fraction
t,C=s.symbols('t C', positive=True)
d=(s.Rational(1,2)-t)/(1-t)
print('Spectral dimension lower bound:',d)
print('In terms of Bessel bound C=1/t:',s.factor(d.subs(t,1/C)))
for cutoff in [Fraction(1,4),Fraction(1,3),Fraction(1,10)]:
    dim=(Fraction(1,2)-cutoff)/(1-cutoff)
    bound=1/cutoff
    assert cutoff+(1-cutoff)*dim==Fraction(1,2)
    print(f'cutoff {cutoff}: dimension >= {dim}, projection partial sums <= {bound}*1')
print('Endpoint scaling: (2*eta)*(1/2) =',s.simplify(2*s.Symbol('eta')*s.Rational(1,2)))
