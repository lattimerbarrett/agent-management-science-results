import sympy as S
j,n=S.symbols('j n')
alpha=(n+2)/2
D=(j+1)*(j+n+1)
Qs=[]
for k in range(3):
    cs=S.symbols('c:'+str(2*k+1))
    Q=sum(cs[i]*j**i for i in range(len(cs)))
    expr=S.Poly(S.expand((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(j+alpha)*D**k),j)
    sol=S.solve(expr.all_coeffs(),cs)
    Q=S.factor(Q.subs(sol))
    assert S.simplify((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(j+alpha)*D**k)==0
    Qs.append(Q)
    print('k=',k,'Q=',Q)
R0=S.gamma(S.Rational(3,2))**2/S.gamma((n+1)/2)**2
R1=1/S.gamma((n+2)/2)**2
mom=[S.factor((n-1)**2*Q.subs(j,0)*R0+n**2*Q.subs(j,1)*R1) for Q in Qs]
for k,M in enumerate(mom): print('M',k,'=',M)
