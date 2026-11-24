from fractions import Fraction
from z3 import Real, Solver, unsat

# Check the scalar deduction from positivity/order-preservation:
# d1 <= 1-d0 gives eta <= 1-eta.
eta = Real('eta')
s = Solver()
s.add(eta > 0, eta <= 1-eta, eta > Fraction(1, 2))
assert s.check() == unsat
print('Checked: eta <= 1-eta excludes eta > 1/2.')
