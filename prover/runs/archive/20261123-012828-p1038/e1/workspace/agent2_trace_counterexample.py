"""Exact actual-configuration counterexample to a proposed residual-trace lemma.
This does not contradict the problem's desired theorem.
"""
import sympy as s

def check():
    T,c,x0,x1,y0,y1=s.symbols("T c x0 x1 y0 y1")
    rows=[(1-x0*T)*(1-y0*T),T*(1-x1*T)*(1-y1*T),
          (1-c*T)*(T+x0)*(T+x1),(T+c)*(T+y0)*(T+y1)]
    M=s.Matrix([[s.expand(p).coeff(T,j) for j in range(4)] for p in rows])
    D=s.expand(M.det())
    E=s.expand(D-(1+c*c)*(1+x0*x0)*(1+x1*x1)*(1+y0*y0)*(1+y1*y1))
    trace=s.expand(E.coeff(y1,0)+E.coeff(y1,2))
    cc=s.Rational(1,40);xx0=s.Rational(1,4);xx1=s.Integer(100);yy0=s.Rational(3,40)
    H=lambda t:(t-cc)*(1+cc*t)/t
    rr=s.factor(H(yy0)/H(xx0));R=s.Integer(1)
    d=s.factor((R-rr)*(1-cc*cc)/(2*cc))
    lam=s.factor(rr*(xx0-1/xx0)/2)
    mu=s.factor(rr*(xx1-1/xx1)/2)
    assert 0<rr<R and lam<0<d<mu
    assert lam==d+(yy0-1/yy0)/2
    z=rr*H(xx1)-(1-cc*cc)
    yy1=(z+s.sqrt(z*z+4*cc*cc))/(2*cc)
    assert rr*H(xx1)>H(1) # H increasing, hence yy1>1.
    assert s.simplify(H(yy1)-rr*H(xx1))==0
    ans=s.factor(trace.subs({c:cc,x0:xx0,x1:xx1,y0:yy0}))
    assert ans==s.Rational(3737615359,20480000)>0
    return {"r":str(rr),"R":1,"d":str(d),"lambda":str(lam),"mu":str(mu),
            "y1":str(s.N(yy1,40)),"positive_residual_I_trace":str(ans)}

if __name__=="__main__":print(check())
