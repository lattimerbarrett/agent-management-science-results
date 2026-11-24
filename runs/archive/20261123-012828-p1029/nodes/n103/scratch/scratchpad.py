import sympy as s
eta,u=s.symbols('eta u', real=True)
print('Two-increment certificate:',s.expand((u-eta)+(1-u-eta)))
print('If eta>0 witness exists, monotone order-Cauchy regularity cannot hold:')
print('C*(b_n,1) gives tau(b_n**2) >= eta**2, hence d >= eta**(2/3).')
print('Projection normality does not apply directly: b_n need not be projections or monotone.')
print('Order continuity with an existing supremum does not assert a supremum exists.')
print('No scalar contradiction at eta=1/2: interior tau(a_n)=1/2 is feasible.')