import sympy as s
eta,t=s.symbols('eta t', positive=True)
d=s.solve(s.Eq(eta,t+(1-t)*s.Symbol('d')),s.Symbol('d'))[0]
print('Dimension lower bound for the spectral cutoff:', d)
print('With cutoff eta/2:', s.factor(d.subs(t,eta/2)))
print('Bound on positive partial sums of the cutoff projections:', 2/eta)
print('The lower bound is strictly positive for 0<eta<=1.')