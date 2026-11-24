import numpy as np,itertools
from scipy.optimize import minimize
rng=np.random.default_rng(1)
A=.09
claimed=min(.5,(1-np.sqrt(A))**2,1+2*A-4*np.sqrt(A/3))
best=1
for k in [3,4,5,6]:
 ij=list(zip(*np.triu_indices(k,1))); ne=len(ij)
 for trial in range(1200):
  # deterministic loop colors and edge supports, most loops blue
  loops=(rng.random(k)<.12).astype(float)
  types=rng.choice([0,1,2],ne,p=[.27,.63,.10]) #0 blue,1 mixed,2 red
  variables=[ij[t] for t in range(ne) if types[t]==1]
  Pbase=np.diag(loops)
  for t,(i,j) in enumerate(ij):
   if types[t]==2:Pbase[i,j]=Pbase[j,i]=1
  Rmask=Pbase>0;Bmask=Pbase<1
  for i,j in variables:Rmask[i,j]=Rmask[j,i]=True
  def calc(z):
   x=z[:k];P=Pbase.copy()
   for t,(i,j) in enumerate(variables):P[i,j]=P[j,i]=z[k+t]
   R=(P*x)@P.T;Q=1-P;B=(Q*x)@Q.T
   return R,B
  def cons(z):
   R,B=calc(z)
   return np.r_[A-R[Rmask],z[-1]-B[Bmask]]
  z=np.r_[rng.dirichlet(np.ones(k)*5),rng.uniform(.2,.7,len(variables)),.5]
  out=minimize(lambda z:z[-1],z,bounds=[(.000001,1)]*k+[(.000001,.999999)]*len(variables)+[(0,1)],constraints=[{'type':'eq','fun':lambda z:z[:k].sum()-1},{'type':'ineq','fun':cons}],method='SLSQP',options={'maxiter':100,'ftol':1e-9})
  if out.success and out.fun<best-1e-7:
   best=out.fun
   print('best',k,trial,best,'claimed',claimed,'loops',loops,'types',types,'x',out.x,flush=True)
 print('done',k,flush=True)
