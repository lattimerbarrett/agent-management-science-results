import sympy as s
t,p=s.symbols('t p', real=True, positive=True)
F=(1-t)**p
print('Integral F on [0,1]:',s.integrate(F,(t,0,1)))
print('Second derivative:',s.diff(F,t,2).factor())
print('For p>=1: F is convex, F(0)=1, F(1)=0, integral=1/(p+1).')
print('Hence the scalar extremal-distribution constraints allow every value in (0,1/2].')
