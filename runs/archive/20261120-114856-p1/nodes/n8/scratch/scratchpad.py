import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy.optimize import linprog
rng=np.random.default_rng(128)
lam0=np.arange(1.,7.);W=Poly.fromroots(lam0);delta=225/128
roots=np.sort((W+delta).roots());p=Poly.fromroots(roots[::2]);p/=p(0)
M=np.vstack([np.ones(6)]+[p(lam0)*lam0**j for j in range(3)])
vertices=[]
for i in range(60):
 sol=linprog(rng.normal(size=6),A_eq=M,b_eq=[1,0,0,0],bounds=[(0,None)]*6,method='highs')
 if sol.success and not any(np.linalg.norm(sol.x-v)<1e-8 for v in vertices): vertices.append(sol.x)
vertices=np.array(vertices);print('vertices',vertices)
B=100
weights=rng.dirichlet(np.ones(len(vertices)),size=B)@vertices
initial=weights.copy();eps=1e-5
v=np.column_stack([weights*(1-eps),np.full(B,eps)])
x=np.append(lam0,3.5);x=(x-x.mean())/5

def step(w):
 prev=np.zeros_like(w);pol=np.ones_like(w);b=np.zeros(B)
 for j in range(3):
  nn=np.sum(w*pol*pol,axis=1)
  a=np.sum(w*x*pol*pol,axis=1)/nn
  new=(x-a[:,None])*pol-b[:,None]*prev
  b=np.sum(w*new*new,axis=1)/nn
  prev,pol=pol,new
 w=w*pol*pol
 return w/np.sum(w,axis=1)[:,None]
history=[]
for k in range(1,20001):
 v=step(step(v))
 if k in [10,100,1000,5000,10000,20000]:
  history.append(v.copy()); print('k',k,'max z',max(v[:,-1]),'median z',np.median(v[:,-1]))
scores=np.linalg.norm(history[-1]-history[-2],axis=1)
for i in np.argsort(scores)[-5:]:
 print('trial',i,'score',scores[i],'init',initial[i])
 for k,h in zip([10,100,1000,5000,10000,20000],history): print(k,h[i])
np.savez('scan7.npz',initial=initial,history=history,scores=scores)
