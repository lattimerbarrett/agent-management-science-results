"""Exact reverse-radii RHP boundary inequality; no numerical claim substitutes for algebra."""
import sympy as sp
import mpmath as mp
import random

def exact_check():
    L, beta, k, C, S = sp.symbols('L beta k C S', real=True)
    alpha = L**2*(beta-1)-1
    E=(L*beta-k*(L*C+S))**2-(alpha*beta+k*k-k*(alpha+beta)*C)
    target=(beta-k*C)*(L*L+1-k*((L*L-1)*C+2*L*S))
    rem=sp.Poly(sp.expand(E-target),S).rem(sp.Poly(S*S+C*C-1,S)).as_expr()
    assert sp.expand(rem)==0
    # This is the amplitude identity establishing strict positivity of second factor.
    assert sp.expand((L*L-1)**2+4*L*L-(L*L+1)**2)==0
    B,r,t,p,q=sp.symbols('B r t p q',real=True)
    K=B*p+r*q; U=r*p+B*q; A=r-B
    rem=sp.expand(K*K-U*U-t*t*A*A-A*A*((B+r)**2-t*t))
    rem=sp.rem(sp.Poly(rem,q),sp.Poly(q*q-r*r+t*t,q)).as_expr()
    rem=sp.rem(sp.Poly(rem,p),sp.Poly(p*p-B*B+t*t,p)).as_expr()
    assert sp.expand(rem)==0
    # t=0: G=s^2 and s^2-A^2=2rB(1-kC)>0.
    s2=B*B+r*r-2*r*k*B*C
    assert sp.expand(s2-(r-B)**2-2*r*B*(1-k*C))==0
    return {'exact_identities':4,'passed':True}

def numerical_check(cases=1000,dps=80):
    mp.mp.dps=dps; rng=random.Random(265)
    worst=mp.inf; worstfactor=mp.inf
    for _ in range(cases):
        h=mp.exp(mp.mpf(rng.uniform(-12,12)))
        u=mp.exp(mp.mpf(rng.uniform(-5,3)))
        v=u+mp.exp(mp.mpf(rng.uniform(-5,3)))
        k=1/(1+mp.exp(mp.mpf(rng.uniform(-12,12))))
        theta=mp.mpf(rng.uniform(-3.14159,3.14159))
        sign=rng.choice([-1,1]); t=sign*h
        B=h*mp.cosh(u); r=h*mp.cosh(v)
        p=h*mp.sinh(u); q=h*mp.sinh(v); A=r-B
        C=mp.cos(theta); S=mp.sin(theta)
        K=B*p+r*q; U=r*p+B*q
        G=K-k*(U*C+t*A*S)
        s2=p*p+r*r+k*k*t*t-2*r*k*B*C
        beta=mp.cosh(v-u)
        L=mp.cosh((u+v)/2)/mp.sinh((v-u)/2)
        target=(beta-k*C)*(L*L+1-k*((L*L-1)*C+2*L*sign*S))
        actual=(G*G-A*A*s2)/(A*A*t*t)
        err=abs(actual-target)/max(1,abs(target))
        assert err < mp.mpf('1e-45'), (err,u,v,k,theta)
        defect=G-A*mp.sqrt(s2)
        assert defect>0 and target>0
        worst=min(worst,defect/max(1,K)); worstfactor=min(worstfactor,target)
    return {'cases':cases,'digits':dps,'smallest_scaled_defect':str(worst),'smallest_factor_product':str(worstfactor)}

if __name__=='__main__':
    print(exact_check()); print(numerical_check())
