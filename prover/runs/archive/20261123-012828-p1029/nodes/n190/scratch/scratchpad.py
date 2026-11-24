import sympy as s
t=s.symbols('t', positive=True)
n=s.symbols('n', positive=True)
error=s.integrate((t**(-s.Rational(1,4))-n)**2,(t,0,n**-4))
print('L2-squared truncation error:',s.simplify(error))
print('These truncations have norms n, so this says nothing about bounded-ball completeness.')
