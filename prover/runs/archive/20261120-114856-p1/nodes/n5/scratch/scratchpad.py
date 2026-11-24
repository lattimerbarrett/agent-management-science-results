import numpy as np
from scipy.linalg import null_space
from numpy.polynomial import Polynomial as P
p=P([1,-1.25,.25]); q=P([1,-.7,.1]); F=p*q; c=.001
main=(F-c).roots(); other=(F+c).roots()
lam=np.r_[main,other]
print('main',main, 'other',other)
B=np.array([np.ones(4),main*p(main),main**2*p(main)])
w0=np.linalg.lstsq(B,np.array([1.,0.,0.]),rcond=None)[0]; d=null_space(B)[:,0]
lo=max(-w0[d>0]/d[d>0]); hi=min(-w0[d<0]/d[d<0]); print('weights',w0,'d',d,'interval',lo,hi)
w0+=d*(lo+hi)/2
v=np.sqrt(np.r_[w0*.999,np.ones(4)*.00025])
for k in range(1000000):
    # minimization in energy coordinates
    m=np.array([np.dot(v*v,lam**j) for j in range(1,5)])
    co=np.linalg.solve([[m[1],m[2]],[m[2],m[3]]],m[:2])
    z=v*(1-co[0]*lam-co[1]*lam**2); rho=np.linalg.norm(z); v=z/rho
    if k in [100,1000,10000,100000,999999]:
        print(k,rho,np.dot(v[:4]**2-w0,d),v**2)
