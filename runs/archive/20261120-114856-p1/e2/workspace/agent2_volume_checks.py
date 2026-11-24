import sympy as S

def check(n,s):
    lam=list(map(S.Integer,range(1,n+1)))
    w=[S.Rational(i+2,sum(range(2,n+2))) for i in range(n)]
    X=S.Matrix([[li**j for j in range(s)]for li in lam])
    W=S.diag(*w); H=X.T*W*X
    ls=S.Matrix([li**s for li in lam]);c=-H.inv()*X.T*W*ls
    q=ls+X*c; h=(q.T*W*q)[0]
    # derivative of unnormalized v_i=q_i*y_i in dy coordinates,
    # conjugated by diag(y) to eliminate square roots:
    # diag(y)^-1 Dv diag(y)=(I-2 K W)diag(q).
    K=X*H.inv()*X.T
    B=(S.eye(n)-2*K*W)*S.diag(*q)
    assert S.factor(B.det()-(-1)**s*S.prod(q))==0
    # Homogeneity and orthogonality make radial derivative v itself.
    assert B*S.ones(n,1)==q
    # Reflection matrix squares to I and has s negative eigenvalues.
    R=S.eye(n)-2*K*W
    assert R*R==S.eye(n)
    assert S.factor(R.det()-(-1)**s)==0

if __name__=='__main__':
    for n in range(3,8):
        for s in range(1,min(n,4)):check(n,s)
    print('Exact reflection derivative and determinant checks passed.')
