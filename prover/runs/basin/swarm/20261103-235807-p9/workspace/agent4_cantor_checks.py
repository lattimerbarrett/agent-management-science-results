import numpy as np
from scipy.signal import lfilter
from pathlib import Path

def cantor(p,Q,N,rho=.05):
 q=p/(p-1); ea=1/Q; ec=Q**(-1/(p-1)); sa=(1-ea)/rho; sc=(1-ec)/rho
 da=ea/(1-rho); dc=ec/(1-rho); r=Q**(1/p)
 out=[]
 def rec(l,h,a,c,z,n):
  if n==N:
   out.append((l,h,a,c,z)); return
  delta=r/(a**(1/p)*c**(1/q)); length=h-l
  u=l+.2*length; v=u+rho/2*length
  w=h-.2*length-rho/2*length; t=h-.2*length
  out.extend([(l,u,da*a,dc*c,z-2*delta),(v,w,da*a,dc*c,z),(t,h,da*a,dc*c,z+2*delta)])
  rec(u,v,sa*a,sc*c,z-delta,n+1)
  rec(w,t,sa*a,sc*c,z+delta,n+1)
 rec(0.,1.,1.,1.,0.,0)
 return np.array(sorted(out))

def ratio_kernel(leaves,p):
 q=p/(p-1); a,c,z=leaves[:,2:].T
 x=(a[:,None]/a[None,:])**(1/p)
 y=(c[None,:]/c[:,None])**(1/q)
 off=a[:,None]**(1/p)*c[None,:]**(1/q)*(z[:,None]-z[None,:])
 trace=x*x+y*y+off*off
 return np.sqrt((trace+np.sqrt(np.maximum(0,trace*trace-4*x*x*y*y)))/2)

def char(prob,K,p):
 q=p/(p-1)
 return prob@((K**q@prob)**(p-1))

for p in [1.5,2.,3.,4.]:
 Q=10.; L=cantor(p,Q,6); K=ratio_kernel(L,p)
 prob=L[:,1]-L[:,0]
 assert abs(prob@L[:,2]-1)<1e-5 and abs(prob@L[:,3]-1)<1e-5
 assert np.all(np.diff(L[:,4])>=-1e-12)
 print('p,Q,leaves,root characteristic=',p,Q,len(L),char(prob,K,p))
 # All interval endpoints selected from a coarse sample of actual boundaries.
 boundaries=np.unique(L[:,:2]); ix=np.unique(np.linspace(0,len(boundaries)-1,35).astype(int)); mx=0
 for i in ix:
  for j in ix:
   if j<=i: continue
   l,h=boundaries[i],boundaries[j]
   pr=np.maximum(0,np.minimum(L[:,1],h)-np.maximum(L[:,0],l))/(h-l)
   mx=max(mx,char(pr,K,p))
 print('sampled maximum interval characteristic=',mx)

# Positive depth-model lower bound, computed using two linear recurrences.
for p in [1.5,2.,3.,4.]:
 q=p/(p-1)
 for Q in [10.,30.,100.]:
  ea=1/Q; ec=Q**(-1/(p-1)); aa=(1-ea)**(1/p); cc=(1-ec)**(1/q)
  r=Q**(1/p); n=int(100*max(1/ea,1/ec)); f=np.ones(n)
  # upper geometric kernel followed by lower geometric kernel
  upper=lfilter([1.],[1.,-cc],f[::-1])[::-1]
  out=lfilter([r*ea**(1/p)*ec**(1/q)],[1.,-aa],upper)
  ratio=np.linalg.norm(out,ord=p)/np.linalg.norm(f,ord=p)
  exact=r*ea**(1/p)*ec**(1/q)/((1-aa)*(1-cc))
  target=Q**(1+1/(p*(p-1)))
  assert .85<ratio/exact<=1+1e-8
  print('depth p,Q,finite norm/exact,exact/target=',p,Q,ratio/exact,exact/target)
