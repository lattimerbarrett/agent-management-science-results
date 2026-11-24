import sympy as s
eta,t=s.symbols('eta t', positive=True)
p_lower=(eta-t)/(1-t)
print('General spectral lower bound:',p_lower)
print('At t=eta/2:',s.simplify(p_lower.subs(t,eta/2)))
print('Bessel bound at t=eta/2:',s.simplify(1/(eta/2)))
u=s.symbols('u',real=True)
print('Two-increment certificate:',s.expand((u-eta)+(1-u-eta)))
