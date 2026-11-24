import sympy as s
n=s.symbols('n', integer=True, positive=True)
p=(n+2)/(n-2)
a=2**((n-2)/2)
print('For v = 2^((n-2)/2) u, the interior nonlinear coefficient is:')
print(s.simplify(n*(n-2)*a**(1-p)))
print('This equals c_n times n(n-1):')
print(s.simplify((n-2)/(4*(n-1))*n*(n-1)))
