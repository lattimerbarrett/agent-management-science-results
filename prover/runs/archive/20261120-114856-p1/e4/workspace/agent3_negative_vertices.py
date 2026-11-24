import numpy as np,itertools
from numpy.polynomial import Polynomial as P
x=P([0,1]);beta=13/8;gamma=7/4
q=(x*x-1)*(x-beta)*(x+gamma);r=(x*x-1)*(x+beta)*(x-gamma);H=10125/65536;Q=q*r;poly=Q-H;l=np.sort(poly.roots());extras=np.array([-np.sqrt(23/8),np.sqrt(23/8)])
V=np.vander(l,4,increasing=True);fext=np.vander(extras,4,increasing=True);qv=q(l);rv=r(l)
for bits in itertools.product([0,1],repeat=3):
    ix=[0,1+bits[0],3+bits[1],5+bits[2],7]
    A=np.vstack([np.ones(5),(qv[ix,None]*V[ix]).T]);w=np.zeros(8);w[ix]=np.linalg.solve(A,np.r_[1.,np.zeros(4)])
    assert min(w)>-1e-9
    G=V.T@(w[:,None]*V);wp=w*qv*qv/H;Gp=V.T@(wp[:,None]*V)
    drmap=-np.linalg.solve(Gp,G)
    Fmap=rv[:,None]*V+qv[:,None]*V@drmap
    deh=w@Fmap;Emap=Fmap-deh
    assert np.max(np.abs(Emap[ix]))<1e-5
    Fext=r(extras)[:,None]*fext+q(extras)[:,None]*fext@drmap
    Cf=4*np.linalg.solve(G,(q(extras)[:,None]*fext).T)
    L=(Fext+deh)@Cf/H
    eta=np.linalg.solve(L,np.ones(2));v=Cf@eta
    growth=2*Emap@v/H
    gr=[growth[1+(1-bits[0])],growth[3+(1-bits[1])],growth[5+(1-bits[2])]]
    print(bits,'eta',eta,'edge',np.round(gr,5))
