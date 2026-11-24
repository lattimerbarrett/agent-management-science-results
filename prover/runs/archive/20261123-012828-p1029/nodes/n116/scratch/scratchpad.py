from fractions import Fraction
# Exact check of the scalar certificate used in the established upper bound.
for eta in [Fraction(1,4), Fraction(1,2), Fraction(3,4)]:
    lo, hi = eta, 1-eta
    print(f'eta={eta}: necessary interval for tau(a_1) = [{lo}, {hi}]; nonempty={lo <= hi}')
print('This checks only the scalar bound, not quasitracial exhaustion or existence.')
