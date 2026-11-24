import numpy as np
import sympy as s
r=s.symbols('r',positive=True)
assert s.simplify((r-1)/(r-1/r)-r/(r+1))==0
# r here is sqrt(lambda/mu), k=(r-1/r)^2.
rng=np.random.default_rng(2026)
for trial in range(200):
    lam=np.exp(rng.uniform(0,6)); mu=np.exp(rng.uniform(-6,0))
    probs=rng.random(8); probs/=sum(probs)
    ang=rng.uniform(0,np.pi,8)
    P=[np.outer([np.cos(t),np.sin(t)],[np.cos(t),np.sin(t)]) for t in ang]
    meanP=sum(t*a for t,a in zip(probs,P))
    W=[lam*a+mu*(np.eye(2)-a) for a in P]
    meanW=sum(t*a for t,a in zip(probs,W))
    meanInv=sum(t*np.linalg.inv(a) for t,a in zip(probs,W))
    k=(lam-mu)**2/(lam*mu)
    lhs=np.trace(meanW@meanInv)
    rhs=2+k*np.trace(meanP-meanP@meanP)
    assert abs(lhs-rhs)<1e-7*max(1,abs(rhs)),(lhs,rhs)
print('PASS: fixed-spectrum obstruction exact coefficient identity and 200 moment identities.')
