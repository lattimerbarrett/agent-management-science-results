import numpy as np
from pathlib import Path
module='''import numpy as np

def cantormodel(p,Q,N):
    q=p/(p-1);rho=1/8;ea=1/Q;ec=Q**(-1/(p-1));r=Q**(1/p)
    sa=(1-ea)/rho;sc=(1-ec)/rho;da=ea/(1-rho);dc=ec/(1-rho)
    leaves=[]
    def rec(l,L,a,c,z,n):
        delta=r/(a**(1/p)*c**(1/q))
        if n==N:leaves.append((l,l+L,a,c,z,n,False));return
        for u,v,t in [(0,1/4,-2),(5/16,11/16,0),(3/4,1,2)]:
            leaves.append((l+u*L,l+v*L,da*a,dc*c,z+t*delta,n,True))
        rec(l+L/4,L/16,sa*a,sc*c,z-delta,n+1)
        rec(l+11*L/16,L/16,sa*a,sc*c,z+delta,n+1)
    rec(0,1,1,1,0,0)
    return sorted(leaves,key=lambda x:x[0])

def interval_bound(leaves,p,ends):
    l=np.array([x[0] for x in leaves]);rr=np.array([x[1] for x in leaves]);lens=rr-l
    a=np.array([x[2] for x in leaves]);c=np.array([x[3] for x in leaves]);z=np.array([x[4] for x in leaves]);
    vals=np.array([a,a**(-1/(p-1)),c**(-(p-1)),c]).T
    pref=np.vstack([np.zeros(4),np.cumsum(vals*lens[:,None],axis=0)])
    def primitive(x):
        i=min(np.searchsorted(rr,x,side='right'),len(l)-1)
        return pref[i]+(x-l[i])*vals[i]
    best=(0,None)
    for s,t in ends:
        if t<=s:continue
        avg=(primitive(t)-primitive(s))/(t-s)
        i=min(np.searchsorted(rr,s,side='right'),len(l)-1)
        j=max(0,np.searchsorted(l,t,side='left')-1)
        osc=z[j]-z[i]
        term=avg[0]*avg[1]**(p-1)+avg[2]*avg[3]**(p-1)+osc**p*avg[0]*avg[3]**(p-1)
        if term>best[0]:best=(term,(s,t))
    return best

def H_test(leaves,p,Q,N):
    q=p/(p-1);ea=1/Q;ec=Q**(-1/(p-1));ac=1-ec
    l=np.array([x[0] for x in leaves]);rr=np.array([x[1] for x in leaves]);L=rr-l
    a=np.array([x[2] for x in leaves]);c=np.array([x[3] for x in leaves]);z=np.array([x[4] for x in leaves]);n=np.array([x[5] for x in leaves]);dead=np.array([x[6] for x in leaves]);
    psi=(ec*ac**n)**(-1/p)*dead;h=c*psi
    inp=np.sum(L*c*psi**p)
    out=0.
    # Log1p form avoids cancellation when source intervals are very tiny/far.
    for pt,wt in zip(*np.polynomial.legendre.leggauss(5)):
        x=(l+rr)/2+pt*L/2
        den=x[:,None]-rr[None,:]
        with np.errstate(invalid='ignore',divide='ignore'):
            K=np.log(np.abs(1+L[None,:]/den))/np.pi
        K[np.diag_indices(len(l))]=0
        potential=np.sum(K*(z[:,None]-z[None,:])*h[None,:],axis=1)
        assert np.min(potential)>-1e-6
        out+=wt/2*np.sum(L*a*potential**p)
    return (out/inp)**(1/p),inp
'''
Path('workspace/agent3_cantor_model.py').write_text(module)
exec(module)
rng=np.random.default_rng(234)
for p,Q in [(2,10),(3,10),(3,30),(1.5,10)]:
    N=7;leaves=cantormodel(p,Q,N)
    assert all(leaves[i][4]<=leaves[i+1][4]+1e-12 for i in range(len(leaves)-1))
    assert abs(sum((y-x)*a for x,y,a,c,z,n,d in leaves)-1)<1e-10
    assert abs(sum((y-x)*c for x,y,a,c,z,n,d in leaves)-1)<1e-10
    ends=list(np.sort(rng.random((10000,2)),axis=1))
    for j in range(len(leaves)-1):
        b=leaves[j][1];ell=min(b-leaves[j][0],leaves[j+1][1]-b)
        for frac in [.01,.5,1,2,10]:
            ends.append((max(0,b-frac*ell),min(1,b+frac*ell)))
    bound,loc=interval_bound(leaves,p,ends)
    ratio,inp=H_test(leaves,p,Q,N)
    print('p,Q,N,leaves',p,Q,N,len(leaves),'max interval upper surrogate',bound,'ratio/Q',bound/Q,'loc',loc,'H ratio',ratio,'input^p',inp,flush=True)
