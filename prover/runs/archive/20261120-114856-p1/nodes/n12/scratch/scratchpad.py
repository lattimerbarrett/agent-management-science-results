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

# Exact-arithmetic check of the reduction for a nontrivial block.
A=sp.diag(1,2,4,7)
r=sp.Matrix([1,2,1,3])
K=sp.Matrix.hstack(r,A*r)
coef=(K.T*A*K).inv()*(K.T*r)
rnew=r-A*K*coef
assert K.T*rnew == sp.zeros(2,1)
a0,a1=sp.symbols('a0 a1')
Pvec=A**2*r+a1*A*r+a0*r
polycoef=sp.solve(list(K.T*Pvec),[a0,a1])
Pvec=Pvec.subs(polycoef)
assert rnew == Pvec/polycoef[a0]
print('Exact s=2 orthogonal-polynomial reduction verified.')
