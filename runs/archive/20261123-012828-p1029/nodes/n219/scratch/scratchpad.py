import sympy as sp
r,t,z,a=sp.symbols('r t z a', real=True)
print('Interpolation increment:', sp.expand(((1-t)*a+t*z)-a))
P,u,v=sp.symbols('P u v')
print('Residual-coefficient identity:', sp.simplify((1-t)*(P*u+(1-P)*v)+t*v-((1-t)*P*u+(1-(1-t)*P)*v)))
from fractions import Fraction
eta=Fraction(1,7)
for N in range(1,101):
    P=Fraction(1)
    for k in range(N):
        tk=eta+(1-eta)*Fraction(k%5,5)
        assert eta <= tk <= 1
        P*=1-tk
    assert 0 <= P <= (1-eta)**N
print('Checked product bound for 100 interpolation lengths.')