import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(12345)
for sizes in [[1,1,2],[2,2,2],[1,2,3]]:
 k=sum(sizes);cls=np.repeat(np.arange(3),sizes);inds=np.array([(i,j) for i in range(k) for j in range(i+1,k) if cls[i]!=cls[j]]);nedge=len(inds)
 for al in [.17,.19,.2,.20072,.201,.21,.24]:
  best=(0,None)
  for it in range(40):
   nr=3;N=k+nr
   def unpack(v):
    x=v[:N];P=np.zeros((N,N));P[inds[:,0],inds[:,1]]=v[N:N+nedge];P+=P.T;P[k:,k:]=1;P[:k,k:]=v[N+nedge:-1].reshape(k,nr);P[k:,:k]=P[:k,k:].T
    return x,P,v[-1]
   def con(v):
    x,P,b=unpack(v);Q=(P*x)@P;B=((1-P)*x)@(1-P);a=al*b
    return np.r_[a-Q[inds[:,0],inds[:,1]],a-Q.diagonal()[k:],b-B.diagonal()[:k],(a-Q[:k,k:]).ravel(),(b-B[:k,k:]).ravel()]
   xr=rng.uniform(.0001,.03,nr);xb=np.concatenate([rng.dirichlet([5]*s)/3 for s in sizes])*(1-sum(xr));x=np.r_[xb,xr]
   v=np.r_[x,rng.uniform(.49,.55,nedge),rng.uniform(.2,.28,k*nr),.49]
   r=minimize(lambda v:v[-1],v,method='SLSQP',bounds=[(1e-8,1)]*N+[(1e-6,1-1e-6)]*(nedge+k*nr)+[(.2,1)],constraints=[{'type':'eq','fun':lambda v:sum(v[:N])-1},{'type':'ineq','fun':con}],options={'maxiter':1000,'ftol':1e-11})
   if r.success and min(con(r.x))>-1e-7 and 1/r.fun>best[0]:best=(1/r.fun,unpack(r.x))
  print(sizes,al,best,flush=True)
