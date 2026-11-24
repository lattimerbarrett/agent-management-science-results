import sympy as sp
import mpmath as mp

# Exact algebra used by the two scalar test families.
p, eps = sp.symbols('p eps', positive=True)
a = (p-1)*(1-eps)
assert sp.simplify(p*(-1+eps)+a-(-1+eps)) == 0
q = p/(p-1)
assert sp.simplify((q-1)*(p-1)-1) == 0

# For v(x)=|x|^(-1+eps), the scalar A_p expression on (0,1).
characteristic_on_01 = 1/eps * ((p-1)/(p-eps))**(p-1)
print('A_p expression on (0,1):', characteristic_on_01)
print('Exact exponent identities: PASS')

# The Hilbert transform of 1_(0,1) is pi^-1 log|x/(x-1)|.
# We integrate its output only over (0,1). The quantity below is
# eps * ||H 1_(0,1)||_{L^p(v);(0,1)} / ||1_(0,1)||_{L^p(v)}.
# The change of variables s=-eps log x removes the singular measure.
mp.mp.dps = 35
for power in [mp.mpf('1.5'), mp.mpf('3')]:
    limit = mp.gamma(power+1)**(1/power)/mp.pi
    print('p =', power, 'asymptotic scaled ratio =', mp.nstr(limit, 12))
    for e in [mp.mpf('.2'), mp.mpf('.1'), mp.mpf('.05')]:
        def integrand(s):
            if s == 0:
                return mp.mpf(0)  # endpoint value does not affect integral
            term = s + e*mp.log(-mp.expm1(-s/e))
            return mp.exp(-s)*abs(term)**power
        val = mp.quad(integrand, [0, e*mp.log(2), 1, 4, mp.inf])
        scaled_ratio = val**(1/power)/mp.pi
        rigorous_lower = mp.exp(-2/power)/(2*mp.pi)
        assert scaled_ratio > rigorous_lower
        print('  eps =', e, 'scaled ratio =', mp.nstr(scaled_ratio, 12),
              'analytic lower bound =', mp.nstr(rigorous_lower, 12))
