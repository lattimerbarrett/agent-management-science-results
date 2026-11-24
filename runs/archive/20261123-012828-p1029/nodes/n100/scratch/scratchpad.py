from fractions import Fraction
h=Fraction(1,2)
# At an endpoint witness, every nonempty finite sum of increments
# has quasitrace 1/2, by comparison with an unused increment.
print('quasitrace of finite nonempty increment sum:', h)
print('quasitrace of its complement:', 1-h)
print('additivity defect for disjoint nonempty finite sums:', h-h-h)
print('equal values on comparable elements do not give zero on their difference:')
print('q(y)-q(x) =', h-h, '; q(y-x) =', h)
for eta in [Fraction(1,100), Fraction(1,4), Fraction(1,2)]:
    scale=2*eta
    assert 0<scale<=1 and scale*h==eta
    print('eta =',eta,'; scaling of endpoint witness =',scale)
