import sympy as s
n=s.symbols('n', positive=True, integer=True)
c=(n-2)/(4*(n-1))
print('Scalar curvature of u^(4/(n-2))*g:', s.simplify(n*(n-2)/c))
print('Boundary mean curvature coefficient:', s.simplify(1/(2*c)))
print('Rescaling to scalar curvature n*(n-1): u ->', s.simplify(4**((n-2)/4)))
