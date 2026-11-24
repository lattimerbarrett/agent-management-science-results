"""Exact radial symbolic checks, no claim of threshold or gluing proof."""
import sympy as s
m,r=s.symbols('m r', positive=True)
F=s.Function('F')(r)
O=2/(1+r)
# P harmonic homogeneous degree 2 in R^m; expressions below divide by P.
lap=lambda q:4*r*s.diff(q,r,2)+2*(m+4)*s.diff(q,r)
euler=lambda q:2*q+2*r*s.diff(q,r)
# u=Omega P F; the equatorial metric is Omega^2 dx^2.
J_sphere=(lap(O*F)-2*(m-2)*euler(O*F)/(1+r))/O**2+m*O*F
J_flat=lap(F)-2*m*euler(F)/(1+r)+2*m*F/(1+r)
assert s.simplify(J_sphere-J_flat/O)==0
for j in range(5):
    f=r**j
    actual=(m-1)*(f-euler(f)+(1+r)*lap(f)/(2*m))
    expected=(m-1)*((1-(2+2*j))*f+(1+r)*j*(2*j+m+2)*r**(j-1)/m)
    assert s.expand(actual-expected)==0
print('PASS: first Robin graph variation and stereographic Jacobi covariance, all dimensions symbolically.')
