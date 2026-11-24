import numpy as np
lam=np.array([1.,2.,4.,9.,20.])
r=np.array([1.,2.,-1.,3.,2.]); s=2
for k in range(8):
    u=r/np.sqrt(lam); u/=np.linalg.norm(u)
    K=np.column_stack([lam**j*u for j in range(1,s+1)])
    c=np.linalg.lstsq(K,u,rcond=None)[0]
    p=1-sum(c[j-1]*lam**j for j in range(1,s+1))
    rn=p*r
    tau=np.linalg.norm(rn/np.sqrt(lam))/np.linalg.norm(r/np.sqrt(lam))
    print(k, 'energy contraction',tau, 'residual contraction',np.linalg.norm(rn)/np.linalg.norm(r))
    if k:
        un=rn/np.sqrt(lam); un/=np.linalg.norm(un)
        print('identity discrepancy',np.dot(un,uprev)-tauprev/tau)
    uprev=u.copy(); tauprev=tau
    r=rn
