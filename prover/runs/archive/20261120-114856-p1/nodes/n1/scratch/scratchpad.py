import sympy as sp
# For s=2, verify the orthogonal monic polynomial and residual normalization.
m1,m2,m3=sp.symbols('m1 m2 m3', real=True)
a,c=sp.symbols('a c')
sol=sp.solve([m2+a*m1+c,m3+a*m2+c*m1],[a,c])
print('Monic orthogonal polynomial t^2+a*t+c:',sol)
print('Constant term:',sp.factor(sol[c]))
# Algebraic condition on a limiting two-cycle in the energy-normalized variables.
t,rho=sp.symbols('t rho')
p1,p2,q1,q2=sp.symbols('p1 p2 q1 q2')
p=1+p1*t+p2*t*t;q=1+q1*t+q2*t*t
print('Cycle support must lie among roots of:',sp.expand(p*q-rho**2))
