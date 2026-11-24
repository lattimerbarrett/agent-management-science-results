import numpy as np
from scipy.optimize import root
l=np.array([1.,2.,4.,5.])
def T(v):
 K=np.array([l*v,l*l*v]).T
 c=np.linalg.solve(K.T@K,K.T@v)
 z=v-K@c
 return z/np.linalg.norm(z),np.linalg.norm(z)
v=np.sqrt(np.array([.1,.2,.3,.4]))
w,r=T(v); z,r2=T(w)
print(v,w,z,r,r2, 'diff',z-v)
for k in range(1000):
 v,r=T(v)
print(v,r)
P=np.poly(l); t=1.0; pp=P.copy();pp[-1]+=t
roots=np.sort(np.roots(pp).real)
p=np.poly(roots[[0,2]]);p/=p[-1]
q=np.poly(roots[[1,3]]);q/=q[-1]
pv=np.polyval(p,l)
M=np.array([np.ones(4),l*pv,l*l*pv])
w0=np.linalg.lstsq(M,np.array([1.,0.,0.]),rcond=None)[0]
print('roots',roots,'p',p,'q',q,'w',w0)
if np.min(w0)>0:v=np.sqrt(w0)
print('F diff',T(T(v)[0])[0]-v)
# finite difference D(T2) at limit
F=lambda v:T(T(v/np.linalg.norm(v))[0])[0]
eps=1.e-6
D=np.column_stack([(F(v+eps*np.eye(4)[i])-F(v-eps*np.eye(4)[i]))/(2*eps) for i in range(4)])
print(np.linalg.eigvals(D)); print(D)
