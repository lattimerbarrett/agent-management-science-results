import numpy as np
from pathlib import Path
rng=np.random.default_rng(914)
maxerr=0.
for p in [2.1,2.5,3,5,10]:
 q=p/(p-1);beta=1/(p-1);L=np.log(100);delta=.5-.001-1/(2*q)
 assert delta>0
 for _ in range(200):
  t=np.arange(10001)*.001
  Z=np.r_[0,np.cumsum(rng.normal(0,np.sqrt(.001),10000))]+t/(2*q)
  V=Z+delta*t
  X=L-(np.maximum.accumulate(V)-V)
  stop=np.flatnonzero(X<=0)
  n=stop[0] if len(stop) else len(X)
  Z=Z[:n];X=X[:n]
  lhs=np.maximum.accumulate(Z+q*beta*X)
  rhs=np.maximum.accumulate(Z)+q*beta*L
  error=np.max(np.abs(lhs-rhs))
  maxerr=max(maxerr,error)
  assert error<1e-10
print('1000 actual Brownian paths: exact coupled barrier identity max error',maxerr)
Path('workspace/agent2_coupled_barrier_check.py').write_text(Path(__file__).read_text())
