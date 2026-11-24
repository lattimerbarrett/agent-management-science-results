import sympy as sp
s,t=sp.symbols('s t', real=True)
F=lambda x:(1-x)**2
print('Quadratic tail mean:',sp.integrate(F(t),(t,0,1)))
print('Matrix midpoint-convexity gap:',sp.factor(F(s)+F(t)-2*F((s+t)/2)))
# For Lambda=1/3, the elementary high-spectral-corner bound
# F(t) <= (1-Lambda)/(1-Lambda+Lambda*t) becomes (2+t)F(t)<=2.
print('High-spectral-corner bound gap:',sp.factor(2-(2+t)*F(t)))
print('Original uniform candidate mean:',sp.integrate(1-t,(t,0,1)))
print('\nUltraproduct construction notes:')
print(open('experiments/e1/agent3_qt_ultraproduct_notes.md').read())