from pathlib import Path
import numpy as np
rng=np.random.default_rng(731)
worst=0.;checked=0
for p in [1.2,1.5,2.,2.5,3.,5.]:
 q=p/(p-1)
 for trial in range(40):
  hs=rng.normal(0,3,4)+1j*rng.normal(0,3,4)
  phases=rng.integers(0,4,12)
  ds=np.exp(rng.uniform(-2,2,(12,2)))
  Ts=np.array([[[1,h],[0,1]] for h in hs],complex)
  Ms=np.array([np.diag(d)@Ts[j] for d,j in zip(ds,phases)])
  roots=np.linalg.inv(Ms).conj().transpose(0,2,1)
  norms=np.empty((12,12))
  for x in range(12):
   for y in range(12):norms[x,y]=np.linalg.norm(roots[x]@np.linalg.inv(roots[y]),2)
  B=np.mean(np.mean(norms**p,axis=1)**(q-1))
  original=np.empty((12,12))
  for x in range(12):
   for y in range(12):original[x,y]=np.linalg.norm(Ms[x]@np.linalg.inv(Ms[y]),2)
  A=np.mean(np.mean(original**q,axis=1)**(p-1))
  for j in range(4):
   for k in range(2):
    v=Ts[j].conj().T[:,k]
    z=np.linalg.norm(roots@v,axis=1)**q
    u=z**(-(p-1))
    scalar=np.mean(u)*np.mean(u**(-1/(p-1)))**(p-1)
    assert scalar<=B**(p-1)*(1+1e-8)
    assert scalar<=A*(1+1e-8)
    matching=phases==j
    if np.any(matching):
     err=np.max(np.abs(u[matching]/ds[matching,k]**p-1))
     worst=max(worst,err)
     assert err<1e-8
    checked+=1
print('Finite-row identity and actual scalar-vs-dual characteristic checks:',checked,'max identity error=',worst)
Path('workspace/agent2_finite_row_checks.py').write_text(Path(__file__).read_text())