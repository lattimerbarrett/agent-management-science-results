import sympy as sp
from z3 import Real, RealVal, Solver
eta, delta, d = sp.symbols('eta delta d', real=True)
print('Spectral bound rearrangement:')
print(sp.solve(sp.Eq(eta, delta+(1-delta)*d), d)[0])
print('At delta=eta/2:',sp.simplify(((eta-delta)/(1-delta)).subs(delta,eta/2)))
# Test only the necessary scalar constraints, not operator realizability.
for N in (2,10,100):
    s=Solver()
    e=RealVal('1/3')
    alpha=[Real(f'a_{N}_{i}') for i in range(N+1)]
    for x in alpha: s.add(x>=0,x<=1)
    for i in range(N):
        s.add(alpha[i]<=alpha[i+1], e<=alpha[i+1], e<=1-alpha[i])
    print(f'Necessary scalar constraints, N={N}, eta=1/3:',s.check())
print('These checks do not construct a quasitrace or an operator family.')