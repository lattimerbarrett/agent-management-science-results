import sympy as s
C,eta=s.symbols('C eta', positive=True)
lower=(eta*C-1)/(C-1)
model=1-1/C
print('model minus spectral lower bound =',s.factor(model-lower))
print('numerator at eta=1/2:',s.factor(s.together(model-lower).as_numer_denom()[0].subs(eta,s.Rational(1,2))))
print('For eta<=1/2 and C>1/eta>=2 this difference is positive.')
print('Thus this continuous-dimension scalar model is not excluded by the spectral-cut bounds.')
