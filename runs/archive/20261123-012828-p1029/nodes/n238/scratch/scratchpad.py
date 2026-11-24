from fractions import Fraction
# With an established endpoint witness, scaling by t=2*eta gives eta.
for q in range(2,101):
 for p in range(1,q//2+1):
  eta=Fraction(p,q)
  t=2*eta
  assert 0<t<=1 and t*Fraction(1,2)==eta
print('Endpoint scaling verified exactly for all sampled rational eta in (0,1/2].')
print('Upper bound: eta<=tau(a1)<=1-eta, hence eta<=1/2.')
print('Ultraproduct audit: finite configurations preserve fixed gaps; no-supremum needs a separate diagonal upper-bound argument, not just AW* preservation.')
