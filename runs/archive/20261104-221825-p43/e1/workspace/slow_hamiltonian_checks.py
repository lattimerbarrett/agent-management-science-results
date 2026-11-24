"""Symbolic identities used in the short-period exclusion lemma."""
import sympy as s
# The variance identity in arbitrary finite samples is polynomial.
for n in range(2,9):
    x=s.symbols('x:'+str(n))
    mean=sum(x)/n
    lhs=sum((v-mean)**2 for v in x)
    rhs=sum((v-w)**2 for v in x for w in x)/(2*n)
    assert s.expand(lhs-rhs)==0
# Wirtinger for trigonometric polynomials: the kth Fourier mode has
# derivative norm squared (2*pi*k/T)^2 times its norm squared.
# Orthogonality and completion extend the inequality to smooth loops.
t=s.symbols('t',real=True)
for k in range(1,6):
    u=s.cos(k*t)
    norm=s.integrate(u*u,(t,0,2*s.pi))
    dnorm=s.integrate(s.diff(u,t)**2,(t,0,2*s.pi))
    assert s.simplify(dnorm-k*k*norm)==0
    assert k*k>=1
# Pointwise spherical Hamiltonian formula for the sign convention:
# X_f = grad(f) cross x; x dot ((grad f cross x) cross v)=grad f dot v
# for v tangent to the unit sphere.
x,y,z,a,b,c,p,q,r=s.symbols('x y z a b c p q r',real=True)
v=s.Matrix([p,q,r]); pos=s.Matrix([x,y,z]); grad=s.Matrix([a,b,c])
expr=s.expand(pos.dot((grad.cross(pos)).cross(v))-grad.dot(v))
expected=(pos.dot(pos)-1)*grad.dot(v)-grad.dot(pos)*pos.dot(v)
assert s.expand(expr-expected)==0
print('Variance, Fourier/Wirtinger, and Hamiltonian sign identities checked exactly.')
