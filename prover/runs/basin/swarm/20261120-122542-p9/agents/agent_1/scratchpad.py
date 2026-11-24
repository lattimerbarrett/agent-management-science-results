import sympy as s
p = s.symbols('p', positive=True)
q = p/(p-1)
E = lambda t: 1 + 1/(t*(t-1))
# These are algebraic consistency checks, not checks of the analytic estimate.
assert s.factor(E(p) - (1 + 1/(p-1) - 1/p)) == 0
assert s.factor(E(q) - (p-1)*E(p)) == 0
assert E(s.Integer(2)) == s.Rational(3,2)
assert s.limit(E(p), p, s.oo) == 1
assert s.limit((p-1)*E(p), p, 1, dir='+') == 1
print('All five exact symbolic consistency checks passed.')
