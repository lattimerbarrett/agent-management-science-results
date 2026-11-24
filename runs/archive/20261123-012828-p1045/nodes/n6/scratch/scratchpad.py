import numpy as np
from scipy.optimize import differential_evolution

def opt(a,k):
 ij=np.triu_indices(k,1)
 def calc(z,full=False):
  x=np.r_[z[:k-1],1.];x=x/x.sum();P=np.zeros((k,k));P[ij]=z[k-1:];P+=P.T
  R=(P*x)@P;Q=1-P;B=(Q*x)@Q
  av=max(R[ij]);bv=max(np.diag(B));val=max(av/a,bv)
  return (1/val,x,P,av/bv) if full else val
 r=differential_evolution(calc,[(.000001,10)]*(k-1)+[(.000001,.999999)]*(k*(k-1)//2),tol=1e-8,popsize=20,maxiter=1800,seed=22)
 return calc(r.x,True)
for a in [.17,.18,.19,.2,.21,.23]:
 c,x,P,ratio=opt(a,4)
 print(a,'c',c,'x',x,'P',P,'ratio',ratio,flush=True)
