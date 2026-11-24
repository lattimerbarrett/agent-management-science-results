import sympy as sp
eta, q2 = sp.symbols('eta q2', positive=True)
# In C*(b,1), q is a positive state. Cauchy--Schwarz gives
# eta**2 <= q(b**2); hence d(b,0) >= eta**(2/3).
print('Constant increment implies: eta**2 <= tau(b_n**2).')
print('Thus d_tau(a[n+1],a[n]) >=', eta**sp.Rational(2,3))
print('Sequential order-Cauchy regularity would force the left side to 0.')
print('No convergence in M and no completeness of its bounded balls is needed.')