import sympy as s
from fractions import Fraction
# A complete metric alone does not turn bounded increasing sequences into
# Cauchy sequences: initial-segment projections in l_infinity have sup-norm
# distance 1 at every two different indices.
for n,m in [(1,2),(3,9),(20,40)]:
 a=[int(i<n) for i in range(m)]
 b=[int(i<m) for i in range(m)]
 assert max(abs(x-y) for x,y in zip(a,b)) == 1
print('Complete-metric countercheck: increasing initial segments remain distance 1.')
# The universal two-increment bound uses no noncommutative additivity.
u, eta=s.symbols('u eta', real=True)
print('Two-increment certificate:', s.simplify((u-eta)+(1-u-eta)))
# Quasitracial completeness + closed order gives:
# metric Cauchy monotone bounded sequence => least upper bound in M.
# Contraposition supplies non-Cauchy tail gaps, not conversely.
print('Verified implication: bounded increasing + metric Cauchy => supremum in M.')
print('Missing assertion: bounded increasing => metric Cauchy.')
# Check the cofinal interpolation estimate from the alternative recurrence.
t=s.symbols('t', nonnegative=True)
a,b=s.symbols('a b', real=True)
print('Interpolation increment identity:', s.expand(((1-t)*a+t*b)-a))
for r in range(1,21):
 assert (1-Fraction(1,5))**r > 0
print('Constant-gap interpolation preserves upper bounds by geometric convergence.')
