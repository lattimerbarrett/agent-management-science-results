import sympy as sp
x=sp.symbols('x', real=True)
alpha=sp.symbols('alpha', positive=True)
F=(1-x)**alpha
print('F_alpha(x)=',F)
print('second derivative:',sp.factor(sp.diff(F,x,2)))
print('integral on [0,1]:',sp.integrate(F,(x,0,1)))
for a in [1,sp.Rational(3,2),2,3]:
 print('alpha =',a,'; mean =',sp.integrate(F.subs(alpha,a),(x,0,1)))
print('Thus alpha>1 gives convex tails with every mean strictly between 0 and 1/2.')
