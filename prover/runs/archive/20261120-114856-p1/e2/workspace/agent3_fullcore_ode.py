import numpy as np
from scipy.integrate import solve_ivp
class FullCore:
 def __init__(self,h=32.,picks=(0,0,0)):
  self.core=np.array([-3.,-2,-1,1,2,3]);self.h=h;cc=np.poly(self.core);cc[-1]+=h;roots=np.sort(np.roots(cc).real);picks=np.array(picks);self.pc=np.poly(roots[2*np.arange(3)+picks]);self.qc=np.poly(roots[2*np.arange(3)+1-picks]);self.p=np.polyval(self.pc,self.core);self.q=np.polyval(self.qc,self.core);self.X=np.array([self.core**j for j in range(3)]).T;self.dc=1/np.prod(np.where(np.eye(6,dtype=bool),1,self.core[:,None]-self.core[None,:]),axis=1);self.wu=self.dc*self.q*self.core;self.wv=self.dc*self.q;self.T=np.array([self.wu,self.wv]).T;self.Ti=np.linalg.pinv(self.T);Z=np.vstack([np.ones(6),self.X.T*self.p]);self.Zi=np.linalg.pinv(Z)[:,1:];self.Lu=self.X.T@(self.wu*(self.p-self.q));self.Lv=self.X.T@(self.wv*(self.p-self.q))
 def data(self,pos,A):
  u,v=pos;w=self.dc*self.q*(self.core**2+u*self.core+v);H=self.X.T@(w[:,None]*self.X);dw=self.Zi@(-H@A);ap=self.X@A;E=w@(ap*(self.p-self.q));wp=w*self.p**2/self.h;dwp=(dw*self.p**2+2*w*self.p*ap+wp*E)/self.h;Hp=self.X.T@(wp[:,None]*self.X);b=-np.linalg.solve(Hp,self.X.T@(dwp*self.q));R=self.q*ap+self.p*(self.X@b)+E;V=self.Ti@(2*w*R/self.h);Q=-np.linalg.solve(H,self.X.T@(w*R*R*self.p)/self.h**2);L=self.X.T@(w*(self.p-self.q));D=np.dot(w+wp,R*R)/self.h
  return w,H,L,V,Q,D,R
 def rhs(self,t,y):
  u,v,a1,a2=y;w=self.dc*self.q*(self.core**2+u*self.core+v);L=self.X.T@(w*(self.p-self.q));A=np.array([(1-L[1]*a1-L[2]*a2)/L[0],a1,a2]);w,H,L,V,Q,D,R=self.data([u,v],A);Ad=Q+D*A;return np.r_[V,Ad[1:]]
 def event(self,t,y):
  u,v,a1,a2=y;ww=self.dc*self.q*(self.core**2+u*self.core+v);return min(ww.min()-1e-8,100-max(abs(a1),abs(a2)))
