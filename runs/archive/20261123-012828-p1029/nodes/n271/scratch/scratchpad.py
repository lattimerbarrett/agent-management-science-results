import sympy as s
# For the extremal spectral model F(t)=(1-t)_+ on [0,1],
# the dimension-only n-block Weyl inequalities reduce to Jensen.
# Check that they do not by themselves exclude the endpoint 1/2.
from fractions import Fraction
from itertools import product
F=lambda t:max(Fraction(0),1-t)
checks=0
for n in range(2,6):
    grid=[Fraction(k,4) for k in range(9)]
    for ts in product(grid,repeat=n):
        assert n*F(sum(ts)/n)<=sum(F(t) for t in ts)
        checks+=1
print('Dimension-model inequalities passed:',checks)
t=s.symbols('t', real=True)
print('Integral of the candidate tail distribution:',s.integrate(1-t,(t,0,1)))
print('These scalar inequalities leave the endpoint viable; they do not construct an operator realization.')
