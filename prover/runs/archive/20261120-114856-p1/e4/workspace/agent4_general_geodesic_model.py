import numpy as np
from scipy.linalg import null_space
class GeneralModel:
 def __init__(self,q,r,H,x):
  self.q=np.array(q);self.r=np.array(r);self.H=H;self.x=np.array(x);s=4;self.f=np.vander(x,s,increasing=True);self.qv=np.polyval(q,x);self.rv=np.polyval(r,x);self.P=np.poly(x);m=len(x);self.td=m-s-1;den=np.polyval(np.polyder(self.P),x);self.C=self.rv[:,None]*np.vander(x,self.td,increasing=True)/den[:,None];self.wb=self.rv*x**self.td/den;self.Ci=np.linalg.pinv(self.C)
  Syl=np.zeros((8,8))
  for j in range(4):Syl[:,j]=np.r_[np.zeros(j),r[::-1],np.zeros(3-j)];Syl[:,4+j]=np.r_[np.zeros(j),q[::-1],np.zeros(3-j)]
  targets=[]
  for j in range(9-m):
   if j==0:pp=np.r_[1.,np.zeros(7)]
   else:pp=np.r_[self.P[::-1],np.zeros(7-m)]
   targets.append(np.linalg.solve(Syl,pp)[:4])
  self.N=null_space(np.array(targets));self.dim=self.N.shape[1]
 def weights(self,tau):return self.wb+self.C@tau
 def maps(self,Z):
  tau=Z[:self.td];v=self.N@Z[self.td:];w=self.weights(tau);wp=w*self.qv**2/self.H;G=self.f.T@(w[:,None]*self.f);Gp=self.f.T@(wp[:,None]*self.f);dr=-np.linalg.solve(Gp,G@v);dqv=self.f@v;drv=self.f@dr;dQ=self.rv*dqv+self.qv*drv;dh=w@dQ;E=dQ-dh;wdot=2*w*E/self.H;K=np.linalg.solve(G,self.f.T@(w*self.qv*E**2))/self.H**2
  return np.r_[self.Ci@wdot,-self.N.T@K]
 def field(self,t,Z):return self.maps(Z)
