import sympy as s
eta=s.symbols('eta', positive=True)
t=eta/2
delta=s.factor((eta-t)/(1-t))
print('cutoff:',t)
print('dimension lower bound:',delta)
print('Bessel bound:',s.simplify(1/t))
print('reconstruction:',s.simplify(t+(1-t)*delta))
