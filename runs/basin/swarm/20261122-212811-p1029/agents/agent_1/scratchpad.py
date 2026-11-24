import sympy as sp
# Exact telescoping certificate in the tracial case, for arbitrary N.
N, eta, t0 = sp.symbols('N eta t0', positive=True)
k = sp.symbols('k', integer=True, nonnegative=True)
t = sp.Function('t')
# Encode only the given constant-increment relation after applying a trace.
closed_form = t0 + N*eta
assert sp.simplify(closed_form.subs(N, N+1)-closed_form-eta) == 0
assert sp.simplify(closed_form.subs(N, 0)-t0) == 0
print('Exact trace recurrence verified: t_N = t_0 + N*eta.')
print('For eta > 0, choosing N > 1/eta contradicts 0 <= t_N <= 1.')
# The quasitrace axioms alone give q(d)+q(1-d)=1 for a contraction d.
u=sp.symbols('u', real=True)
assert sp.simplify(u+(1-u)-1)==0
print('Complement identity checked symbolically; it does not telescope noncommuting increments.')
