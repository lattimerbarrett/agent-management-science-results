import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import linprog
class Geodesic:
 def __init__(self,h=18,picks=(0,0,0),core=None):
  x=np.array([-3.,-2.,-1.,1.,2.,3.]) if core is None else np.array(core);self.x=x;self.h=h;X=np.vander(x,3,increasing=True);self.X=X
  ch=np.poly(x);ch[-1]+=h;rr=np.roots(ch)
  if max(abs(rr.imag))>1e-8:raise ValueError()
  rr=np.sort(rr.real);self.pc=np.poly(rr[[2*j+picks[j]for j in range(3)]]);self.qc=np.poly(rr[[2*j+1-picks[j]for j in range(3)]]);p=np.polyval(self.pc,x);q=np.polyval(self.qc,x);self.p=p;self.q=q;d=1/np.prod(np.where(np.eye(6,dtype=bool),1,x[:,None]-x[None,:]),axis=1);self.w0=d*q*x*x;self.W=np.array([d*q*x,d*q]).T;self.P=np.array([x,x*x-self.qc[1]*x]);self.rat=p*p/h
  lp=linprog([0,0,-1],A_ub=np.c_[-self.W,np.ones(6)],b_ub=self.w0,bounds=[(None,None),(None,None),(0,None)],method='highs');self.center=lp.x[:2]
 def data(self,pos):
  X=self.X;p=self.p;q=self.q;h=self.h;w=self.w0+self.W@pos;H=(X.T*w)@X;Hp=(X.T*(w*self.rat))@X;M=np.linalg.solve(Hp,H);L=(w*(p-q))@X;Rc=q[:,None]*X-(p[:,None]*X)@M+L
  V=2/h*(self.P*w)@Rc;der=[]
  for j in range(2):
   dw=self.W[:,j];dH=(X.T*dw)@X;dHp=(X.T*(dw*self.rat))@X;dM=np.linalg.solve(Hp,dH-dHp@M);dL=(dw*(p-q))@X;dRc=-(p[:,None]*X)@dM+dL;der.append(2/h*((self.P*dw)@Rc+(self.P*w)@dRc))
  return w,H,L,Rc,V,der
 def rhs(self,t,y):
  pos=y[:2];theta=y[2];vel=np.array([np.cos(theta),np.sin(theta)]);w,H,L,Rc,V,der=self.data(pos);A=np.linalg.solve(np.vstack([V,L]),np.r_[vel,1.]);R=Rc@A;Q=-np.linalg.solve(H,self.X.T@(w*R*R*self.p))/self.h**2;acc=(der[0]*vel[0]+der[1]*vel[1])@A+V@Q
  return np.r_[vel,np.array([-vel[1],vel[0]])@acc]
 def integrate(self,pos,angle,length=100):
  def boundary(t,y):return min(self.w0+self.W@y[:2])-1e-6
  boundary.terminal=True;boundary.direction=-1
  return solve_ivp(self.rhs,[0,length],np.r_[pos,angle],rtol=3e-7,atol=1e-9,events=boundary,max_step=.1)
