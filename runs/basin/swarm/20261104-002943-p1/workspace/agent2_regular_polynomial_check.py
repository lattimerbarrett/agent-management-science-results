import sympy as S

def check(s,nodes,P,Q,C,f):
    X=S.symbols('X');m=len(nodes);V=S.Matrix([[x**j for j in range(s)] for x in nodes]);p=S.Matrix([P.subs(X,x) for x in nodes]);q=S.Matrix([Q.subs(X,x) for x in nodes]);D=S.prod(X-x for x in nodes)
    w=S.Matrix([C*f.subs(X,x)/(S.diff(D,X).subs(X,x)*p[i]) for i,x in enumerate(nodes)])
    assert min(w)>0 and sum(w)==1 and V.T*S.diag(*w)*p==S.zeros(s,1)
    assert all(p[i]*q[i]==C for i in range(m))
    def DF(w,p):
        M=V.T*S.diag(*w)*V;DP=-M.inv()*V.T*S.diag(*p)
        h=(w.T*p.applyfunc(lambda a:a*a))[0]
        raw=S.diag(*p.applyfunc(lambda a:a*a))+2*S.diag(*[w[i]*p[i] for i in range(m)])*V*DP
        dh=S.ones(1,m)*raw
        return raw/h-(S.diag(*w)*p.applyfunc(lambda a:a*a))*dh/h**2,DP
    A,DP=DF(w,p);zz=S.diag(*w)*p.applyfunc(lambda a:a*a)/C;B,_=DF(zz,q);J=S.simplify(B*A);N=J-S.eye(m)+w*S.ones(1,m)
    assert DP.rank()==s and N.rank()==m-s-1
    assert S.simplify(DP*N)==S.zeros(s,m)
    assert S.simplify(N*N)==S.zeros(m,m)
    print('s,m=',s,m,'cycle positivity, derivative ranks, polynomial stationarity and square-zero shear checked')

if __name__=='__main__':
    X=S.symbols('X')
    check(2,[-8,-1,1,8],X**2+3*X-28,X**2-3*X-28,S.Integer(720),X-S.Rational(1,7))
    P=X**3-7*X-5;Q=P+10
    check(3,[-3,-2,1,3],P,Q,S.Integer(11),S.Integer(1))
    check(3,[-3,-2,1,2,3],P,Q,S.Integer(11),X-S.Rational(3,2))
    check(3,[-3,-2,-1,1,2,3],P,Q,S.Integer(11),X**2-S.Rational(9,4))
    P=X**4-65*X**2+294;Q=P+260
    check(4,[-8,-7,-1,4,8],P,Q,S.Integer(112700),S.Integer(1))
