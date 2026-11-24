import numpy as np

def replenishing_leaves(Q,N,alpha=None):
    assert Q>=10 and N>=0
    if alpha is None: alpha=100*Q
    out=[]
    r=np.sqrt(Q/2)
    S=3-1/Q
    s=(S+np.sqrt(S*S-8))/2
    t=2/s
    def leaf(a,b,th,prob):
        # Exact two-point det-one termination, including q=1.
        v=max(0.,a*a-a/b)
        big=a+np.sqrt(v)
        small=(a/b)/big
        for lam in (big,small):
            # alpha was chosen large, so lambda is the major eigenvalue.
            assert lam>=1
            out.append((prob/2,lam,th))
    def rec(a,b,th,prob,n):
        if n==0:
            leaf(a,b,th,prob);return
        gap=np.hypot(a-b,2*r)
        aa=(a+b+gap)/2
        bb=(Q/2)/aa
        ang=.5*np.arctan2(2*r,a-b)
        for sign in (-1,1):
            rec(s*aa,t*bb,th+sign*ang,prob/4,n-1)
            # Dead stretch child has determinant one.
            ad=(2-s)*aa;bd=(2-t)*bb
            assert abs(ad*bd-1)<1e-10
            leaf(ad,bd,th+sign*ang,prob/4)
    rec(alpha,Q/alpha,0.,1.,N)
    return np.array(out)

def characteristic(leaves,p):
    q=p/(p-1)
    prob,lam,theta=leaves.T
    N=len(lam)
    roots=[];inverses=[]
    for a,th in zip(lam,theta):
        c,s=np.cos(th),np.sin(th)
        U=np.array([[c,-s],[s,c]])
        roots.append((U*np.array([a**(1/p),a**(-1/q)]))@U.T)
        inverses.append((U*np.array([a**(-1/p),a**(1/q)]))@U.T)
    K=np.linalg.norm(np.einsum('iab,jbc->ijac',roots,inverses),ord=2,axis=(-2,-1))
    return np.sum(prob*np.sum(prob[None,:]*K**q,axis=1)**(p-1))

if __name__=='__main__':
    for Q in (10.,30.,100.):
        leaves=replenishing_leaves(Q,5)
        prob,lam,theta=leaves.T
        assert abs(prob.sum()-1)<1e-12
        # Check exact averages of the original determinant-one A2 weight.
        avg00=np.sum(prob*(lam*np.cos(theta)**2+np.sin(theta)**2/lam))
        avg11=np.sum(prob*(lam*np.sin(theta)**2+np.cos(theta)**2/lam))
        assert abs(avg00/(100*Q)-1)<1e-9
        assert abs(avg11/(.01)-1)<1e-7
        print('Q=',Q,'leaves=',len(lam),'root averages=',avg00,avg11)
        for p in (2.,3.,4.):
            A=characteristic(leaves,p)
            print(' p=',p,'root characteristic=',A,'normalized=',A/Q**max(1,p-1))
