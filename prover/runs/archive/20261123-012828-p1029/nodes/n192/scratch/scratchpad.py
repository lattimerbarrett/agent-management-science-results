import numpy as np
from scipy.linalg import sqrtm
b0=np.array([[.2,0.],[0.,.05]])
b1=np.array([[.1,.08],[.08,.1]])
r=np.eye(2)-b0-b1
V=np.vstack([sqrtm(b0),sqrtm(b1),sqrtm(r)])
P0=np.diag([1.,1.,0.,0.,0.,0.])
P1=np.diag([0.,0.,1.,1.,0.,0.])
print('Increment commutator norm:',np.linalg.norm(b0@b1-b1@b0))
print('Isometry error:',np.linalg.norm(V.T@V-np.eye(2)))
print('First compression error:',np.linalg.norm(V.T@P0@V-b0))
print('Join compression error:',np.linalg.norm(V.T@(P0+P1)@V-(b0+b1)))
print('Interpretation: finite partial sums are compressions of finite orthogonal joins.')
print('An infinite projection join gives the desired order supremum only with an appropriate order-continuous compression; projection completeness alone is not that assertion.')