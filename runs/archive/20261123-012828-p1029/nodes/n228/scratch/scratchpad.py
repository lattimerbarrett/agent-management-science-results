import sympy as s
x,alpha=s.symbols('x alpha', positive=True)
F=1-x**alpha
print('Integral of F_alpha:',s.integrate(F,(x,0,1)))
print('Second derivative:',s.diff(F,x,2).factor())
print('For 0<alpha<=1: F_alpha is decreasing and convex, F(0)=1, F(1)=0.')
print('Its integral tends to 1/2 as alpha tends to 1 from below.')
print('Thus the midpoint-convexity inequality alone gives no strict universal gap.')
