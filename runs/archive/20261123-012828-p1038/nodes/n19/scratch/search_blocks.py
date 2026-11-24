import numpy as np
from scipy.linalg import lu_factor

def convnorm(p,q):
 p=np.convolve(p,q); return p/max(abs(p))

def canonical(m,r,R,d,heights):
 k=np.arange(m); z=np.exp(2j*np.pi*k/m)
 w=R*z-r; ds=d+np.hypot(d,abs(w)); cs=w.conjugate()/ds; bs=z*cs
 H=np.array([1.],dtype=np.longdouble)
 for j in range(1,m): H=np.append(H,H[-1]/np.tan(np.pi*j/(2*m)))
 H/=max(H)
 Q=np.array([1.],dtype=np.longdouble); B=np.array([bs[0].real,1.],dtype=np.longdouble)
 for j in range(1,(m+1)//2):
  Q=convnorm(Q,[1,-2*cs[j].real,abs(cs[j])**2])
  B=convnorm(B,[abs(bs[j])**2,2*bs[j].real,1])
 if m%2==0:
  Q=convnorm(Q,[1,-cs[m//2].real]);B=convnorm(B,[bs[m//2].real,1])
 A=convnorm(H,Q); B=convnorm(H,B)
 xs=[];ys=[]
 for h in heights:
  x=np.exp(np.arcsinh(h/r)); y=np.exp(np.arcsinh((h-d)/R))
  xs.append(x);ys.append(y)
  A=convnorm(A,[x,1]); B=convnorm(B,[y,1])
 A=convnorm(A,[1,-cs[0].real]);
 blocks=[];n=len(heights)+2*m
 for q in range(m):
  cols=list(range(q,n,m)); C=np.zeros((len(cols),len(cols)),dtype=np.longdouble)
  for j,i in enumerate(range(q,len(heights),m)):
   lx=m*np.log(xs[i]);ly=m*np.log(ys[i]);lmax=max(0,lx,ly,lx+ly)
   C[j,j:j+3]=[np.exp(-lmax),-np.exp(lx-lmax)-np.exp(ly-lmax),np.exp(lx+ly-lmax)]
  C[-2,:]=A[q::m];C[-1,:]=B[q::m]
  for _ in range(5):
   C/=np.maximum(np.max(abs(C),axis=1),np.finfo(np.longdouble).tiny)[:,None]
   C/=np.maximum(np.max(abs(C),axis=0),np.finfo(np.longdouble).tiny)[None,:]
  blocks.append(np.array(C,dtype=float))
 return blocks

def signs(m,r,R,d,heights):
 return [np.linalg.slogdet(C)[0] for C in canonical(m,r,R,d,heights)]
