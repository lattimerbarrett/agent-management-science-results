import numpy as np
from itertools import product
rng=np.random.default_rng(244)
D=11.;delta=5.;activeX=np.array([-3.,-2.,-1.,1.,2.,3.]);R=np.poly(activeX);Rp=np.polyder(R)
rootA=np.sort(np.r_[np.roots([1,0,-7,-delta]),np.roots([1,0,-7,delta])])
extX=np.sort(np.r_[np.roots([1,0,-7,-np.sqrt(36-2*D)]),np.roots([1,0,-7,np.sqrt(36-2*D)])])
x=np.r_[activeX,extX];z=x/3;V=np.array([z**j for j in range(3)]).T;M=np.array([np.outer(v,v) for v in V]);B0=V*z[:,None]**3
w0=[]
for bits in product([0,1],repeat=3):
 qroots=rootA[[2*j+1-b for j,b in enumerate(bits)]];q=np.poly(qroots)
 for j in range(50):
  be=np.array([rng.uniform(-1.9,-1.1),rng.uniform(1.1,1.9)])
  wa=np.polyval(q,activeX)*np.polyval(np.poly(be),activeX)/np.polyval(Rp,activeX);wa/=sum(wa)
  we=rng.dirichlet(np.ones(6))*.00001
  w=np.r_[wa*(1-sum(we)),we];w0.append(w)
w=np.array(w0);w0=w.copy();N=len(w);prev=w.copy();dist=np.zeros(N);distold=dist.copy()
for k in range(500001):
 if k%1000==0:
  dist+=np.linalg.norm(w-prev,axis=1);prev=w.copy()
 if k%100000==0:
  print(k,'active6',np.count_nonzero(w[:,:6].min(axis=1)>1e-5),'ext',np.max(w[:,6:].sum(axis=1)),'travel',np.max(dist-distold),'total',dist.max(),flush=True)
  distold=dist.copy();np.savez('s3negative%d.npz'%k,w=w,w0=w0,dist=dist,z=z)
 c=np.linalg.solve(np.einsum('ni,ijk->njk',w,M),(-w@B0)[:,:,None])[:,:,0]
 pp=z**3+c@V.T;w=w*pp*pp;w/=w.sum(axis=1)[:,None]
