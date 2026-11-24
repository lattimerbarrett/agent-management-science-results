import sympy as s
# In a horizontal frame, rho=||v||^2 and psi=rho^{-1}.
r=s.symbols('rho',positive=True)
f=1/r
print('radial coefficient f\' + rho f\'\' =',s.simplify(s.diff(f,r)+r*s.diff(f,r,2)))
print('angular coefficient f\' =',s.diff(f,r))
print('horizontal curvature multiplier -rho f\' =',s.simplify(-r*s.diff(f,r)))
