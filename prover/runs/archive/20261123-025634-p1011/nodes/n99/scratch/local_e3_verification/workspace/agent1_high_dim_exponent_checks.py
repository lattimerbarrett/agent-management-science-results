import sympy as s
from pathlib import Path
n,r=s.symbols('n r',positive=True)
a=n*(n-2);q=2*n/(n-2);c=(n-2)/(4*(n-1))
# Boundary stationarity density divided by U_boundary^2.
grad2=(n-2)**2*r**2/(1+r**2)**2
lap_U2=2*(n-2)*(n-1)*(r**2-1)/(1+r**2)**2
assert s.factor(a/q/(1+r**2)**2-grad2/2+c*lap_U2)==0
# Bulk quadratic tail exponent, boundary cubic tail exponent.
assert s.expand((n-1)+2*(7+1-n))==15-n
assert s.expand((n-2)+2*7+6+2*(2-n))==22-n
# Trace-dual integrability criterion simplifies to n>16.
t=2*(n-1)/n
exponent=s.factor((8-n)*t+n-2)
assert s.factor(exponent+1+(n-1)*(n-16)/n)==0
# Local cubic/leading-energy ratio: delta*R^(23-n), delta=mu*eps^7,R=r/eps.
mu,eps,R=s.symbols('mu eps R',positive=True)
assert s.simplify(s.expand_power_base(mu*eps**7*(r/eps)**(23-n)/(mu*eps**(n-16)*r**(23-n)),force=True))==1
print('Exact boundary stationarity and all high-dimensional weighted exponents checked.')
if __file__.endswith('scratchpad.py'):
    Path('workspace/agent1_high_dim_exponent_checks.py').write_text(Path(__file__).read_text())
