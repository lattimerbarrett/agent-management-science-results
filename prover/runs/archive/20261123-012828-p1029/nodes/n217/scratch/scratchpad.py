from fractions import Fraction
import sympy as s
eta=s.symbols('eta', positive=True)
c=2*eta
print('Rescaled endpoint increment:', s.simplify(c*s.Rational(1,2)))
print('Order-bound condition c<=1:', s.solve_univariate_inequality(c<=1,eta))
print('Universal bound from two increments:', s.solve_univariate_inequality(eta<=1-eta,eta))
for den in range(1,101):
    for num in range(1,den//2+1):
        target=Fraction(num,den)
        scale=2*target
        assert 0<scale<=1
        assert scale*Fraction(1,2)==target
print('All rational rescaling checks passed.')
print('The algebra and quasitrace, including its M_2 extension, are unchanged by scalar rescaling of the sequence.')
print('If b=sup_n(c*a_n), then b/c=sup_n(a_n); hence no-supremum is preserved.')