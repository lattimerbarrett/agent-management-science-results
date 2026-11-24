import sympy as s
eta,t,d=s.symbols('eta t d', positive=True)
# Spectral cutoff b <= t(1-p)+p gives eta <= t+(1-t)d.
print('Cutoff dimension lower bound:',s.solve(s.Eq(eta,t+(1-t)*d),d)[0])
print('At t=eta/2:',s.factor(((eta-t)/(1-t)).subs(t,eta/2)))
# The cutoff argument is compatible with eta<=1/2 and alone does
# not force eta=0; demonstrate its necessary scalar constraints.
from fractions import Fraction
for E in [Fraction(1,10),Fraction(1,3),Fraction(1,2)]:
    T=E/2
    D=(E-T)/(1-T)
    C=1/T
    print('eta=',E,'threshold=',T,'dimension lower bound=',D,'Bessel bound=',C)
