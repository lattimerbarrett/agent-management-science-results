"""Exact local gap-Darboux and crossnode-gluing checks.
This deliberately does NOT assert any identity with the full Atiyah determinant.
"""
import sympy as s

def exact_checks():
    x,y,c,b,Z,r,R=s.symbols('x y c b Z r R',nonzero=True)
    eta=(r*(x+1/x)-R*(y+1/y))/2
    d=(r*(x-1/x)-R*(y-1/y))/2
    H=s.Matrix([[d,r-R/Z],[r-R*Z,-d]])
    D=s.Matrix([[-1/x,1],[Z,-y]])
    Ds=D.T.subs(Z,1/Z)
    J=s.diag(-r*x,R/y)
    assert all(s.factor(t)==0 for t in H-eta*s.eye(2)-Ds*J*D)
    assert s.factor(D.det()-(y/x-Z))==0
    K=d*d+r*r+R*R
    assert all(s.factor(t)==0 for t in H*H-(K-r*R*(Z+1/Z))*s.eye(2))
    assert s.factor(K-eta*eta-r*R*(y/x+x/y))==0
    spectralfactor=r*R*x/y*(1-y/x/Z)*(1-y/x*Z)
    assert s.factor(K-r*R*(Z+1/Z)-eta*eta-spectralfactor)==0
    # Curve difference, so this vanishes when (x,y),(c,b) share height.
    delta=r*((x-1/x)-(c-1/c))-R*((y-1/y)-(b-1/b))
    identity=r/x*(x-c)*(1+x*c)-R/y*c/b*(y-b)*(1+y*b)
    assert s.factor(identity-c*delta)==0
    F=((1/c+x)/(1-x/c))/((1/b+y)/(1-y/b))
    W2=r*y/(R*x)*(1+x*c)**2/(1+y*b)**2
    quotient=s.factor((F-b/c*W2)/delta)
    assert s.factor(F-b/c*W2-quotient*delta)==0
    print('7 symbolic matrix/spectral/gluing identities passed')
    return quotient

if __name__=='__main__':
    print('Gluing discrepancy divided by curve difference:',exact_checks())
