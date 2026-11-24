import sympy as S
x=S.symbols('x')
for s in range(1,5):
    n=s+1
    J=S.diag(*[S.Integer(i+1) for i in range(n)])
    beta=[S.Integer(i+1) for i in range(s)]
    for i,b in enumerate(beta):J[i,i+1]=J[i+1,i]=b
    cp=lambda M:(x*S.eye(M.rows)-M).det(method='domain-ge') if M.rows else S.Integer(1)
    P=cp(J[:-1,:-1]);Q=cp(J[1:,1:]);D=cp(J);R=cp(J[1:-1,1:-1]);C=S.prod(b*b for b in beta)
    assert S.expand(P*Q-C-D*R)==0
    # Monic Lanczos identity P(J)e1=(product beta) e_{s+1}.
    vals=S.Poly(P,x).all_coeffs();v=S.zeros(n,1);e=S.eye(n)[:,0]
    for a in vals:v=J*v+a*e
    assert v==S.prod(beta)*S.eye(n)[:,-1]
    print('s=',s,'Desnanot-Jacobi and normalized-residual endpoint identities verified')
