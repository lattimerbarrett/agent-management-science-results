import numpy as np
s=np.load('workspace/agent4_twochannel_setup.npz');lam=s['lam'];target=s['target'];d=s['d'];be=float(s['h']);extra=s['extras'];zi=s['zi'];n=7
V=np.vander(lam,3,increasing=True);rhs=lam**3
# balanced mass ratio at theta=-.5 from analytic G-Jacobian
pv=rhs+V@target;rb=(lam-extra[0])*(lam-extra[1]);theta0=-.5
wb=d*be*rb*(lam-theta0)/pv;tan=-d*be*rb/pv
def Jac(w):
 M=V.T@(w[:,None]*V);c=np.linalg.solve(M,-V.T@(w*rhs));p=rhs+V@c;H=sum(w*p*p);ww=w*p*p/H
 return np.diag(p*p/H)-2/H*(w*p)[:,None]*V@np.linalg.solve(M,V.T*p[None,:])-ww[:,None]*(p*p/H)[None,:],ww
J,w1=Jac(wb);J2,_=Jac(w1);NN=J2@J-np.eye(n)
g=[]
for z in zi:g.append(np.dot(NN@NN@(np.eye(n)[z]-wb),tan)/np.dot(tan,tan))
ratio=-g[1]/g[0]
theta=-.55;t2=1e-8;ts=np.array([ratio*t2,t2])
R=rb*(lam-theta);K=np.column_stack([(lam-extra[1])/(extra[0]-extra[1]),(lam-extra[0])/(extra[1]-extra[0])]);DL=K@((ts/d[zi])[:,None]*V[zi])
def init(c):
 q=rhs+V@c;L=K@(ts*q[zi]/d[zi]);S=sum(d*R/q);C=sum(d*L/q);F=(1-C)/S
 dS=-(d*R/q**2)@V;dC=(d/q)@DL-(d*L/q**2)@V;dF=-(dC+F*dS)/S
 W=d*(F*R+L)/q;DW=d[:,None]*((R[:,None]*dF+DL)/q[:,None]-(F*R+L)[:,None]*V/q[:,None]**2)
 return W,DW
def run(c,N,jac=True,save=False):
 W,D=init(c);hist=[]
 for k in range(2*N):
  M=V.T@(W[:,None]*V);co=np.linalg.solve(M,-V.T@(W*rhs));p=rhs+V@co;F=sum(W*p*p)
  if jac:
   dc=np.linalg.solve(M,-V.T@(p[:,None]*D));dF=(p*p)@D
   D=(p*p/F)[:,None]*D+(2*W*p/F)[:,None]*(V@dc)-(W*p*p/F**2)[:,None]*dF
  W=W*p*p/F
  if save and k%max(2,2*N//400)==0:hist.append(W.copy())
 M=V.T@(W[:,None]*V);co=np.linalg.solve(M,-V.T@(W*rhs))
 J=np.linalg.solve(M,-V.T@((rhs+V@co)[:,None]*D)) if jac else None
 return co-target,W,J,hist
