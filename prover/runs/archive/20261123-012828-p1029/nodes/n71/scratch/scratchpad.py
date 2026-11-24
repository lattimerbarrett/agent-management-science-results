import sympy as s
eta=s.symbols('eta', positive=True)
r,N=s.symbols('r N', positive=True)
print('For an r-fold diagonal copy in M_N(M), ambient increment:', r*eta/N)
print('After normalizing the supporting corner:', s.cancel((r*eta/N)/(r/N)))
delta=s.symbols('delta', positive=True)
c=2*delta
print('Rescale the verified endpoint witness by c=2*delta.')
print('New increment:', s.simplify(c*s.Rational(1,2)))
print('Order bounds: 0 <= c*a_n <= c*a_(n+1) <= c*1 <= 1 when delta<=1/2.')
print('If b is a supremum of c*a_n, b/c is a supremum of a_n, since positive scalar multiplication is an order isomorphism.')
print('Thus matrix-copy/corner normalization alone does not amplify eta, but scaling the verified endpoint supplies every target delta in (0,1/2].')