import math
import sympy as sp
from scipy.integrate import quad

p, e = sp.symbols('p e', positive=True)
a = (p-1)*(1-e)
assert sp.simplify(p*(-1+e)+a-(-1+e)) == 0
assert sp.simplify(a+(-1+e)*(p-1)) == 0
q = p/(p-1)
assert sp.simplify(q-1-1/(p-1)) == 0

# Negative-axis Hilbert-transform integral for f(y)=y^(e-1)1_(0,1).
# y=u^(1/e) removes the endpoint singularity.
for ep in [0.5, 0.25, 0.1]:
    for t in [0.01, 0.2, 0.8]:
        integral, error = quad(lambda u: 1/(t+u**(1/ep)), 0, 1,
                               epsabs=1e-11, epsrel=1e-11)
        H_abs = integral/(math.pi*ep)
        analytic_lower = t**(-1+ep)/(2*math.pi*ep)
        assert H_abs + error/(math.pi*ep) >= analytic_lower
        print(f'epsilon={ep:g}, t={t:g}, |Hf(-t)|={H_abs:.10g}, '
              f'proved lower bound={analytic_lower:.10g}')

# Exact scalar A_p expression on the interval (0,1).
for pp in [1.5, 3., 5.]:
    for ep in [0.5, 0.25, 0.1]:
        alpha = (pp-1)*(1-ep)
        expression = (1/(1+alpha))*ep**(-(pp-1))
        assert expression <= (4/ep)**(pp-1)
        print(f'p={pp:g}, epsilon={ep:g}, A_p on (0,1)={expression:.10g}')
print('All symbolic identities and numerical checks passed. Numerical checks do not prove supremum bounds.')
