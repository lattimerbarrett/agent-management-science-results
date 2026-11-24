import sympy as s
r2,t=s.symbols('r2 t',real=True)
D=r2+(t+1)**2
cayley_norm2=(4*r2+(r2+t*t-1)**2)/D**2
print('Cayley identity:',s.factor(cayley_norm2-(1-4*t/D)))
n=s.Integer(19)
a=(n-2)/2
qb=2*(n-1)/(n-2)
print('n=19: bubble exponent a =',a,'critical boundary exponent =',qb)
print('Boundary trace mass scaling exponent (must be zero):',s.simplify(n-1-a*qb))
print('Boundary peak exponent from trace mass:',s.simplify((n-1)/qb))
print('Tail scaling: (n-2)-2*(8-1) =', (n-2)-2*(8-1))
print('These identities check conditional transfer/concentration only, not existence of exact solutions.')
