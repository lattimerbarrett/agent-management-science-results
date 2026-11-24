"""Exact SymPy checks of least-norm formulation and coefficient transport.
The assertions are checked on rational examples for degrees 1,...,4.
"""
import sympy as S

def least_norm_step(x,lam,s):
    C=S.Matrix.hstack(*[S.diag(*[t**j for t in lam])*x for j in range(s+1)])
    rhs=S.zeros(s+1,1);rhs[s]=1
    coeff=(C.T*C).inv()*rhs
    y=C*coeff
    assert C.T*y==rhs
    return y,coeff
for s in range(1,5):
    n=2*s+3
    lam=list(map(S.Integer,range(1,n+1)))
    x=S.Matrix([S.Rational(i+2,n+3) for i in range(n)])
    y,Q=least_norm_step(x,lam,s)
    xp,P=least_norm_step(y,lam,s)
    yp,Qp=least_norm_step(xp,lam,s)
    d=xp-x;e=yp-y
    assert S.factor((x.T*x)[0]-(xp.T*xp)[0]-(d.T*d)[0])==0
    A=S.diag(*lam)
    for j in range(s+1):
        assert S.factor((d.T*A**j*y)[0])==0
        lhs=((sum(((Qp[t]-Q[t])*A**t for t in range(s+1)),S.zeros(n))*xp).T*A**j*xp)[0]
        rhs=-(d.T*sum((Q[t]*A**t for t in range(s+1)),S.zeros(n))*A**j*d)[0]
        assert S.factor(lhs-rhs)==0
    C=S.Matrix.hstack(*[A**j*xp for j in range(s+1)])
    Proj=C*(C.T*C).inv()*C.T
    assert e==(S.eye(n)-Proj)*sum((Q[t]*A**t for t in range(s+1)),S.zeros(n))*d
print('Exact least-norm / coefficient-transport checks passed for s=1,...,4.')
