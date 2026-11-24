import sympy as s
eta,u=s.symbols('eta u', real=True)
c=2*eta
print('Scaled endpoint increment:', s.simplify(c*s.Rational(1,2)))
print('Two-increment upper-bound certificate:', s.expand((u-eta)+(1-u-eta)))
print('Allowed scaling range:', s.reduce_inequalities([eta>0,c<=1],eta))
# These are algebraic checks only. Endpoint existence is the verified premise;
# scaling does not replace M, tau, or its M_2 extension.
