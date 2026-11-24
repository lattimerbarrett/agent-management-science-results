import numpy as np
lam=np.array([1.,2.,3.,4.,5.,7.,10.])
v=np.ones(7);v/=np.linalg.norm(v)
for k in range(20000):
    K=np.array([lam*v,lam**2*v]).T
    c=np.linalg.lstsq(K,v,rcond=None)[0]
    z=v-K@c; rho=np.linalg.norm(z); v=z/rho
    if k in [100,1000,19999]: print(k,rho,v)
