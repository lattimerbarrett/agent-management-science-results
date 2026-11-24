import numpy as np
from scipy.integrate import solve_ivp
s=4;base=np.arange(-3.,4.);nb=len(base);d=np.array([np.prod([a-b for b in base if a!=b])for a in base]);P=np.poly1d(np.poly(base));L=1.;prod=P*np.poly1d([1,0])+L;tpol=np.array([1,-14,49,-36,L]);tr=np.sort(np.roots(tpol));print('t roots',tr)
f=np.poly1d([1,0,-tr[0],0,0]) # overwrite
f=np.poly1d([1,0,-(tr[0]+tr[2]),0,tr[0]*tr[2]]);g=np.poly1d([1,0,-(tr[1]+tr[3]),0,tr[1]*tr[3]]);print(f,g)
neg=np.sort(np.roots(prod+L));neg=np.array([z.real for z in neg if abs(z.imag)<1e-8]);print('negative',neg);mu=neg[neg>0][0];x=np.r_[base,mu];V=np.array([x**j for j in range(9)]);VB=V[:,:nb];f0=f.c[:0:-1].copy()
def monic(p,V):
 M=np.array([[p@V[i+j]for j in range(s)]for i in range(s)]);return np.linalg.solve(M,-np.array([p@V[i+s]for i in range(s)]))
def F(p):
 c=monic(p,V);v=V[s]+c@V[:s];z=p*v*v;return z/z.sum()
def raw(y,eps):
 H=base*base+y[0]*base+y[1];c=f0+eps*y[2:6];ff=VB[s]+c@VB[:s];w=H/(d*ff);w/=sum(w);z=eps*eps*y[6];p=np.r_[w*(1-z),z];p=F(F(p));w=p[:nb]/sum(p[:nb]);cc=monic(w,VB);HH=w*d*(VB[s]+cc@VB[:s]);hc=np.polynomial.polynomial.polyfit(base,HH,2);hc/=hc[2];return np.r_[(hc[1]-y[0])/eps,(hc[0]-y[1])/eps,(cc-c)/eps**2,(p[-1]-z)/eps**3]
def field(y):return 2*raw(y,5e-5)-raw(y,1e-4)+np.r_[0.,0.,y[2:6],2*y[6]]
