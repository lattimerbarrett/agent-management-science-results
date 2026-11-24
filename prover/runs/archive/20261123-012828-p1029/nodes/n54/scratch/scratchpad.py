import sympy as sp
eta = sp.Symbol('eta', positive=True)
n = sp.Symbol('n', integer=True, positive=True)
constant_limit = sp.limit(eta, n, sp.oo)
print('Limit of the prescribed quasitrace increments:', constant_limit)
print('Quasitracial exhaustion requires that same limit to be 0.')
print('Can eta > 0 and eta = 0 both hold?', sp.reduce_inequalities([eta > 0, sp.Eq(eta, 0)], eta))
