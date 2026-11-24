import numpy as np
from scipy.special import expit
from scipy.integrate import solve_bvp, cumulative_trapezoid
class PeriodicBVP:
 def __init__(self,picks=(0,1,0),radius=.25,shape=0):
  self.l=np.array([-3.,-2.,-1.,1.,2.,3.]);self.X=self.l[:,None]**np.arange(3);self.d=np.array([1/np.prod(self.l[i]-np.delete(self.l,i)) for i in range(6)])
  self.picks=picks;self.radius=radius;self.shape=shape;self.cache=None;self.S=4*np.pi*np.pi*radius*radius
 def setup(self,h):
  if self.cache is not None and self.cache[0]==h:return self.cache[1]
  rr=np.sort(np.roots([1.,0,-14,0,49,0,-36+h]).real)
  pc=np.poly(rr[[2*j+self.picks[j] for j in range(3)]]);qc=np.poly(rr[[2*j+1-self.picks[j] for j in range(3)]])
  out=pc,qc,np.polyval(pc,self.l),np.polyval(qc,self.l)
  self.cache=(h,out)
  return out
 def data(self,y,h):
  pc,qc,p,q=self.setup(h);ss=expit(np.clip(y[:2],-22,22));aa=-2+ss[0];bb=1+ss[1];u=-aa-bb;v=aa*bb
  w=self.d*q*(self.l*self.l+u*self.l+v);H=(self.X.T*w)@self.X;wp=w*p*p/h;Hp=(self.X.T*wp)@self.X
  Lv=self.X.T@(w*(p-q));A=np.array([(1-Lv[1]*y[2]-Lv[2]*y[3])/Lv[0],y[2],y[3]])
  b=-np.linalg.solve(Hp,H@A);R=q*(self.X@A)+p*(self.X@b)+1
  dotw=2*w*R/h;ud=self.l@dotw;vd=self.l**2@dotw-qc[1]*ud
  Q=-np.linalg.solve(H,self.X.T@(w*R*R*p))/h**2;D=(w+wp)@(R*R)/h;Ad=Q+D*A
  ad=(vd+aa*ud)/(bb-aa);bd=(-vd-bb*ud)/(bb-aa)
  out=np.r_[ad/(ss[0]*(1-ss[0])),bd/(ss[1]*(1-ss[1])),Ad[1:]]
  return out,np.array([ad,bd]),(u,v,A,D,w)
 def rhs(self,t,y,par):
  T=np.exp(np.clip(par[0],-15,10));h=.001+35.998*expit(par[1]);pc,qc,p,q=self.setup(h)
  ss=expit(np.clip(y[:2],-22,22));aa=-2+ss[0];bb=1+ss[1];u=-aa-bb;v=aa*bb
  w=(self.d*q)[None,:]*(self.l[None,:]**2+u[:,None]*self.l[None,:]+v[:,None]);wp=w*p*p/h
  H=np.einsum('ni,ij,ik->njk',w,self.X,self.X);Hp=np.einsum('ni,ij,ik->njk',wp,self.X,self.X)
  Lv=(w*(p-q))@self.X;A=np.stack([(1-Lv[:,1]*y[2]-Lv[:,2]*y[3])/Lv[:,0],y[2],y[3]],axis=1)
  try:b=-np.linalg.solve(Hp,np.einsum('nij,nj->ni',H,A)[...,None])[...,0]
  except np.linalg.LinAlgError:return np.full_like(y,1e10)
  R=q*(A@self.X.T)+p*(b@self.X.T)+1;dotw=2*w*R/h;ud=dotw@self.l;vd=dotw@(self.l**2)-qc[1]*ud
  Q=-np.linalg.solve(H,((w*R*R*p)@self.X)[...,None])[...,0]/h**2;D=np.sum((w+wp)*R*R,axis=1)/h;Ad=Q+D[:,None]*A
  ad=(vd+aa*ud)/(bb-aa);bd=(-vd-bb*ud)/(bb-aa)
  return np.stack([T*ad/(ss[0]*(1-ss[0])),T*bd/(ss[1]*(1-ss[1])),T*Ad[:,1],T*Ad[:,2],T*T*(ad*ad+bd*bd)])
 def bc(self,ya,yb,par):return np.r_[ya[:4]-yb[:4],ya[0],ya[4],yb[4]-self.S]
 def guess(self,h,T,N=81):
  t=np.linspace(0,1,N);th=2*np.pi*t+np.pi/2;r=self.radius
  if self.shape:
   k=self.shape;aa=-1.5+r*np.tanh(k*np.cos(th))/np.tanh(k);bb=1.5+r*np.tanh(k*np.sin(th))/np.tanh(k)
   ad=-r*2*np.pi*k*np.sin(th)/np.cosh(k*np.cos(th))**2/np.tanh(k)/T;bd=r*2*np.pi*k*np.cos(th)/np.cosh(k*np.sin(th))**2/np.tanh(k)/T
  else:
   aa=-1.5+r*np.cos(th);bb=1.5+r*np.sin(th);ad=-r*2*np.pi*np.sin(th)/T;bd=r*2*np.pi*np.cos(th)/T
  u=-aa-bb;v=aa*bb;ud=-ad-bd;vd=bb*ad+aa*bd
  y=np.zeros((5,N));sa=aa+2;sb=bb-1;y[0]=np.log(sa/(1-sa));y[1]=np.log(sb/(1-sb))
  pc,qc,p,q=self.setup(h)
  for j in range(N):
   w=self.d*q*(self.l*self.l+u[j]*self.l+v[j]);H=(self.X.T*w)@self.X;wp=w*p*p/h;Hp=(self.X.T*wp)@self.X;Lv=self.X.T@(w*(p-q));bs=-np.linalg.solve(Hp,H)
   Rs=q[:,None]*self.X+p[:,None]*(self.X@bs)+Lv[None,:];dw=2*w[:,None]*Rs/h;du=self.l@dw;dv=self.l**2@dw-qc[1]*du
   A=np.linalg.solve(np.vstack([du,dv,Lv]),[ud[j],vd[j],1]);y[2:4,j]=A[1:]
  y[4]=cumulative_trapezoid(T*T*(ad*ad+bd*bd),t,initial=0);self.S=y[4,-1]
  return t,y,np.array([np.log(T),np.log((h-.001)/(35.999-h))])
 def solve(self,h=18,T=2,tol=.003,max_nodes=800):
  t,y,p=self.guess(h,T);return solve_bvp(self.rhs,self.bc,t,y,p,tol=tol,max_nodes=max_nodes,verbose=0)
