import numpy as np
rng=np.random.default_rng(123)
x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
C=np.linalg.norm(x,2)
Gs=[]
for k in range(1,5):
    V=np.vstack([np.eye(4)[:,:k],x[:,:k]])
    G=V@np.linalg.inv(V.conj().T@V)@V.conj().T
    Gs.append(G)
    E=np.diag([1.]*4+[0.]*4)
    print(k,'projection error',np.linalg.norm(G@G-G),
          'angle min eig',np.linalg.eigvalsh(G@E@G-G/(1+C*C)).min())
for k in range(3):
    print('nesting error',k+1,np.linalg.norm(Gs[k+1]@Gs[k]-Gs[k]))
G=Gs[-1]
x_rec=G[4:,:4]@np.linalg.inv(G[:4,:4])
print('reconstruction error',np.linalg.norm(x_rec-x))
