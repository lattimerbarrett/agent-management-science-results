import sys;sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
from scipy.special import expit,logit
bits=(0,1,0,0)
def geom(L,eta):
 m=g.m;mid=(1+L*L)/2;H=(L*L-1)**2/8;delta=H*np.sqrt((1+eta*eta)/2);C=H*H*(1-eta*eta)/2
 active=np.array([-L,-np.sqrt(mid),-1,1,np.sqrt(mid),L]);D6=np.polynomial.Polynomial.fromroots(active);cv=np.array([1/np.prod(active[j]-np.delete(active,j)) for j in range(6)])
 r1=np.sqrt(mid+np.array([-1,1])*np.sqrt(H+delta));r2=np.sqrt(mid+np.array([-1,1])*np.sqrt(H-delta));pairs=np.sort(np.r_[r1,-r1,r2,-r2]).reshape(4,2)
 Pp=np.polynomial.Polynomial.fromroots(pairs[np.arange(4),bits]);Qp=np.polynomial.Polynomial.fromroots(pairs[np.arange(4),1-np.array(bits)]);mu=np.sqrt(mid+np.sqrt(H*(1+eta)))
 m.x=np.r_[active,[-mu,mu]];m.V=m.x[:,None]**np.arange(4);m.p=Pp(m.x);m.q=Qp(m.x);m.C=C;m.w0=np.r_[C*active*cv/m.p[:6],[0,0]]
 wref=m.w0.copy();T=np.r_[-wref[:6]/active,[0,0]]
 def coords(hc):
  w=wref;h=m.V@hc;u=w*m.p*h;M=m.V.T@(w[:,None]*m.V);ac=-np.linalg.solve(M,m.V.T@(u*m.p));aa=m.V@ac;F=np.dot(u,m.p*m.p);z=w*m.p*m.p/C;z1=(u*m.p*m.p+2*w*m.p*aa-z*F)/C
  K=m.V.T@(z[:,None]*m.V);bc=-np.linalg.solve(K,m.V.T@(z1*m.q));bb=m.V@bc;FF=np.dot(z1,m.q*m.q);f1=(z1*m.q*m.q+2*z*m.q*bb-w*FF)/C;b=f1-u;v=T@b/(T@T)
  R=Qp*np.polynomial.Polynomial(ac)+Pp*np.polynomial.Polynomial(bc)-F;quot=(R*np.polynomial.Polynomial([0,1])+C*v/2)//D6
  return np.r_[np.pad(quot.coef,(0,3-len(quot.coef))),-F/C]
 g.active=active;g.D6=D6;g.cv=cv;g.pairs=pairs;g.wref=wref;g.Pp=Pp;g.Qp=Qp;g.L=np.column_stack([coords(np.eye(4)[j]) for j in range(4)])
 return mu
