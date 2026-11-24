import numpy as np,itertools
from scipy.optimize import root
base=np.array([-3.,-1.,0.,1.,2.,3.]);nbase=6;s=4;d=np.array([np.prod([a-b for b in base if b!=a])for a in base]);P=np.poly1d(np.poly(base));f=np.poly1d([1,0,-4.5,0,63/40]);g=np.poly1d([1,0,-9.5,0,187/40]);L=11781/1600;negroots=np.sort(np.roots(f*g+L));negroots=np.array([v.real for v in negroots if abs(v.imag)<1e-7]);print('neg',negroots)
VB=np.array([base**j for j in range(2*s+1)]);f0=np.array(f.c[:0:-1]);
def monic(p,V):
 M=np.array([[p@V[i+j]for j in range(s)]for i in range(s)]);return np.linalg.solve(M,-np.array([p@V[i+s]for i in range(s)]))
def setup(ext):
 global V
 x=np.r_[base,ext];V=np.array([x**j for j in range(2*s+1)])
def F(p):
 c=monic(p,V);z=p*(V[s]+c@V[:s])**2;return z/z.sum()
def raw(y,eps):
 t=y[0];c=f0+eps*y[1:1+s];ff=VB[s]+c@VB[:s];w=(base-t)/(d*ff);w/=sum(w);z=eps**2*y[1+s:];p=np.r_[w*(1-sum(z)),z];p=F(F(p));w=p[:nbase]/sum(p[:nbase]);cc=monic(w,VB);q=1/(d*d*w);tt=(base@q)/sum(q);return np.r_[(tt-t)/eps,(cc-c)/eps**2,(p[nbase:]-z)/eps**3]
def field(y):return 2*raw(y,5e-5)-raw(y,1e-4)+np.r_[0,y[1:1+s],2*y[1+s:]]
