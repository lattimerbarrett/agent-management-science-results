import sympy as s
eta,t=s.symbols('eta t', real=True)
print('Upper-bound identity:',s.expand((t-eta)+(1-t-eta)))
print('Endpoint scalar constraints:',s.reduce_inequalities([t>=s.Rational(1,2),t<=s.Rational(1,2)],t))
print('These computations do not establish strict order preservation or existence.')