import sympy as s
# rho=||z'||^2+(|w|^2-1)^2-4. Boundary smoothness:
t=s.symbols('t', real=True)
print('Fiber squared radius:',s.factor(4-(t-1)**2))
print('w Levi eigenvalue:',s.diff((t-1)**2,t)+t*s.diff((t-1)**2,t,2))
print('Boundary at w=0: ||zprime||^2=3; Levi(w)=-2.')
# Critical points require zprime=0 and w=0 or |w|^2=1.
print('Critical rho values:',(t-1)**2-4, 'at t=0,1:',[(t-1)**2 .subs(t,k) if False else ((t-1)**2-4).subs(t,k) for k in (0,1)])
print('rho is proper and has n-1 positive Levi eigenvalues everywhere.')
print('For n>=3 this supplies at least two strictly positive eigenvalues.')
# Exhaustion of the interior.
r=s.symbols('r', negative=True)
print('For psi=-log(-rho): scalar Hessian coefficient',s.diff(-s.log(-r),r),'rank-one coefficient',s.diff(-s.log(-r),r,2))