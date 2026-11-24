"""Exact checks of the shifted contraction identities for residual restart maps."""
import sympy as S

def step(lam,w,s):
    x=S.symbols('x');m=lambda j:sum(a*t**j for a,t in zip(w,lam))
    H=S.Matrix(s,s,lambda i,j:m(i+j))
    c=H.inv()*S.Matrix([m(s+j) for j in range(s)])
    q=x**s-sum(c[j]*x**j for j in range(s))
    val=[q.subs(x,t) for t in lam]
    f=S.factor(sum(a*t*t for a,t in zip(w,val)))
    return q,f,[S.factor(a*t*t/f) for a,t in zip(w,val)]

def checks():
    x,t=S.symbols('x t')
    for s in range(1,5):
        lam=list(map(S.Rational,range(1,s+4)))
        w=[S.Rational((i+1)**2,sum((j+1)**2 for j in range(len(lam)))) for i in range(len(lam))]
        q,f,v=step(lam,w,s);p,g,u=step(lam,v,s)
        def st(a):return sum(aa/(ll+t) for aa,ll in zip(a,lam))
        C=S.factor(f*st(v)/(q.subs(x,-t)**2*st(w)))
        D=S.factor(g*st(u)/(p.subs(x,-t)**2*st(v)))
        # Orthogonality gives cancellation of one q(-t) factor.
        assert S.cancel(sum(ww*qq/(ll+t) for ww,qq,ll in zip(w,[q.subs(x,ll) for ll in lam],lam))-q.subs(x,-t)*st(v)*f/q.subs(x,-t)**2)==0
        for shift in [0,1,3,9]:
            assert C.subs(t,shift)>0
            assert D.subs(t,shift)>=C.subs(t,shift)
        # Product/ratio identity valid off poles.
        assert S.cancel(C*D-f*g*st(u)/(q.subs(x,-t)**2*p.subs(x,-t)**2*st(w)))==0
    print('Exact shifted-contraction identities and monotonicity checks passed for s=1..4.')
if __name__=='__main__':checks()
