import sympy as s
r,k,e0,e1=s.symbols('r k eta_0 eta_1', positive=True)
gap=s.factor((r*e0+(k-r)*e1)/k)
print('Normalized matrix-quasitrace gap for r bad blocks and k-r auxiliary blocks:')
print(gap)
print('If eta_1=1/2, the gap is:')
print(s.collect(s.expand(gap.subs(e1,s.Rational(1,2))),r/k))
print('Deficit from 1/2:')
print(s.factor(s.Rational(1,2)-gap.subs(e1,s.Rational(1,2))))