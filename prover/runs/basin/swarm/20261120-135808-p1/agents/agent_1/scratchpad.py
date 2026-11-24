import numpy as np,itertools
from scipy.linalg import null_space
for s,n in [(2,4),(2,5),(3,6),(3,7)]:
 l=np.arange(n,dtype=float);rng=np.random.default_rng(42);N=1000
 w=rng.dirichlet(np.ones(n),N);V=np.array([l**j for j in range(s)]).T
 def step(w):
  M=np.einsum('ij,ni,ik->njk',V,w,V);rhs=-np.einsum('ij,ni,i->nj',V,w,l**s)
  a=np.linalg.solve(M,rhs[:,:,None])[:,:,0];p=l**s+a@V.T
  w=w*p*p;w/=w.sum(axis=1)[:,None];return w
 w2=step(step(w))
 for d in [1,2,3]:
  comb=list(itertools.combinations_with_replacement(range(n),d))
  feats=lambda v:np.array([np.prod(v[:,ind],axis=1) for ind in comb]).T
  diff=feats(w2)-feats(w)
  sv=np.linalg.svd(diff,compute_uv=False)
  print(s,n,d,sv[-5:]/sv[0],flush=True)
