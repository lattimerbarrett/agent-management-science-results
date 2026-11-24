"""Exact rational geometry certificates and optional high-precision block checks.
Run: python agent3_certificates.py [--numerical]
No claim of existence rests on floating point: asymptotic proof is separate.
"""
from fractions import Fraction as F

def parameter_interval(z,t,lo,hi):
    # s=t/(z+sqrt(z*z+t*t)) is the positive root of t*s*s+2*z*s-t.
    poly=lambda s:t*s*s+2*z*s-t
    assert 0<lo<hi<1 and poly(lo)<0<poly(hi)
    return lo,hi

def exact_certificates():
    # lambda=-10,hA=0,hB=1/1000,mu=1/10,r=1,R=10.
    I={
      'x':parameter_interval(F(10),F(1),F(49,1000),F(50,1000)),
      'y':parameter_interval(F(10001,1000),F(10),F(414,1000),F(415,1000)),
      'u':parameter_interval(F(1,10),F(1),F(904,1000),F(906,1000)),
      'v':parameter_interval(F(99,1000),F(10),F(990,1000),F(991,1000))}
    x,y,u,v=(I[k] for k in ('x','y','u','v'))
    assert x[1]<y[0]<y[1]<u[0]<u[1]<v[0]<1
    assert u[0]**3>x[1] and u[0]**2*v[0]>y[1]
    # For all z in [u,v], derivative log rho(z)>0.
    derivative_numerator_lower=(y[0]-x[1])-(v[1]-u[0])*(1+x[1])*(1+y[1])
    assert derivative_numerator_lower>0
    print('EXACT rational certificates passed:',I)
    print('rho derivative numerator lower bound =',derivative_numerator_lower)
    return I

def numerical_blocks(m,A,dps=100):
    import mpmath as mp
    mp.mp.dps=dps
    assert A % m == 0
    one=mp.mpf(1); H=one/1000
    f=lambda z,t:t/(z+mp.sqrt(z*z+t*t))
    x,y,u,v=f(mp.mpf(10),one),f(10+H,mp.mpf(10)),f(one/10,one),f(one/10-H,mp.mpf(10))
    def mul(p,q):
        out=[mp.mpc(0)]*(len(p)+len(q)-1)
        for i,pi in enumerate(p):
            for j,qj in enumerate(q):out[i+j]+=pi*qj
        return out
    intra=[one];C=[one];E=[one]
    for k in range(1,m):intra=mul(intra,[1,mp.j*mp.exp(-mp.pi*mp.j*k/m)])
    for k in range(m):
        z=mp.exp(2*mp.pi*mp.j*k/m)
        D=H+mp.sqrt(H*H+1+100-20*mp.re(z))
        C=mul(C,[1,-(10/z-1)/D]);E=mul(E,[(10-z)/D,1])
    PA=mul(intra,C);PB=mul(intra,E)
    for _ in range(A):
        PA=mul(PA,[x,1]);PA=mul(PA,[1,u])
        PB=mul(PB,[y,1]);PB=mul(PB,[1,v])
    # Axis annihilators on each residue: initial upper mode t^(e-A),
    # then extend through v_e=(x^m+y^m)v_(e+m)-(xy)^m v_(e+2m).
    X,Y=x**m,y**m
    vals=[]
    for s in range(m):
        es=list(range(s,len(PA),m)); ix=next(i for i,e in enumerate(es) if e>=A)
        row=[]
        for t in (u,v):
            w=[mp.mpf(0)]*len(es)
            for i in range(ix,len(es)):w[i]=t**(es[i]-A)
            for i in reversed(range(ix)):w[i]=(X+Y)*w[i+1]-X*Y*w[i+2]
            row.append([mp.re(sum(P[e]*w[i] for i,e in enumerate(es))) for P in (PA,PB)])
        a,b=row
        determinant=a[0]*b[1]-b[0]*a[1]
        vals.append(determinant)
    print('m=%d A=%d block signs:'%(m,A),[mp.sign(d) for d in vals])
    return vals

if __name__=='__main__':
    import sys
    exact_certificates()
    if '--numerical' in sys.argv:
        for m in range(1,6):numerical_blocks(m,600)
