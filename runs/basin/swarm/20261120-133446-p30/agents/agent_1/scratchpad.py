import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from itertools import product,combinations
import time
rng=np.random.default_rng(123)
A=[];B=[];pairs=[]
for cs in combinations(range(1,6),2):
    ca={0,*cs}
    for choose in product(range(3),repeat=6):
        cuts=[3*c+choose[c] for c in range(6)]
        A.append([cuts[c] for c in range(6) if c in ca])
        B.append([cuts[c] for c in range(6) if c not in ca])
        pairs.append([[3*c+k for k in range(3) if k!=choose[c]] for c in range(6)])
A=np.array(A);B=np.array(B);pairs=np.array(pairs)
ones=np.ones((len(A),3,1))
def count(P):
    aa=np.linalg.solve(P[A],ones)[...,0]
    bb=np.linalg.solve(P[B],ones)[...,0]
    vals=(np.einsum('gkhi,gi->gkh',P[pairs],aa)-1)*(np.einsum('gkhi,gi->gkh',P[pairs],bb)-1)
    return np.sum(np.all(vals[:,:,0]*vals[:,:,1]<0,axis=1))
t=np.linspace(-1,1,18)
P=np.polynomial.chebyshev.chebvander(t,3)[:,1:]
print('moment curve',count(P),flush=True)
start=time.time();best=1000
for restart in range(20):
    Q=P.copy() if restart%3==0 else (rng.normal(size=(18,3)) if restart%3==1 else np.load('best_pizza.npy').copy())
    Q-=Q.mean(axis=0);Q=np.linalg.qr(Q)[0]*3
    c=count(Q)
    for step in range(3000):
        R=Q.copy();scale=10**rng.uniform(-2,.7)
        if rng.random()<.8:R[rng.integers(18)]+=scale*rng.normal(size=3)
        else:R+=scale*rng.normal(size=(18,3))
        cc=count(R)
        temperature=.1
        if cc<=c or rng.random()<np.exp((c-cc)/temperature):Q=R;c=cc
        if c<best:
            best=c;np.save('best_pizza.npy',Q)
            print('best',best,'restart',restart,'step',step,'sec',time.time()-start,flush=True)
        if best==0:raise SystemExit
    print('restart',restart,'end',c,flush=True)
