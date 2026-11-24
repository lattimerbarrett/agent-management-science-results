import numpy as np
lam=np.array([1.,2.,3.,4.,5.,7.,10.]);s=2
y=np.ones(len(lam));y/=np.linalg.norm(y)
ys=[y.copy()];hs=[]
for k in range(2000):
    K=np.array([lam**j*y for j in range(s)]).T
    z=lam**s*y
    q=z-K@np.linalg.lstsq(K,z,rcond=None)[0]
    h=q@q
    y=q/np.sqrt(h)
    ys.append(y.copy());hs.append(h)
ys=np.array(ys)
d=np.linalg.norm(ys[2:]-ys[:-2],axis=1)
# The readily available telescoping estimate controls squared, not first, powers.
for N in [10,100,1000]:
 print(N, 'even length',sum(d[:2*N:2]), 'all squared displacements',sum(d[:2*N]**2), 'log bound',np.log(hs[min(2*N,len(hs)-1)]/hs[0]))
print('Maximum violation of squared-distance logarithmic bound:',max(d**2-np.log(np.array(hs[1:])/np.array(hs[:-1]))))
