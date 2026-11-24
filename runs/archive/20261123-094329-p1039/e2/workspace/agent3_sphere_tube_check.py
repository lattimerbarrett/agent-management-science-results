"""Exact Levi calculation for the S^(2n-3)-tube candidate.
This checks geometry only and makes NO assertion of the Oka property.
"""
import sympy as s
T,e=s.symbols('T e',real=True)
A=e**2-(T-1)**2
N=s.expand((4*T-2)*A+4*T*(T-1)**2)
certificate=2*(T-(1-e**2))**2+2*e**2*(1-e**2)
assert s.expand(N-certificate)==0
# Adapted coordinates: z=(sqrt(T),0,...), w=sqrt(A).
# Tangent basis: radial-w vector (sqrt(A),-2(T-1)sqrt(T)),
# together with the n-2 z-directions orthogonal to z.
# The first basis vector has Levi norm N. Each remaining norm is 2(T-1).
assert s.simplify(N.subs(T,1-e)-4*e**2*(1-e))==0
assert s.simplify(N.subs(T,1+e)-4*e**2*(1+e))==0
assert s.simplify(N.subs(T,1)-2*e**2)==0
assert (2*(T-1)).subs(T,1-e)==-2*e
assert (2*(T-1)).subs(T,1+e)==2*e
# Smoothness: if d rho=0 on the boundary, w=0, T=1+/-e,
# and the squared gradient norm equals 4 e^2 T >0 for 0<e<1.
grad_norm=4*(T-1)**2*T+A
assert s.simplify(grad_norm.subs(T,1-e)-4*e**2*(1-e))==0
assert s.simplify(grad_norm.subs(T,1+e)-4*e**2*(1+e))==0
print('S^(2n-3)-tube: exact tangential Levi certificate verified.')
print('For 0<eps<1: one positive tangent eigenvalue everywhere;')
print('the other n-2 eigenvalues have sign T-1. NO Oka claim checked.')
