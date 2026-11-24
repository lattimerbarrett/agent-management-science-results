import numpy as np
from math import pi

def mul(p,q): return np.convolve(p,q)
def H(m):
 p=np.ones(1,dtype=np.clongdouble)
 for k in range(1,m): p=mul(p,np.array([1,1j*np.exp(-1j*pi*k/m)],dtype=np.clongdouble))
 return p.real.astype(float)
def rows(m,lo,hi,hm,hp,r,R):
 # Real canonical polynomials; upper axis factors scaled to constant 1.
 z=np.exp(2j*pi*np.arange(m)/m)
 D=hp-hm+np.sqrt((hp-hm)**2+abs(R*z-r)**2)
 cs=(R/z-r)/D; bs=(R-r*z)/D
 A=H(m).astype(complex); B=A.copy()
 for c,b in zip(cs,bs): A=mul(A,[1,-c]); B=mul(B,[b,1])
 for l in lo:
  x=r/(hm-l+np.hypot(hm-l,r)); y=R/(hp-l+np.hypot(hp-l,R))
  A=mul(A,[x,1]); B=mul(B,[y,1])
 for u in hi:
  x=r/(u-hm+np.hypot(u-hm,r)); y=R/(u-hp+np.hypot(u-hp,R))
  A=mul(A,[1,x]); B=mul(B,[1,y])
 return A.real,B.real

def reduced(m,lo,hi,hm,hp,r,R,lim=None):
 n=len(lo)+len(hi)+2*m; a=len(lo)
 if lim=='same':
  # d=0, r=R=1, (R-r)/d=1, so kappa=sqrt(2)-1.
  F=mul(H(m),H(m)); kappa=np.sqrt(2)-1
  for l in lo: F=mul(F,[1/(-l+np.hypot(l,1)),1])
  for u in hi: F=mul(F,[1,1/(u+np.hypot(u,1))])
  A=mul(F,[1,-kappa]); B=mul(F,[kappa,1])
 else: A,B=rows(m,lo,hi,hm,hp,r,R)
 blocks=[]
 for q in range(m):
  cols=list(range(q,n,m)); Z=[]
  for j,l in enumerate(lo):
   if j%m==q:
    x=(r/(hm-l+np.hypot(hm-l,r)))**m
    y=(R/(hp-l+np.hypot(hp-l,R)))**m
    p=np.zeros(n); p[j]=1;p[j+m]=-x-y;p[j+2*m]=x*y
    Z.append(p[cols])
  for j,u in enumerate(hi):
   s=a+j
   if s%m==q:
    x=(r/(u-hm+np.hypot(u-hm,r)))**m
    y=(R/(u-hp+np.hypot(u-hp,R)))**m
    p=np.zeros(n);p[s]=x*y;p[s+m]=-x-y;p[s+2*m]=1
    Z.append(p[cols])
  Z.extend([A[cols],B[cols]])
  blocks.append(np.array(Z))
 return blocks

if __name__=='__main__':
 import mpmath as mp
 mp.mp.dps=80
 for mm in [1,2,3,4,5,7,11,16,24,31,40,61,96,127]:
  hh=[mp.mpf(1)]
  for j in range(1,mm): hh.append(hh[-1]*mp.cot(mp.pi*j/(2*mm)))
  ff=[sum(hh[j]*hh[t-j] for j in range(max(0,t-mm+1),min(mm-1,t)+1)) for t in range(2*mm-1)]
  val=lambda j: ff[j] if 0<=j<len(ff) else mp.mpf(0)
  limits=[val(0)*val(mm-1)]+[val(q)*val(q+mm-1)-val(q-1)*val(q+mm) for q in range(1,mm)]
  print('exact-form leading core, m=',mm,'all coefficients >0:',all(x>0 for x in limits))
 lo=[-2.,-1.]; hi=[1.,2.]
 for m in [1,2,3,4,5,6,7,8,9,10,12,16,20,24,30,40,60]:
  # block row order introduces q-dependent orientation, removed by reference.
  ref=reduced(m,lo,hi,0,.5,.7,1.4)
  sg=np.array([np.linalg.slogdet(v)[0] for v in ref])
  same=reduced(m,lo,hi,0,0,1,1,'same')
  same_sign=np.array([np.linalg.slogdet(v)[0] for v in same])*sg
  collapsed=reduced(m,lo,hi,0,.5,0,1.4)
  collapsed_sign=np.array([np.linalg.slogdet(v)[0] for v in collapsed])*sg
  min_same=min(abs(np.linalg.det(v/np.max(abs(v),axis=1)[:,None])) for v in same)
  min_coll=min(abs(np.linalg.det(v/np.max(abs(v),axis=1)[:,None])) for v in collapsed)
  print(m,'same-circle signs',sorted(set(same_sign)), 'axis signs', sorted(set(collapsed_sign)), 'min normalized |limits|',min_same,min_coll)
