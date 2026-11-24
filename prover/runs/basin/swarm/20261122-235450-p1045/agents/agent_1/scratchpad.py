import numpy as np
from scipy.optimize import differential_evolution, minimize
import networkx as nx
rng=np.random.default_rng(42)
for a in [.05,.0833333,.09,.095,.1,.12]:
 for G in [nx.complete_graph(3), nx.circular_ladder_graph(3), nx.wheel_graph(6)]:
  k=len(G); ed=list(G.edges());M=len(ed)
  def unpack(x):
   w=x[:k];W=np.zeros((k,k))
   for (i,j),v in zip(ed,x[k:]):W[i,j]=W[j,i]=v
   return w,W
  def calc(x):
   w,W=unpack(x);return np.sum(w[:,None]*w[None,:]*(2*W-W*W))
  def con(x):
   w,W=unpack(x);R=(W*w)@W
   return np.array([a-R[i,j] for i,j in ed])
  best=(-1,None)
  for it in range(100):
   w=rng.dirichlet(np.ones(k));p=rng.uniform(.2,.8,M);x=np.r_[w,p]
   res=minimize(lambda x:-calc(x),x,bounds=[(0,1)]*(k+M),constraints=[{'type':'eq','fun':lambda x:sum(x[:k])-1},{'type':'ineq','fun':con}],method='SLSQP',options={'maxiter':200,'ftol':1e-10})
   if res.success and -res.fun>best[0]:best=(-res.fun,unpack(res.x))
  target=max(.5,4*np.sqrt(a/3)-2*a)
  print(a,k,best[0],target,'gap',best[0]-target,flush=True)
  if best[0]>target+1e-6:print('COUNTER',best[1]);raise SystemExit
