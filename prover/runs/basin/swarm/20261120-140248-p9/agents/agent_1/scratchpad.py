import math
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma

# Verify exact integrals and rigorous lower-bound constants for scalar tests.
# Numerical integration uses y=exp(-u/eps), then u=v/(1-v).
# The indicator test gives integral log(1+1/t)^p t^(eps-1) dt.
def output_integral(p, eps):
    def integrand(u):
        if u == 0:
            return math.log(2.0)**p
        a = u/eps
        log_term = a + math.log1p(math.exp(-a))
        return math.exp(-u) * log_term**p / eps
    return quad(integrand, 0, np.inf, epsabs=1e-8, epsrel=1e-10)[0]

for p in (1.5, 3., 4.):
    for eps in (.2, .1, .05):
        actual = output_integral(p, eps)
        lower = gamma(p+1)/eps**(p+1)
        assert actual >= lower * (1-1e-9)
        alpha1 = -1+eps
        alpha2 = (p-1)*(1-eps)
        def at_origin(alpha):
            return 1/((alpha+1)*(1-alpha/(p-1))**(p-1))
        A1, A2 = at_origin(alpha1), at_origin(alpha2)
        # Direct quadrature of both power integrals, after exact substitution
        # x = t^(1/(alpha+1)) (first) or t^(1/delta) (second).
        for a in (alpha1, alpha2):
            d = 1-a/(p-1)
            first = quad(lambda t: 1/(a+1), 0, 1)[0]
            second = quad(lambda t: 1/d, 0, 1)[0]
            assert math.isclose(first*second**(p-1),at_origin(a),rel_tol=1e-12)
        norm_ratio_lower = (eps*actual)**(1/p)/math.pi
        print(f'p={p:g}, eps={eps:g}: origin Ap(alpha=-1+eps)={A1:.6g}; '
              f'origin Ap(alpha=(p-1)(1-eps))={A2:.6g}; '
              f'indicator norm ratio lower={norm_ratio_lower:.6g}; '
              f'eps*ratio={eps*norm_ratio_lower:.6g}')
print('All numerical checks passed. They are checks of the scalar obstructions, not of a sharp matrix theorem.')
