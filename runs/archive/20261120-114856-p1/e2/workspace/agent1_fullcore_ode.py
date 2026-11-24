import numpy as np,itertools,time,sys
from scipy.optimize import linprog
from scipy.integrate import solve_ivp
class FullCoreODE:
 def __init__(self,h=18.,picks=(0,1,0)):
  self.l=np.array([-3.,-2.,-1.,1.,2.,3.]);self.h=h;self.X=self.l[:,None]**np.arange(3);self.d=1/np.prod(np.where(np.eye(6,dtype=bool),1,self.l[:,None]-self.l[None,:]),axis=1)
  rr=np.sort(np.roots([1,0,-14,0,49,0,-36+h]).real);self.pc=np.poly(rr[[2*j+picks[j] for j in range(3)]]);self.qc=np.poly(rr[[2*j+1-picks[j] for j in range(3)]]);self.p=np.polyval(self.pc,self.l);self.q=np.polyval(self.qc,self.l)
  self.WT=(self.d*self.q)[:,None]*np.array([self.l,np.ones(6)]).T;self.wc=self.d*self.q*self.l**2
  self.Z=np.vstack([np.ones(6),(self.X.T*self.p)]);self.Zinv=np.linalg.pinv(self.Z)
  self.Lder=(self.X.T*(self.p-self.q))@self.WT
  lp=linprog([0,0,-1],A_ub=np.c_[-self.WT,np.ones(6)],b_ub=self.wc,bounds=[(None,None),(None,None),(0,None)],method='highs');self.center=lp.x[:2]
 def data(self,y):
  u,v,a1,a2=y;w=self.wc+self.WT@np.array([u,v]);H=(self.X.T*w)@self.X;Lv=self.X.T@(w*(self.p-self.q));A=np.array([(1-Lv[1]*a1-Lv[2]*a2)/Lv[0],a1,a2]);dw=self.Zinv@np.r_[0.,-H@A];wp=w*self.p*self.p/self.h;dwp=(dw*self.p*self.p+2*w*self.p*(self.X@A)+wp)/self.h
  b=-np.linalg.solve((self.X.T*wp)@self.X,self.X.T@(dwp*self.q));R=self.q*(self.X@A)+self.p*(self.X@b)+1
  dotw=2*w*R/self.h;du=self.l@dotw;dv=self.l**2@dotw-self.qc[1]*du;Q=-np.linalg.solve(H,self.X.T@(w*R*R*self.p))/self.h**2;D=-(Lv@Q+(self.Lder@np.array([du,dv]))@A);Adot=Q+D*A
  return np.r_[du,dv,Adot[1:]],w,A,D
 def rhs(self,t,y):return self.data(y)[0]
 def event(self,t,y):
  rhs,w,A,D=self.data(y);return min(w.min()-1e-7,100-max(abs(A)))

