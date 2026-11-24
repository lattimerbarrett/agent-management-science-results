"""Exact rational checks and high-precision Fourier block checks.
Run with Python; requires mpmath (no external programs).
The proof uses arbitrary k; finite runs verify algebra and example signs.
"""
from fractions import Fraction as F
import mpmath as mp

def exact_checks():
    # t is the unique positive root of t*t+2*(height/radius)*t-1.
    data=[(F(10),F(1),F(49,1000),F(51,1000)),
          (F(10001,1000),F(10),F(41,100),F(42,100)),
          (F(1,10),F(1),F(904,1000),F(906,1000)),
          (F(99,1000),F(10),F(990,1000),F(991,1000))]
    for h,r,lo,hi in data:
        f=lambda t:t*t+2*h/r*t-1
        assert f(lo)<0<f(hi)
    xl,xh=data[0][2:]; yl,yh=data[1][2:]
    ul,uh=data[2][2:]; vl,vh=data[3][2:]
    assert ul**3>xh and ul**2*vl>yh
    # Uniform lower bound for logarithmic derivative of K on [u,v].
    assert (yl-xh)/((1+xh)*(1+yh))-(vh-ul)>0
    return True

def conv(a,b):
    c=[mp.mpc(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def core(k,x,u):
    a=[mp.binomial(k,j)*x**(k-j) for j in range(k+1)]
    b=[mp.binomial(k,j)*u**j for j in range(k+1)]
    return conv(a,b)

def geometry(scale=1):
    r=mp.mpf(scale); R=10*r; H=mp.mpf(1)/1000
    t=lambda h,r:r/(h+mp.sqrt(h*h+r*r))
    return r,R,H,t(10,r),t(10+H,R),t(mp.mpf(1)/10,r),t(mp.mpf(1)/10-H,R)

def rows(m,k,scale=1):
    assert k%m==0
    r,R,H,x,y,u,v=geometry(scale)
    Fm=[mp.mpc(1)]; C=[mp.mpc(1)]; E=[mp.mpc(1)]
    for j in range(1,m):
        Fm=conv(Fm,[1,1j*mp.exp(-mp.pi*1j*j/m)])
    for j in range(m):
        z=mp.exp(2j*mp.pi*j/m)
        d=H+mp.sqrt(H*H+r*r+R*R-2*r*R*mp.re(z))
        C=conv(C,[1,-(R/z-r)/d])
        E=conv(E,[(R-r*z)/d,1])
    A=conv(conv(Fm,C),core(k,x,u))
    B=conv(conv(Fm,E),core(k,y,v))
    for P in [A,B]:
        assert max(abs(mp.im(t)) for t in P)<mp.mpf('1e-65')*max(abs(t) for t in P)
    return list(map(mp.re,A)),list(map(mp.re,B)),(x,y,u,v)

def blocks(m,k,scale=1):
    A,B,(x,y,u,v)=rows(m,k,scale)
    n=2*k+2*m; result=[]
    for s in range(m):
        V=[]
        for t in [u,v]:
            w=[mp.mpf(0)]*n
            for e in range(k+s,n,m):w[e]=t**(e-k)
            for e in range(k+s-m,-1,-m):
                w[e]=(x**m+y**m)*w[e+m]-(x*y)**m*w[e+2*m]
            V.append(w)
        W=mp.matrix([[mp.fdot(P,w) for w in V] for P in [A,B]])
        # Positive normalization prevents gigantic output, preserves sign.
        norm=mp.sqrt(sum(z*z for z in W))
        result.append(mp.det(W/norm))
    return result

if __name__=='__main__':
    assert exact_checks()
    mp.mp.dps=100
    print('All exact rational inequalities certified.')
    for m in [1,2,3]:
        k=600 # divisible by all these m
        neg=blocks(m,k)
        pos=blocks(m,k,mp.mpf('1e-8'))
        assert all(t<0 for t in neg), (m,neg)
        assert all(t>0 for t in pos), (m,pos)
        print('m=',m,'k=',k,'negative blocks:',[mp.nstr(t,8) for t in neg],
              'positive reference:',[mp.nstr(t,8) for t in pos])
