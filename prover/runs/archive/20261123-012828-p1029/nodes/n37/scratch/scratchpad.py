import sympy as sp
# For h >= 0 and a normalized 2-quasitrace, abelian Cauchy--Schwarz
# gives q(h)^2 <= q(h^2).  With d=q(h^2)^(1/3), this is q(h)<=d^(3/2).
d, eta = sp.symbols('d eta', positive=True)
print('Square of the resulting bound:', sp.simplify((d**sp.Rational(3,2))**2))
print('A constant increment eta forces metric distance at least:', eta**sp.Rational(2,3))
print('Consistency check:', sp.simplify((eta**sp.Rational(2,3))**sp.Rational(3,2)))