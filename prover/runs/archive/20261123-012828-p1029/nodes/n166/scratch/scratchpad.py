import sympy as s
eta,t,C=s.symbols('eta t C', positive=True)
# Correct spectral-threshold lower bound on projection dimension.
delta=(eta-t)/(1-t)
print('threshold dimension lower bound:',delta)
print('eta=1/3, t=1/6:',delta.subs({eta:s.Rational(1,3),t:s.Rational(1,6)}),'Bessel bound:',6)
# Dimension-only recurrence from weighted finite joins.  This scalar
# model shows that the recurrence does not imply exhaustion.
m=s.symbols('m', positive=True, integer=True)
Cp=C/(m-(m-1)*C)
D=lambda z:1-1/z
print('D(Cprime)-m D(C) =',s.factor(D(Cp)-m*D(C)))
print('Thus D(C)=max(0,1-1/C) is compatible with this recurrence in its valid regime.')
# Also verify intersection compression recurrence at integer C>1.
print('Intersection recurrence slack:',s.factor(D(C-1)-(2-1/D(C))))
