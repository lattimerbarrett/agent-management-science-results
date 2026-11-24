import sympy as s
x,y,eta,e1,e2=s.symbols('x y eta e1 e2',real=True)
D=e1-2*y
N=D**2+2*y*D+(e2+2*x)*((x-1)**2+y*y)
S=(e1-y)**2+(x-eta)**2+eta*(1-eta)+e2*(1-eta)
constraint=x*x+y*y-2*x+eta
assert s.rem(s.Poly(s.expand(N-S),x),s.Poly(constraint,x)).as_expr()==0
print('Worm tangent-Levi sum-of-squares identity independently checked modulo boundary equation.')
