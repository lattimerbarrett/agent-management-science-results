import numpy as np,time
from scipy.optimize import root
core=np.array([-3.,-2.,-1.,1.,2.,3.]);f=core**3-7*core;wc=(1+f/(6*np.sqrt(2)))/6
sp=np.r_[core,0.,np.sqrt(7.)];ix=np.argsort(sp);x=sp[ix]/6

def shoot(pars,N,trace=False):
 pars=np.atleast_2d(pars);B=len(pars)
 g=f[None,:]/6*(1+pars[:,0,None]*core[None,:]/3+pars[:,1,None]*(core[None,:]**2-14/3)/9)
 eps=.01;ws=np.c_[wc[None,:]*np.exp(eps*g),np.full((B,2),eps**2*1e-3)];ws=ws[:,ix];ws/=ws.sum(axis=1)[:,None]
 lw=np.log(ws);hist=[]
 for k in range(N+1):
  w=np.exp(lw);p0=np.zeros_like(w);p=np.ones_like(w);beta=np.zeros(B)
  for j in range(3):
   norm=np.sum(w*p*p,axis=1);alpha=np.sum(w*x*p*p,axis=1)/norm
   q=(x-alpha[:,None])*p-beta[:,None]*p0;beta=np.sum(w*q*q,axis=1)/norm;p0,p=p,q
  if trace and k%100==0:hist.append(w.copy())
  if k==N:break
  z=lw+2*np.log(np.maximum(np.abs(p),1e-280));lw=z-np.logaddexp.reduce(z,axis=1)[:,None]
 h=np.sum(w*p*p,axis=1)*6**6
 ans=np.c_[h-18,w[:,4]-w[:,5]]
 return (ans,lw,np.array(hist)) if trace else ans

par=np.array([-1.25,-1/6]);saved=[];t0=time.time()
for N in [1000,3000,10000,30000,100000]:
 def fun(z):return shoot(z,N)[0]
 sol=root(fun,par,tol=1e-8)
 par=sol.x;print('N',N,'success',sol.success,'par',par,'F',sol.fun,'nfev',sol.nfev,'time',time.time()-t0,flush=True)
 ans,lw,hist=shoot(par,N,True)
 saved.append((N,par.copy(),sol.fun.copy(),lw,hist))
 if abs(par).max()>100:break
import pickle
with open('shoot_stationary8.pkl','wb') as f:pickle.dump(saved,f)
