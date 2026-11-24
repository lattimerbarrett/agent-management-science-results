import sympy as sp
x, eta = sp.symbols('x eta', real=True)
F=1-x
print('Endpoint extremal spectral-tail candidate F(x)=1-x on [0,1]')
print('Integral:', sp.integrate(F,(x,0,1)))
s,t=sp.symbols('s t', real=True)
print('Convexity equality:', sp.simplify(2*(1-(s+t)/2)-(1-s)-(1-t)))
print('Scale endpoint witness by c=2*eta:')
c=2*eta
print('New increment quasitrace:', sp.simplify(c*sp.Rational(1,2)))
print('Inverse order-scaling factor:',1/c)
