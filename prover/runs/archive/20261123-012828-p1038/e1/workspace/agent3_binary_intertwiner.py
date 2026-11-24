"""Exact closed REAL self-adjoint binary Darboux step for the fixed Dirac curve.
This is a local Lax identity, NOT a proved determinant identity for M(Q).
"""
import sympy as s

def exact_checks():
    x,y,Z,r,R=s.symbols('x y Z r R',nonzero=True)
    d=(r*(x-1/x)-R*(y-1/y))/2
    eta=(r*(x+1/x)-R*(y+1/y))/2
    z=y/x
    a=x*(y*y+1)/(y*(x*x+1))
    b=(y*y-x*x)/(y*(x*x+1))
    dp=(r*(x+1/x)/2)*(y*y-1)/(y*y+1)-(R*(y+1/y)/2)*(x*x-1)/(x*x+1)
    rp=r/a;Rp=R*a
    H=s.Matrix([[d,r-R/Z],[r-R*Z,-d]])
    Hp=s.Matrix([[dp,rp-Rp/Z],[rp-Rp*Z,-dp]])
    T=s.Matrix([[Z/a-1,-b/a],[-b*Z/a,Z-1/a]])
    adj=T.T.subs(Z,1/Z)
    factor=(z+1/z-Z-1/Z)/a
    identities=[T*H-Hp*T,adj*T-factor*s.eye(2),T.subs(Z,z)*s.Matrix([x,1]),T.subs(Z,1/z)*s.Matrix([-1/x,1])]
    for mat in identities:
        assert all(s.factor(t)==0 for t in mat)
    assert s.factor(rp*Rp-r*R)==0
    assert s.factor(dp*dp+rp*rp+Rp*Rp-d*d-r*r-R*R)==0
    assert s.factor(T.det()-(Z-z)*(Z-1/z)/a)==0
    # Orthogonal-projector representation of the correct paired Darboux kernel.
    U=s.Matrix([[x,-1],[1,x]])
    A=(U*s.diag(z,1/z)*U.inv()).applyfunc(s.factor)
    F=Z*s.eye(2)-A
    K=s.Matrix([[a,0],[b,1]])
    assert all(s.factor(t)==0 for t in K*T-F)
    print('8 exact canonical binary-Darboux identities passed')
    return T,Hp

if __name__=='__main__': exact_checks()
