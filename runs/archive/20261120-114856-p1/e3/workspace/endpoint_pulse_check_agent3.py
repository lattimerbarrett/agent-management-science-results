import sympy as s
from pathlib import Path
t,a,k=s.symbols('t a k',positive=True,real=True)
xi=-a*s.tanh(a*t/2);u=a*a/(2*k)/s.cosh(a*t/2)**2
assert s.simplify(s.diff(xi,t)+k*u)==0
assert s.simplify(s.diff(u,t)-xi*u)==0
assert s.simplify(xi*xi+2*k*u-a*a)==0
assert s.limit(xi,t,s.oo)==-a
assert s.limit(xi,t,-s.oo)==a
assert s.integrate(u,(t,-s.oo,s.oo))==2*a/k
print('Exact one-mode pulse, invariant, asymptotic signs, and integral all checked.')
Path('workspace/endpoint_pulse_check_agent3.py').write_text(Path('scratchpad.py').read_text())
