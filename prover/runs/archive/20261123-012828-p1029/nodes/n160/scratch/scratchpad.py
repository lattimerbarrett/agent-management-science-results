import sympy as s
x,a=s.symbols('x a',commutative=False)
d=s.symbols('delta',positive=True,commutative=True)
print('Regularized compression difference:')
print(s.expand((x+d)*a*(x+d)-x*a*x))
print('For ||a|| <= C, its norm is at most C*delta*(2*||x||+delta).')
print('Thus compression preserves a bounded supremum already existing in the self-adjoint order.')
print('A join in the projection lattice alone is NOT the hypothesis of this argument.')
