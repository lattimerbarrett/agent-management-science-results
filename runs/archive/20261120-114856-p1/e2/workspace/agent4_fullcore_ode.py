import numpy as np
class FullCore:
 def __init__(self,h=1,picks=(0,0,0)):
  self.lam=np.array([-3.,-2.,-1.,1.,2.,3.]);x=self.lam;self.h=h;self.X=np.vander(x,3,increasing=True);self.XX=self.X[:,:,None]*self.X[:,None,:]
  ch=np.poly(x);ch[-1]+=h;r=np.sort(np.roots(ch).real);pc=np.poly(r[[2*j+picks[j] for j in range(3)]]);qc=np.poly(r[[2*j+1-picks[j] for j in range(3)]]);self.p=np.polyval(pc,x);self.q=np.polyval(qc,x);self.q2=qc[1]
  dd=1/np.prod(np.where(np.eye(6,dtype=bool),1,x[:,None]-x[None,:]),axis=1);self.coeff=dd*self.q;self.Lu=(self.coeff*x*(self.p-self.q))@self.X;self.Lv=(self.coeff*(self.p-self.q))@self.X
 def weights(self,Y):return self.coeff[None,:]*(self.lam[None,:]**2+Y[:,0,None]*self.lam[None,:]+Y[:,1,None])
 def energyrow(self,Y):return (self.weights(Y)*(self.p-self.q))@self.X
 def rhs(self,Y,check=False):
  w=self.weights(Y);A=Y[:,2:];L=(w*(self.p-self.q))@self.X;en=np.sum(L*A,axis=1);H=np.einsum('ki,ijl->kjl',w,self.XX);wp=w*self.p**2/self.h;Hp=np.einsum('ki,ijl->kjl',wp,self.XX)
  HA=np.einsum('kij,kj->ki',H,A);B=-np.linalg.solve(Hp,HA[:,:,None])[:,:,0];R=(A@self.X.T)*self.q+(B@self.X.T)*self.p+en[:,None]
  dw=2*w*R/self.h;du=dw@self.lam;dv=dw@(self.lam**2)-self.q2*du;Q=-np.linalg.solve(H,((w*R*R*self.p)@self.X)[:,:,None])[:,:,0]/self.h**2
  D=-np.sum(L*Q,axis=1)-(A@self.Lu)*du-(A@self.Lv)*dv
  if check:return D,np.sum((w+wp)*R*R,axis=1)/self.h,en
  return np.c_[du,dv,Q+D[:,None]*A]
