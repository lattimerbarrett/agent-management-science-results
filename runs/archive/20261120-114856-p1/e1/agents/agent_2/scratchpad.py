import numpy as np
from scipy.optimize import linprog
rng=np.random.default_rng(142)
for dim in [3,4,5,6]:
 for k in range(10000):
  m=2*dim+2;n=2*dim;w=rng.uniform(.1,1,m);w/=sum(w);Q=rng.normal(size=m);Q-=w@Q;Q/=np.sqrt(w@(Q*Q));qsrc=rng.normal(size=n);qsrc[np.abs(qsrc)<.03]+=.1;A=np.c_[np.ones(m),Q,1/Q,rng.normal(size=(m,dim-3))];Z=np.c_[np.ones(n),qsrc,-1/qsrc,rng.normal(size=(n,dim-3))];G=A.T@(w[:,None]*A);H=A.T@((w*Q*Q)[:,None]*A);KG=Z@np.linalg.inv(G)@Z.T;KH=Z@np.linalg.inv(H)@Z.T;C=qsrc[None,:]/qsrc[:,None]*KG+qsrc[:,None]*qsrc[None,:]*KH;op=linprog(np.zeros(n),A_ub=-C.T,b_ub=-np.ones(n),bounds=(1e-8,None),method='highs')
  if not op.success:print('FAIL propergeneric',dim,k);break
 else:print('passed',dim)
