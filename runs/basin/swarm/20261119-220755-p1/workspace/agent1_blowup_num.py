import numpy as np
from scipy.optimize import root
alpha=np.sqrt(2);N0=7.;base=np.array([-3.,-1.,1.,3.]);d=4*base**3-20*base
ext=np.array([-np.sqrt(5+np.sqrt(2)),-np.sqrt(5-np.sqrt(2)),np.sqrt(5-np.sqrt(2)),np.sqrt(5+np.sqrt(2))]);xx=np.r_[base,ext]
def monic(p,x):
 m=[sum(p*x**j)for j in range(5)];den=m[0]*m[2]-m[1]**2
 b=(m[1]*m[3]-m[2]**2)/den;a=(m[1]*m[2]-m[0]*m[3])/den
 return a,b
def F(p):
 a,b=monic(p,xx);z=p*(xx*xx+a*xx+b)**2;return z/sum(z)
def coords(p):
 z=p[4:];w=p[:4]/sum(p[:4]);a,b=monic(w,base);q=1/(d*d*w);t=sum(base*q)/sum(q);return t,a,10+2*b-a*a,z

def raw(y,eps=0.0001):
 t,A,C=y[:3];Z=y[3:];a=alpha+eps*A;E=eps*C;b=(a*a-10+E)/2
 w=(base-t)/(d*(base*base+a*base+b));w/=sum(w);z=eps*eps*Z;p=np.r_[w*(1-sum(z)),z]
 t2,a2,E2,z2=coords(F(F(p)))
 return np.r_[(t2-t)/eps,(a2-a)/eps**2,(E2-E)/eps**2,(z2-z)/eps**3]
def field(y):
 return 2*raw(y,.00005)-raw(y,.0001)+np.r_[0,y[1],y[2],2*y[3:]]
