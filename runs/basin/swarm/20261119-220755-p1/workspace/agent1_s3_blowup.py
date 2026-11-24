import numpy as np
from scipy.optimize import root
base=np.array([-3.,-1.,1.,2.,3.]);d=np.array([np.prod([a-b for b in base if b!=a]) for a in base]);q=np.poly1d([1,0,-7,0]);roots=np.sort(np.roots([1,0,-7,np.sqrt(14)]));print(roots)
ext=roots[1:];x=np.r_[base,ext];s=3
V=np.array([x**j for j in range(7)]);VB=np.array([base**j for j in range(7)]);f0=np.array([5.,-7.,0.])
def monic(p,V):
 M=np.array([[p@V[i+j]for j in range(3)] for i in range(3)]);rhs=-np.array([p@V[i+3]for i in range(3)]);return np.linalg.solve(M,rhs)
def F(p):
 c=monic(p,V);f=V[3]+c@V[:3];z=p*f*f;return z/z.sum()
def coords(p):
 z=p[5:];w=p[:5]/sum(p[:5]);c=monic(w,VB);r=1/(d*d*w);theta=sum(base*r)/sum(r);return theta,c,z
def raw(y,eps):
 theta=y[0];u=y[1:4];Z=y[4:];c=f0+eps*u;f=VB[3]+c@VB[:3];w=(base-theta)/(d*f);w/=sum(w);z=eps**2*Z;p=np.r_[w*(1-sum(z)),z];tt,cc,zz=coords(F(F(p)))
 return np.r_[(tt-theta)/eps,(cc-c)/eps**2,(zz-z)/eps**3]
def field(y):return 2*raw(y,5e-5)-raw(y,1e-4)+np.r_[0,y[1:4],2*y[4:]]
