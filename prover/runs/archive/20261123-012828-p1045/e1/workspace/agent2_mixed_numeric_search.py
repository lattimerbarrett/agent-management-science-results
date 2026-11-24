import numpy as np,networkx as nx
from scipy.optimize import minimize
from pathlib import Path
rng=np.random.default_rng(965)
A=.09
bound=min(.5,1+2*A-4*np.sqrt(A/3),(1-np.sqrt(A))**2)
best=(1,None)
for nb,nr in [(3,1),(4,1),(3,2),(4,2)]:
 m=nb+nr
 for pattern in range(50):
  S=np.ones((m,m),dtype=bool)
  mask=rng.random((m,m))<.2
  mask=np.triu(mask,1); mask|=mask.T
  S&=~mask
  S[nb:,nb:]=True
  np.fill_diagonal(S,False)
  es=[(i,j) for i in range(m) for j in range(i+1,m) if S[i,j] and i<nb]
  fixed=[(i,j) for i in range(nb,m) for j in range(i+1,m)]
  ne=len(es)
  def unpack(x):
   P=np.zeros((m,m))
   for (i,j),v in zip(es,x[:ne]):P[i,j]=P[j,i]=v
   P[nb:,nb:]=1
   return P,x[ne:ne+m]
  def obj(x):return x[-1]
  def con(x):
   P,w=unpack(x); Q=(P*w)@P.T;B=((1-P)**2)@w
   return np.r_[[A-Q[i,j] for i,j in es+fixed],[A-Q[i,i] for i in range(nb,m)],x[-1]-B[:nb]]
  for it in range(3):
   x=np.r_[rng.uniform(.05,.45,ne),np.r_[rng.dirichlet(np.ones(nb))*.98,rng.dirichlet(np.ones(nr))*.02],.7]
   res=minimize(obj,x,bounds=[(.0000001,1)]*ne+[(.0000001,1)]*m+[(0,1)],constraints=[{'type':'eq','fun':lambda x:sum(x[ne:ne+m])-1},{'type':'ineq','fun':con}],method='SLSQP',options={'maxiter':600,'ftol':1e-10})
   if res.success and res.fun<best[0]:
    best=(res.fun,(nb,nr,es,res.x));print('best',best[0],'bound',bound,'B,R',nb,nr,'Rmass',sum(res.x[ne+nb:ne+m]),flush=True)
print('FINAL',best)
Path('workspace/agent2_mixed_numeric_result.txt').write_text(repr(best))
