import sympy as s
eta,d=s.symbols('eta d', positive=True)
t=eta/2
# If eta <= t*(1-d)+d, then d >= (eta-t)/(1-t).
bound=s.factor((eta-t)/(1-t))
print('Spectral projection dimension lower bound:', bound)
print('Bound minus eta/2:',s.factor(bound-eta/2))
print('Projection partial-sum bound: 2/eta')
# The established exhaustion property applied to these projections
# forces their quasitrace values to zero, contradicting the bound.
