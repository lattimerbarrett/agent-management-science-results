import sympy as s
n=s.symbols('n', integer=True, positive=True)
a=(n-2)/2
# N disjoint cutoff bubbles with epsilon=N^(-2/a), grid spacing N^(-1/(n-1)).
eps_exp=-2/a
spacing_exp=-1/(n-1)
print('Exponent of N in total source mass N*epsilon^a:',s.simplify(1+a*eps_exp))
print('Exponent of N in gradient-commutator bound sqrt(N)*(epsilon/spacing)^a:',s.simplify(s.Rational(1,2)+a*(eps_exp-spacing_exp)))
print('Exponent of N in total cutoff-energy error N*(epsilon/spacing)^(n-2):',s.simplify(1+(n-2)*(eps_exp-spacing_exp)))
print('Number of bubble energies: N; hence energy diverges despite vanishing source mass and residual.')
