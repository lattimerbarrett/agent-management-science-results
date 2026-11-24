import sympy as s
C, delta, d = s.symbols('C delta d', positive=True)
eta = delta/C
coefficient = eta/d
print('Set eta_0 =', eta)
print('Coefficient for projection of dimension d:', coefficient)
print('Quasitrace of that increment:', s.simplify(coefficient*d))
print('If d >= delta, the coefficient is <= 1/C.')
print('\nNo-supremum audit:')
print('The bounded sums alone do not establish absence of a supremum in the original factor.')
print('In a quasitracial ultrapower, diagonal reindexing produces a smaller upper bound')
print('from any putative supremum: y=[a_{r(k)}], with r(k) ->_U infinity.')
print('Choose r(k) slowly enough that (y-b)_+=0, while tau((b-y)^2)>=eta_0^2/2.')
print('Thus the constant-gap sequence in the ultrapower has no least upper bound.')
