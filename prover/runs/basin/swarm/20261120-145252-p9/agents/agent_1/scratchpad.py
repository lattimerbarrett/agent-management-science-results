import sympy as s
import mpmath as mp

# Algebraic checks for a scalar obstruction, not a matrix sharpness proof.
p, eps = s.symbols('p eps', positive=True)
q = p/(p-1)
a = (p-1)*(1-eps)
assert s.simplify(p*(eps-1)+a-(eps-1)) == 0
assert s.simplify(a/(p-1)-(1-eps)) == 0
assert s.simplify(1/(q-1)-(p-1)) == 0

# The common mixed-bound exponent is compatible with duality.
B = lambda r: 1+1/(r*(r-1))
assert s.simplify(B(q)/(p-1)-B(p)) == 0

# Integral J(eps) = int_0^1 u^(eps-1)/(1+u) du.
# Substitution v=u^eps removes the endpoint power singularity:
# eps*J(eps) = int_0^1 1/(1+v^(1/eps)) dv, between 1/2 and 1.
mp.mp.dps = 50
for e in [mp.mpf('0.5'),mp.mpf('0.2'),mp.mpf('0.1'),mp.mpf('0.02')]:
    j_scaled = mp.quad(lambda v: 1/(1+v**(1/e)), [0,1])
    j_formula = e*(mp.digamma((e+1)/2)-mp.digamma(e/2))/2
    assert abs(j_scaled-j_formula) < mp.mpf('1e-45')
    assert mp.mpf('0.5') <= j_scaled <= 1
    print('epsilon =', mp.nstr(e,5), ' epsilon*J(epsilon) =', mp.nstr(j_scaled,18))

# Actual scalar A_p expression on I=(-t,1), using exact antiderivatives.
# For nonnegative a, all intervals are either of this type (up to scaling
# and reflection) or positive intervals (t,1).
for pp in [mp.mpf('1.5'),mp.mpf('3'),mp.mpf('5')]:
    for e in [mp.mpf('0.1'),mp.mpf('0.02')]:
        aa=(pp-1)*(1-e)
        pos0=1/((aa+1)*e**(pp-1))
        upper=(4/e)**(pp-1)
        values=[pos0]
        for i in range(1,200):
            t=mp.mpf(i)/200
            crossing=(1+t**(aa+1))/((aa+1)*(1+t)) * ((1+t**e)/(e*(1+t)))**(pp-1)
            positive=(1-t**(aa+1))/((aa+1)*(1-t)) * ((1-t**e)/(e*(1-t)))**(pp-1)
            assert crossing <= upper and positive <= upper
            values.extend([crossing,positive])
        print('p =',pp,'epsilon =',e,'sampled Ap / endpoint Ap =',mp.nstr(max(values)/pos0,12))
print('All symbolic identities and finite numerical tests passed.')
