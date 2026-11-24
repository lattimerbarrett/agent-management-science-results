import numpy as np
from scipy.linalg import solve
CORE=np.array([-3.,-1.,1.,2.,3.]);EXTRA=np.array([0.,np.sqrt(7.)]);h=18.;d=3*np.sqrt(2.)
f=lambda x:x**3-7*x
p=lambda x:f(x)+d
q=lambda x:f(x)-d
DCORE=1/np.prod(np.where(np.eye(5,dtype=bool),1,CORE[:,None]-CORE[None,:]),axis=1)
Lc=np.array([np.ones(5),CORE,CORE**2]).T
Le=np.array([np.ones(2),EXTRA,EXTRA**2]).T

def data(theta,a):
    w=DCORE*q(CORE)*(CORE-theta)
    wt=-DCORE*q(CORE)
    H=(Lc.T*w)@Lc
    # Gauge choice does not affect b or V.
    Z=np.vstack([np.ones(5),(Lc.T*p(CORE))])
    rhs=np.r_[0.,-H@a]
    dw=np.linalg.lstsq(Z,rhs,rcond=None)[0]
    E=np.dot(w,(Lc@a)*(p(CORE)-q(CORE)))
    wp=w*p(CORE)**2/h
    dwp=(dw*p(CORE)**2+2*w*p(CORE)*(Lc@a)+wp*E)/h
    H1=(Lc.T*wp)@Lc
    b=-np.linalg.solve(H1,Lc.T@(dwp*q(CORE)))
    Rc=q(CORE)*(Lc@a)+p(CORE)*(Lc@b)+E
    Re=q(EXTRA)*(Le@a)+p(EXTRA)*(Le@b)+E
    V=np.dot(wt,2*w*Rc/h)/np.dot(wt,wt)
    return w,wt,H,dw,E,b,Rc,Re,V

def rhs(t,y,rescaled=True):
    # y=(theta,a0,a1,a2,M0,M1). rescaled=True is tau=log k,
    # A=k*a, M=k^2*physical mass and hence includes +A,+2M.
    theta=y[0];a=np.array(y[1:4]);M=np.array(y[4:6])
    w,wt,H,dw,E,b,Rc,Re,V=data(theta,a)
    adot=-np.linalg.solve(H,Lc.T@(w*Rc**2*p(CORE))/h**2+4*Le.T@(M*p(EXTRA)))
    mdot=(4*E-2*Re)/h*M
    if rescaled:adot+=a;mdot+=2*M
    return np.r_[V,adot,mdot]

def step(lam,w):
    L=np.array([np.ones(len(lam)),lam,lam**2]).T
    cc=-np.linalg.solve((L.T*w)@L,L.T@(w*lam**3))
    Q=lam**3+L@cc;F=np.dot(w,Q*Q)
    return w*Q*Q/F,cc

if __name__=='__main__':
    th=1.5;a=np.array([.02,-.01,.015]);M=np.array([.03,.04]);y=np.r_[th,a,M]
    w,wt,H,dw,E,b,Rc,Re,V=data(th,a)
    assert min(w)>0 and abs(sum(w)-1)<1e-12
    assert np.linalg.norm(Lc.T@(w*p(CORE)))<1e-11
    assert np.linalg.norm(2*w*Rc/h-wt*V)<1e-11
    expected=rhs(0,y,rescaled=False)
    print('ODE',expected)
    for eps in [.01,.005,.0025]:
        ww=np.r_[(w+eps*dw)*(1-eps**2*sum(M)),eps**2*M]
        lam=np.r_[CORE,EXTRA]
        w1,c0=step(lam,ww);w2,c1=step(lam,w1);w3,c2=step(lam,w2)
        obs=np.r_[np.dot(wt,w2[:5]-ww[:5])/np.dot(wt,wt)/eps,(c2-c0)/eps**2,(w2[5:]-ww[5:])/eps**3]
        print('eps',eps,'error',np.max(abs(obs-expected)))
    print('The ODE is the analytically-derived leading Taylor field; printed finite-epsilon errors are an independent numerical check.')
