import numpy as np,networkx as nx
from scipy.optimize import minimize

def opt(F,A,tries=2):
 k=len(F); ij=list(F.edges());ne=len(ij)
 def calc(z):
  x=z[:k];P=np.zeros((k,k))
  for t,(i,j) in enumerate(ij):P[i,j]=P[j,i]=z[k+t]
  R=(P*x)@P.T;B=np.sum((1-P)**2*x,axis=1)
  return R,B
 def cons(z):
  R,B=calc(z)
  return np.r_[A-np.array([R[i,j] for i,j in ij]),z[-1]-B]
 best=None
 for j in range(tries):
  z=np.r_[np.random.dirichlet(np.ones(k)*2),np.random.uniform(.3,.9,ne),.5]
  out=minimize(lambda z:z[-1],z,bounds=[(1e-7,1)]*k+[(1e-7,1)]*ne+[(0,1)],constraints=[{'type':'eq','fun':lambda z:z[:k].sum()-1},{'type':'ineq','fun':cons}],method='SLSQP',options={'maxiter':250,'ftol':1e-9})
  if out.success and (best is None or out.fun<best.fun):best=out
 return best
for A in [.0957,.09,.105]:
 bound=min(.5,(1-np.sqrt(A))**2,1+2*A-4*np.sqrt(A/3));best=bound
 print('A',A,'bound',bound,flush=True)
 for F in nx.graph_atlas_g():
  if len(F)<3 or not nx.is_connected(F) or sum(nx.triangles(F).values())==0:continue
  out=opt(F,A,2)
  if out is not None and out.fun<best-1e-7:
   best=out.fun
   print('improved',len(F),list(F.edges()),best,out.x,flush=True)
 print('done',flush=True)
