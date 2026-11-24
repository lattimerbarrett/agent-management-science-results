import sympy as s
a=s.Rational(1,5)
p=(s.sqrt(3*a-2*a*a)-2*a)/(1-2*a)
C=s.simplify(3/(1+2*(1-p)**2))
print('p =', s.simplify(p))
print('three-part lower-bound coefficient =', C, '=', s.N(C,15))
random=(1+s.sqrt(a))**2
print('random lower-bound coefficient =', random, '=', s.N(random,15))
print('difference =', s.simplify(C-random), '=', s.N(C-random,15))
x=s.symbols('x', positive=True)
print('ratio equation:', s.expand(x**2-a*(1+2*(1-x)**2)))
