import sympy as s
# Specialized equal-area product-of-spheres fixed-point theorem:
# for (S^2)^k it gives k+1 distinct fixed points, degeneracy allowed.
k=2
print('Specialized degenerate Arnold bound for two equal-area spheres:', k+1)
# Audit the capsule merger independently.
u,v,z,w,eps=s.symbols('u v z w eps',real=True)
A=s.Function('A')(u); d=s.Function('d')(u)
h=A*v+z*w; D=d+v*v+z*z+w*w
Y=s.Matrix([-eps*A*s.diff(d,u),(1+eps*s.diff(A,u)*s.diff(d,u))*v,z/2,w/2])
vars=(u,v,z,w)
def deriv(f): return s.expand(sum(Y[i]*s.diff(f,vars[i]) for i in range(4)))
print('Yh-h =',s.simplify(deriv(h)-h))
expected=-eps*A*s.diff(d,u)**2+2*(1+eps*s.diff(A,u)*s.diff(d,u))*v*v+z*z+w*w
print('YD-formula =',s.simplify(deriv(D)-expected))
# cup length via square-free monomials
from itertools import product
pos=[(1,0),(0,1),(1,1)]
nonzero=lambda fs: all(sum(f[j] for f in fs)<=1 for j in range(2))
print('cup length =',max(n for n in range(1,4) if any(nonzero(fs) for fs in product(pos,repeat=n))))
