import sympy as s
G=s.Matrix([[s.Rational(1,2),s.Rational(1,2)],[s.Rational(1,2),s.Rational(1,2)]])
D=s.diag(*G.diagonal())
print('Gram eigenvalues:',G.eigenvals())
print('Diagonal-minus-Gram eigenvalues:',(D-G).eigenvals())
eta,u=s.symbols('eta u', real=True)
print('Upper-bound certificate:',s.expand((u-eta)+(1-u-eta)))
