import sympy as s
p=s.symbols('p', positive=True)
a=p-1
b=p-1+1/p
beta=s.factor(b/a)
print('Characteristic exponent a(p) =', a)
print('Operator-norm exponent b(p) =', b)
print('Ratio b(p)/a(p) =', beta)
print('Difference from proposed exponent =', s.simplify(beta-(1+1/(p-1)-1/p)))
print('At p=2: a, b, beta =', a.subs(p,2), b.subs(p,2), beta.subs(p,2))
