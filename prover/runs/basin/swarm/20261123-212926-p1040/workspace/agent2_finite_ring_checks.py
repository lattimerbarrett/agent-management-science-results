"""Exact universal Fox/current-matrix and finite-ring checks for W_c."""
import sympy as S
from math import prod
x,a,b,u=S.symbols('x a b u')
I=S.eye(2); E=S.Matrix([[0,1],[0,0]]); F=E.T
# Cycle-coordinate order is (3,1), so root alpha=e3-e1 is E12.
A=I+x*E; B=I-x*F; D=S.diag(1+x,1)
comm=lambda P,Q:S.simplify(P*Q*P.inv()*Q.inv())
assert comm(D,A)==I+x*x*E
# Entire group commutator identity, before truncation.
C=comm(I+a*E,I+b*F)
assert C==S.Matrix([[1+a*b+a*a*b*b,-a*a*b],[a*b*b,1-a*b]])
# Current Lie matrices: t is the adjoint action of x2.
t=S.symbols('t'); d=S.diag(t,0)
for c in range(3,129):
    Y=t**(c-2)*E
    assert d*Y-Y*d==t*Y
    L=Y*(-t*F)-(-t*F)*Y
    assert L*d-d*L==S.zeros(2)
    # Modulo pi^c, the two off-diagonals and quadratic diagonal correction vanish.
    assert min(2*c-3,c,2*c-2)>=c
    cc=C.subs({a:x**(c-2),b:-x}).applyfunc(S.expand)
    reduce=lambda z:S.Poly(z,x).rem(S.Poly(x**c,x)).as_expr()
    vv=1-x**(c-1)
    assert cc.applyfunc(reduce)==S.diag(vv,1+x**(c-1))
    # Local ramified fields Phi_ell(1+X^r), p odd divisor or p=2.
    odds=[p for p in S.factorint(c) if p%2]
    p=min(odds) if odds else 2
    ell=p if p%2 else 4
    r=c//(p if p%2 else 4)
    P=S.Poly(S.cyclotomic_poly(ell,x).subs(x,1+x**r),x)
    e=r*int(S.totient(ell))
    assert P.degree()==e and P.LC()==1 and P.TC()==p
    assert all(int(z)%p==0 for z in P.all_coeffs()[1:])
    assert int(P.TC())%(p*p)!=0
    assert e*p//(p-1)==c
    f=3 if p==2 else 2 if p in (3,5) else 1
    assert p**f>=7 and f%p
print('PASS exact commutator identity; current-Lie Johnson kernels, truncated torus matrices, and local-field Eisenstein/conductor constructions for 3<=c<=128')
