import sympy as s
t,p=s.symbols('t p', real=True, positive=True)
F=(1-t)**p
print('Extremal scalar candidate F_p(t)=(1-t)^p, p>=1')
print('integral:',s.integrate(F,(t,0,1)))
print('second derivative:',s.diff(F,t,2))
print('Thus convexity and endpoint conditions allow every integral in (0,1/2].')
e=s.symbols('e',positive=True)
L=s.log((1+e)/e)
G=s.log((1+e)/(t+e))/L
print('A second family has integral:',s.simplify(s.integrate(G,(t,0,1))))
print('Its convexity is explicit:',s.simplify(s.diff(G,t,2)))
