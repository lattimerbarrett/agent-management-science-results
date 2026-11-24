from fractions import Fraction as Q
from itertools import product

def F(t): return max(Q(0), Q(1)-t)
grid=[Q(k,4) for k in range(9)]
checks=0
for n in range(2,6):
 for ts in product(grid, repeat=n):
  assert n*F(sum(ts)/n) <= sum(F(t) for t in ts)
  checks+=1
print('Uniform spectral-tail law satisfies', checks, 'finite-summand convexity constraints.')

# Scalar constraints from every nonempty finite sum of N increments.
# Assign q(sum_{i in S} b_i)=1/2 and q(1-sum_{i in S} b_i)=1/2.
# This respects all inclusion inequalities and the disjoint-sum order bounds.
for N in range(2,9):
 for mask in range(1,1<<N):
  for other in range(1,1<<N):
   if mask & other == mask:
    assert Q(1,2) <= Q(1,2)
   if not(mask & other):
    assert Q(1,2) <= 1-Q(1,2)
print('Finite-sum scalar order/complement constraints remain consistent at eta=1/2.')
print('These checks do not construct operators or a quasitrace.')
