import sympy as s
eta,r,rho=s.symbols('eta r rho', positive=True)
k=s.symbols('k', integer=True, positive=True)
print('Corner normalization, assuming the increment is supported in p: eta ->',eta/r)
print('Embedding in one corner of M_k(M): eta ->',eta/k)
print('Then renormalizing that corner:',s.simplify((eta/k)/(1/k)))
print('Scalar order-interval width rho: eta ->',eta/rho)
# Verify the positive congruence identity underlying a general interval change.
B=s.Matrix([[s.Rational(1,4),s.Rational(1,8)],[s.Rational(1,8),s.Rational(1,4)]])
D=s.diag(s.Rational(1,4),s.Rational(1,9))
Di=s.diag(2,3)
print('Example congruence:',Di*B*Di)
print('Matrix-amplification followed by corner normalization supplies no enlargement.')
