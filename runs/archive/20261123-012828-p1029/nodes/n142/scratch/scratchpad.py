import sympy as s
eta=s.symbols('eta', positive=True)
t=eta/2
lower=s.factor((eta-t)/(1-t))
print('Spectral dimension lower bound:',lower)
print('Projection partial-sum bound:',s.simplify(1/t))
assert s.simplify(lower-eta/(2-eta))==0
print('For 0 < eta <= 1 the lower bound is strictly positive, contradicting finite-factor projection exhaustion.')
