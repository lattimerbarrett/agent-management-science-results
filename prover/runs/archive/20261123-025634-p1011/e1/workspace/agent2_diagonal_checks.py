from pathlib import Path
import sympy as s
from fractions import Fraction as F
n=s.symbols('n', integer=True, positive=True)
r=s.symbols('r',positive=True)
j=s.symbols('j',integer=True,nonnegative=True)
q=2*n/(n-2)
qb=2*(n-1)/(n-2)
assert s.simplify(n*(n-2)/q-(n-2)**2/2)==0
assert s.simplify((n-1)/qb-(n-2)/2)==0
assert s.summation(r/2*(s.Rational(1,4))**j,(j,0,s.oo))==2*r/3
# Exact finite-budget majorant never reaches persistence radius.
for J in range(1,301):
 total=sum((F(1,2)*F(1,4)**k for k in range(J)),F(0))
 assert total<F(2,3)<1
# Polynomial cutoff derivative terms after eps=e^{-t}, rho=1/t:
# eps^(9-d)rho^(d-k) = e^{-(9-d)t}t^(k-d).
t=s.symbols('t',positive=True)
for d in [2,4,6,8]:
 for k in range(41):
  assert s.limit(s.exp(-(9-d)*t)*t**(k-d),t,s.oo)==0
print('Exact checks: energy primitive coefficient; all-n boundary height exponent; geometric persistence tail; 164 smooth-cutoff derivative limits.')
Path('workspace/agent2_diagonal_checks.py').write_text(Path(__file__).read_text())
