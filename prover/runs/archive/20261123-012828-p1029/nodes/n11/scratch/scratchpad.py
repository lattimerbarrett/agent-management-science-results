import sympy as s
eta=s.symbols('eta', real=True)
print('For three increments d0,d1,d2 with sum <= 1:')
print('eta <= tau(d0+d1) <= 1-eta.')
print('At eta=1/2 both bounds equal:', s.Rational(1,2))
print('For any finite nonempty F with an unused increment:')
print('eta <= tau(sum_F d_i) <= 1-eta.')
print('Thus every such finite sum has quasitrace 1/2 at the endpoint; this is not a contradiction without strict monotonicity.')
print('Ultraproduct diagonal principle: if eta_k -> eta > 0 and each eta_k is witnessed, the quotient coordinate sequences retain gap eta.')