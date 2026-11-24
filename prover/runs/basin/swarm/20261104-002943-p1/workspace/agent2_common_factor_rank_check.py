import sympy as S
x,t=S.symbols('x t');s=4
cases=[
(S.prod(x-a for a in [-5,-2,1,4]),S.prod(x-a for a in [-4,-1,2,5]),(x+3)*x*(x-3)),
(S.prod(x-a for a in [-5,-2,1,4]),S.prod(x-a for a in [-4,-1,1,5]),(x+3)*x*(x-3)),
((x*x-1)*(x*x-4),(x*x-1)*(x*x-9),x*(x*x-S.Rational(9,4))),
((x+3)*(x+1)*(x-1)*(x-4),(x+3)*(x+1)*(x-1)*(x-5),(x+2)*x*(x-S.Rational(5,2))),
((x*x-1)*(x*x-4),(x*x-1)*(x*x-4),x**3-S.Rational(5,2)*x)]
for P,Q,f in cases:
    P,Q,f=map(S.expand,[P,Q,f]);C=S.Integer(1);D=P*Q-C
    assert S.Poly(D,x).count_roots(-S.oo,S.oo)==8
    intervals=S.Poly(D,x).intervals(eps=S.Rational(1,10**15))
    assert len(intervals)==8 and all(mult==1 for _,mult in intervals)
    for j in range(7):
        assert S.Poly(f*Q,x).count_roots(intervals[j][0][1],intervals[j+1][0][0])==1
    def gram(num):
        gg=S.series((num/D).subs(x,1/t)/t,t,0,7).removeO().expand()
        mom=[gg.coeff(t,j) for j in range(7)]
        M=S.Matrix(4,4,lambda i,j:mom[i+j])
        assert all(M[:j,:j].det()>0 for j in range(1,5))
        return M
    M=gram(f*Q);N=gram(f*P);d=S.Matrix([S.Poly(P-Q,x).nth(j) for j in range(4)])
    E=S.zeros(8,4)
    for j in range(4):
        a=S.eye(4)[:,j];b=-N.inv()*M*a;dc=-(a.T*M*d)[0]
        dr=S.expand(Q*x**j+P*sum(b[k]*x**k for k in range(4))-dc)
        for k in range(8):E[k,j]=dr.coeff(x,k)
    c=S.degree(S.gcd(P,Q),x);expected=3 if c==0 else 4-c
    assert E.rank()==expected
    print('common degree',c,'exact simplex shear rank',expected,'checked via rational Stieltjes moments')
