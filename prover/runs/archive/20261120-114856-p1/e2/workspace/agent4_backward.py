import numpy as np
core=np.array([-3.,-1.,1.,2.,3.])/3;ex=np.array([0,np.sqrt(7)/3]);lam=np.sort(np.r_[core,ex]);I=np.isin(lam,core);zi=np.where(~I)[0];V=np.vander(lam,3,increasing=True);rhs=lam**3
ac=1/np.prod(np.where(np.eye(5,dtype=bool),1,core[:,None]-core[None,:]),axis=1)
def invstep(U,c):
 U=U-U.max();w=np.exp(U);w/=sum(w);p=rhs+V@c;sgn=np.sign(p)
 for it in range(30):
  p=rhs+V@c;f=V.T@(w/p);J=-V.T@((w/p**2)[:,None]*V)
  if np.max(abs(f))<2e-13:break
  dc=np.linalg.solve(J,-f);a=1.
  old=sum(w*np.log(abs(p)))
  while a>1e-8:
   cc=c+a*dc;pp=rhs+V@cc
   if np.all(pp*sgn>0) and sum(w*np.log(abs(pp)))>=old-1e-15:break
   a*=.5
  c=cc
 if it==29:raise RuntimeError(('inv Newton failed',np.max(abs(f))))
 U-=2*np.log(abs(rhs+V@c));U-=np.max(U)
 return U,c

def backward(delta,mass=1e-12,stop=1e-6,N=500000):
 root=np.sqrt(18-delta)/27;cp=np.array([root,-7/9,0]);cq=np.array([-root,-7/9,0]);q=core**3-7/9*core-root
 wc=ac*q*(core-1.4/3);W=np.zeros(7);W[I]=wc*(1-mass);rat=1.4/(np.sqrt(7)-1.4);W[zi]=mass*np.array([rat,1])/(1+rat);U=np.log(W)
 cs=[cq,cp];hist=[]
 for k in range(N):
  j=k%2;U,cs[j]=invstep(U,cs[j]);W=np.exp(U);W/=sum(W)
  if k%1000==0:hist.append(W.copy())
  if sum(W[zi])>=stop:break
 return k,W,np.array(hist),cs
