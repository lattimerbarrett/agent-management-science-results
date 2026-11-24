import sys;sys.path.insert(0,'workspace');import agent1_flip_augode as m
import numpy as np,itertools
from scipy.integrate import solve_ivp
from scipy.special import expit
active=np.array([-3,-np.sqrt(5),-1,1,np.sqrt(5),3]);D6=np.polynomial.Polynomial.fromroots(active);cv=np.array([1/np.prod(active[j]-np.delete(active,j)) for j in range(6)])
delta=4*np.sqrt(2);r1=np.sqrt(5+np.array([-1,1])*np.sqrt(8+delta));r2=np.sqrt(5+np.array([-1,1])*np.sqrt(8-delta));roots=np.sort(np.r_[r1,-r1,r2,-r2]);pairs=roots.reshape(4,2)

def setup(bits,mu):
 global wref,L,Pp,Qp
 Pp=np.polynomial.Polynomial.fromroots(pairs[np.arange(4),bits]);Qp=np.polynomial.Polynomial.fromroots(pairs[np.arange(4),1-np.array(bits)])
 m.x=np.r_[active,[-mu,mu]];m.V=m.x[:,None]**np.arange(4);m.p=Pp(m.x);m.q=Qp(m.x);m.C=32.;m.w0=np.r_[32*active*cv/m.p[:6],[0,0]];wref=m.w0.copy()
 T=np.r_[-wref[:6]/active,[0,0]]
 def coords(hc):
  w=wref;h=m.V@hc;u=w*m.p*h;M=m.V.T@(w[:,None]*m.V);ac=-np.linalg.solve(M,m.V.T@(u*m.p));aa=m.V@ac;F=np.dot(u,m.p*m.p);z=w*m.p*m.p/m.C;z1=(u*m.p*m.p+2*w*m.p*aa-z*F)/m.C
  K=m.V.T@(z[:,None]*m.V);bc=-np.linalg.solve(K,m.V.T@(z1*m.q));bb=m.V@bc;FF=np.dot(z1,m.q*m.q);f1=(z1*m.q*m.q+2*z*m.q*bb-w*FF)/m.C;b=f1-u;v=T@b/(T@T)
  R=Qp*np.polynomial.Polynomial(ac)+Pp*np.polynomial.Polynomial(bc)-F
  quot=(R*np.polynomial.Polynomial([0,1])+m.C*v/2)//D6
  return np.r_[np.pad(quot.coef,(0,3-len(quot.coef))),-F/m.C]
 L=np.column_stack([coords(np.eye(4)[j]) for j in range(4)])

def smoothw(u):
 tt=np.tanh(u);w=wref.copy();w[:6]*=1-tt/active;w[2]=wref[2]*2*expit(2*u);w[3]=wref[3]*2*expit(-2*u);return tt,w

def flow(t,z):
 tt,w=smoothw(z[0]);h=m.V@z[1:5];u=w*m.p*h;M=m.V.T@(w[:,None]*m.V);aa=-m.V@np.linalg.solve(M,m.V.T@(u*m.p));d=np.dot(u,m.p*m.p);zz=w*m.p*m.p/m.C;L1=m.p*h+2*aa/m.p-d/m.C;K=m.V.T@(zz[:,None]*m.V);cc=-m.V@np.linalg.solve(K,m.V.T@(zz*L1*m.q));dd=np.dot(zz*L1,m.q*m.q);R=2*aa/m.p+2*cc/m.q-(d+dd)/m.C
 ud=-R[3]/(1+tt) if z[0]>=0 else R[2]/(1-tt);out=m.ode(t,np.r_[w,z[1:]])
 return np.r_[ud,out[8:]]
def fuel(z):
 tt,w=smoothw(z[0]);return -np.dot(w*m.p**3,m.V@z[1:5])/m.C
def evF(t,z):return fuel(z)
evF.terminal=True;evF.direction=-1
def evU(t,z):return 30-abs(z[0])
evU.terminal=True;evU.direction=-1
