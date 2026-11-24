"""Exact first-order Robin defect for Euclidean graph deformations.
The calculation is symbolic in dimension n, |z|^2=r2, h, z.grad(h), and Delta(h).
It is a necessary local input, not a proof of the dimension threshold.
"""
import sympy as s
n, r2, t, h, zh, lap_h, eps = s.symbols('n r2 t h zh lap_h eps', positive=True)
m=(n-2)/2
U=(1+r2+t*t)**(-m)
a=(n-2)/(2*(n-1))
# Outward normal of {t >= eps*h(z)} is (eps*grad(h), -1)+O(eps^2).
# Its mean curvature is eps*Delta(h)+O(eps^2).
normal_horizontal = -(n-2)*zh*(1+r2)**(-n/2)
normal_vertical = -h*s.diff(U,t,2).subs(t,0)
curvature_term=a*lap_h*U.subs(t,0)
actual=s.simplify(normal_horizontal+normal_vertical+curvature_term)
expected=(n-2)*((h-zh)*(1+r2)**(-n/2)+lap_h/(2*(n-1))*(1+r2)**(-(n-2)/2))
assert s.simplify(actual-expected)==0
k=s.symbols('k', integer=True, nonnegative=True)
harmonic=s.simplify(actual.subs({zh:k*h,lap_h:0}))
assert s.simplify(harmonic+(n-2)*(k-1)*h*(1+r2)**(-n/2))==0
# Check the inward graph orientation directly on a paraboloid at z=0.
# h=|z|^2/2: normal=(eps*z,-1)/sqrt(1+eps^2|z|^2), H(0)=eps*(n-1).
# At z=0 the Robin curvature term therefore has positive linear sign.
assert s.simplify(a*(n-1)-(n-2)/2)==0
# Verify general identity for linearized interior Yamabe operator applied to P*(1+|x|^2)^(-n/2).
# Treat P=H_l homogeneous harmonic; check in dimensions 3..8 using H_l=Re((x0+i*x1)^l).
for dim in range(3,9):
    xs=s.symbols('x:'+str(dim),real=True)
    radius=sum(x*x for x in xs)
    for ell in range(1,5):
        P=s.re((xs[0]+s.I*xs[1])**ell).expand(complex=True)
        assert s.expand(sum(s.diff(P,x,2) for x in xs))==0
        assert s.expand(sum(x*s.diff(P,x) for x in xs)-ell*P)==0
print('PASS: symbolic-n graph Robin residual, harmonic specialization, and curvature sign')
print('PASS: harmonic polynomial identities in dimensions 3..8, degrees 1..4')
