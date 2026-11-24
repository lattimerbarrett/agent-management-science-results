import numpy as np
from scipy.optimize import differential_evolution
rng=np.random.default_rng(12)
for alpha in [.17,.2,.205,.22,.3]:
 for k,nr in [(5,1),(6,2),(7,1),(7,3),(8,2),(9,3)]:
  ij=[(i,j) for i in range(k) for j in range(i+1,k) if j>=nr]
  def fun(z,ret=False):
   w=z[:k];w=w/w.sum();P=np.zeros((k,k));P[:nr,:nr]=1
   for v,(i,j) in zip(z[k:],ij):P[i,j]=P[j,i]=min(1,max(0,v))
   A=(P*w)@P;Q=1-P;B=(Q*w)@Q
   a=max([*A[:nr,:nr].diagonal()]+[A[i,j] for i,j in ij if P[i,j]>0])
   b=max([*B[nr:,nr:].diagonal()]+[B[i,j] for i,j in ij if i<nr and P[i,j]<1])
   return (1/max(a/alpha,b),w,P) if ret else max(a/alpha,b)
  best=(0,None)
  for seed in range(2):
   res=differential_evolution(fun,[(.000001,1)]*k+[(-.3,1.3)]*len(ij),popsize=6,maxiter=1800,tol=1e-7,rng=rng)
   v=fun(res.x,True)
   if v[0]>best[0]:best=v
  print(alpha,k,nr,best[0],flush=True)
  with open(f'opt_{alpha}_{k}_{nr}.npz','wb') as f:np.savez(f,c=best[0],w=best[1],P=best[2])
