"""Exact radial linear cancellation for compensated Ricci/II Pohozaev flux.
The general nonlinear mass-sign bridge is NOT established here.
"""
import sympy as s
n,d=s.symbols('n d',positive=True)
beta=d+1-n
# Linear Ricci flux coefficient for G=r^(2-n)+t*r^beta*phi.
C=-2*(beta*(beta-1)+(n-2)*(n-1))-4*(n-1)*beta
assert s.factor(C)==-2*d*(d-1)
mean_phi=(n-2)*(d-2)/(2*(n-1)*(d-1))
ric=s.factor(C*mean_phi)
# For h=t*r'^d, pi_rr= d[(d-1)-(d+n-3)/(n-1)]r'^(d-2).
edge=s.factor(d*((d-1)-(d+n-3)/(n-1)))
assert s.simplify(ric+edge)==0
# Scaling of remaining boundary integrand at infinity.
# X.nu=O(s^(2-d)); R_boundary=O(s^(-d-1)); boundary radial measure s^(n-2)ds.
assert s.expand((2-d)+(-d-1)+(n-2))==n-2*d-1
print('Exact radial Ricci/II edge cancellation checked; remainder integrable for 2d>n.')
