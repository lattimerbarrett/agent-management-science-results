import sympy as s
x=s.symbols('x', positive=True)
p=s.Integer(4)
a=s.Integer(2)
print('p =',p,'; w(x) = x**',a)
print('Integral of w**(-1/(p-1)) on (0,1):',s.integrate(x**(-a/(p-1)),(x,0,1)))
print('Integral of w**(-1) on (0,1):',s.integrate(x**(-a),(x,0,1)))
