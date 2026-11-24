"""Exact identities for the m1 RHP Schur cocycle, plus complex checks.
This proves a kernel lemma, NOT the required determinant/Pick identification.
"""
import sympy as s
import numpy as np

def exact_check():
    x,y,c,ss=s.symbols('x y c ss')
    H=lambda t:(t-c)*(1+c*t)/t
    phi=lambda t:(t-c)/(1+c*t)
    velocity=-y*(y-c)*(1+c*y)/(c*(1+y*y))
    target=-(1+c*c)*y/(c*(1+y*y))
    assert s.factor(s.diff(phi(y),y)*velocity/phi(y)-target)==0
    ww=ss*y/x*((1+c*x)/(1+c*y))**2
    identity=s.factor(ww-phi(y)/phi(x))
    numerator=s.together(identity).as_numer_denom()[0]
    relation=s.together(H(y)-ss*H(x)).as_numer_denom()[0]
    assert s.rem(s.Poly(numerator,ss),s.Poly(relation,ss)).as_expr()==0
    u,v=s.symbols('u v',real=True);t=u+s.I*v
    assert s.simplify(s.re(t/(1+t*t))-u*(1+u*u+v*v)/abs(1+t*t)**2)==0
    return True

def complex_checks(trials=2000,seed=203):
    rng=np.random.default_rng(seed);maximum=0.
    for _ in range(trials):
        c=np.exp(rng.uniform(-6,0));rr=np.exp(rng.uniform(-4,2));ss=np.exp(rng.uniform(-5,0))
        R=rr/ss;d=(R-rr)*(1-c*c)/(2*c)
        z=np.exp(rng.uniform(-6,4))+1j*rng.normal(0,np.exp(rng.uniform(-4,4)))
        x=rr/(z+np.sqrt(z*z+rr*rr));y=R/(z+d+np.sqrt((z+d)**2+R*R))
        w=np.sqrt(ss*y/x)*(1+c*x)/(1+c*y)
        assert abs(w)<1+1e-10
        maximum=max(maximum,abs(w))
    return dict(trials=trials,max_abs=maximum)

if __name__=='__main__':print(exact_check(),complex_checks())
