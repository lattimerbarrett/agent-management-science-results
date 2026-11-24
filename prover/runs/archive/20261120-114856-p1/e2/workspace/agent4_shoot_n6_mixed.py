import numpy as np
be=18/729;t=1e-8;gam=.5
core=np.array([-3.,-2.,-1.,1.,2.,3.])/3
eta=core[1];lam=np.sort(np.r_[np.delete(core,1),0]);n=6;zi=2
d7=1/np.prod(np.where(np.eye(n,dtype=bool),1,lam[:,None]-lam[None,:]),axis=1)
V=np.vander(lam,3,increasing=True);rhs=lam**3;lr=lam*(lam-gam)
chi=np.polynomial.polynomial.polyfromroots(core);chi[0]+=be
rr=np.polynomial.polynomial.polyroots(chi)
target=np.polynomial.polynomial.polyfromroots(rr[[0,2,5]])[:3]
def init(c):
 q=rhs+V@c;delta=2*be*t*q[zi]/eta;S0=sum(d7/q);S1=sum(d7*lr/q);F=(1-delta*S0)/S1
 W=d7*(F*lr+delta)/q
 ds=2*be*t*V[zi]/eta;dS0=-(d7/q**2)@V;dS1=-(d7*lr/q**2)@V
 dF=-(ds*S0+delta*dS0+F*dS1)/S1
 dW=d7[:,None]*((lr[:,None]*dF+ds)/q[:,None]-(F*lr+delta)[:,None]*V/q[:,None]**2)
 return W,dW
def run(c,N,jac=True,save=False):
 W,D=init(c);hist=[]
 for k in range(2*N):
  M=V.T@(W[:,None]*V);co=np.linalg.solve(M,-V.T@(W*rhs));p=rhs+V@co;F=sum(W*p*p)
  if jac:
   dc=np.linalg.solve(M,-V.T@(p[:,None]*D));dF=(p*p)@D
   D=(p*p/F)[:,None]*D+(2*W*p/F)[:,None]*(V@dc)-(W*p*p/F**2)[:,None]*dF
  W=W*p*p/F
  if save and k%max(2,2*N//200)==0:hist.append(W.copy())
 M=V.T@(W[:,None]*V);co=np.linalg.solve(M,-V.T@(W*rhs))
 J=np.linalg.solve(M,-V.T@((rhs+V@co)[:,None]*D)) if jac else None
 return co-target,W,J,hist
