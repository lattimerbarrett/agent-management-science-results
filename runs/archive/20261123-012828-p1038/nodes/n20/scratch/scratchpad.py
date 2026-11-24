import numpy as np

def mul(fs):
 p=np.array([1.])
 for f in fs: p=np.convolve(p,f)
 return p

def blocks(m,heights,r=.7,R=1.2,d=1.):
 h=np.array(heights)
 x=(h+np.hypot(h,r))/r
 y=(h-d+np.hypot(h-d,R))/R
 z=np.exp(2j*np.pi*np.arange(m)/m)
 D=d+np.sqrt(d*d+abs(R*z-r)**2)
 c=(R/z-r)/D; b=z*c
 H=mul([[1,1j*np.exp(-1j*np.pi*k/m)] for k in range(1,m)])
 A=np.convolve(np.convolve(H,mul([[1,-v] for v in c])),mul([[v,1] for v in x]))
 B=np.convolve(np.convolve(H,mul([[v,1] for v in b])),mul([[v,1] for v in y]))
 out=[]
 for q in range(m):
  idx=list(range(q,len(h),m)); C=len(idx)
  K=np.zeros((C+2,C+2),complex)
  for j,i in enumerate(idx):
   u=x[i]**m;v=y[i]**m
   K[j,j:j+3]=[1,-u-v,u*v]
  K[-2]=A[q::m];K[-1]=B[q::m]
  out.append(np.linalg.det(K))
 return out
rng=np.random.default_rng(2)
for m in range(1,9):
 h=np.r_[-np.cumsum(rng.uniform(.3,2,4))[::-1],1+np.cumsum(rng.uniform(.3,2,3))]
 print(m,blocks(m,h))
