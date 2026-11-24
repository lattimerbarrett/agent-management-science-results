import numpy as np, scipy.linalg as la, mpmath as mp, json, time
from pathlib import Path

def mul(p,f):
 p=np.convolve(p,f);p/=np.max(np.abs(p));return p

def parameters(r,d,hs):
 hs=np.array(hs,dtype=np.longdouble); r=np.longdouble(r);d=np.longdouble(d)
 def z(h,r):
  out=np.empty_like(h);lo=h<=0
  out[lo]=r/(np.hypot(h[lo],r)-h[lo]);out[~lo]=(np.hypot(h[~lo],r)+h[~lo])/r
  return out
 return z(hs,r),z(hs-d,np.longdouble(1))

def blocksigns(m,r,d,hs):
 r=np.longdouble(r);d=np.longdouble(d)
 x,y=parameters(r,d,hs); k=len(x);n=k+2*m
 H=np.ones(1,dtype=np.longdouble)
 for j in range(1,m):H=np.r_[H,H[-1]/np.tan(np.longdouble(j)*np.pi/(2*m))]
 H/=max(H)
 A=np.ones(1,dtype=np.clongdouble);B=A.copy()
 for j in range(m):
  zz=np.exp(np.clongdouble(2j*np.pi*j/m))
  D=d+np.hypot(d,abs(zz-r)); cc=(zz.conjugate()-r)/D;bb=(1-r*zz)/D
  A=mul(A,[1,-cc]); B=mul(B,[bb,1])
 A=mul(A,H);B=mul(B,H)
 for u,v in zip(x,y):A=mul(A,[u,1]);B=mul(B,[v,1])
 out=[]
 for q in range(m):
  cols=list(range(q,n,m));ix=list(range(q,k,m));Q=np.zeros((len(cols),len(cols)))
  for j,i in enumerate(ix):
   if x[i]<=1:
    u=x[i]**m;v=y[i]**m;row=np.array([1,-u-v,u*v],dtype=np.longdouble)
   else:
    u=x[i]**(-m);v=y[i]**(-m);row=np.array([u*v,-u-v,1],dtype=np.longdouble)
   row/=max(abs(row));Q[j,j:j+3]=row
  Q[-2]=A[cols].real;Q[-1]=B[cols].real
  Q[-2]/=max(abs(Q[-2]));Q[-1]/=max(abs(Q[-1]));
  out.append(la.det(Q,check_finite=False))
 return out,x,y

def hpblocks(m,r,d,hs,prec=100):
 mp.mp.dps=prec;r=mp.mpf(str(r));d=mp.mpf(str(d));hs=list(map(lambda h:mp.mpf(str(h)),hs))
 def z(h,r):return r/(mp.sqrt(h*h+r*r)-h) if h<=0 else (mp.sqrt(h*h+r*r)+h)/r
 x=[z(h,r) for h in hs];y=[z(h-d,mp.mpf(1)) for h in hs]
 def conv(p,f):
  q=[mp.mpc(0)]*(len(p)+len(f)-1)
  for i,a in enumerate(p):
   for j,b in enumerate(f):q[i+j]+=a*b
  scale=max(map(abs,q));return [a/scale for a in q]
 H=[mp.mpf(1)]
 for j in range(1,m):H.append(H[-1]*mp.cot(mp.pi*j/(2*m)))
 A=[1];B=[1]
 for j in range(m):
  zz=mp.exp(2j*mp.pi*j/m);D=d+mp.sqrt(d*d+abs(zz-r)**2)
  A=conv(A,[1,-(zz.conjugate()-r)/D]);B=conv(B,[(1-r*zz)/D,1])
 A=conv(A,H);B=conv(B,H)
 for u,v in zip(x,y):A=conv(A,[u,1]);B=conv(B,[v,1])
 out=[];n=len(x)+2*m
 for q in range(m):
  cols=list(range(q,n,m));ix=list(range(q,len(x),m));Q=mp.matrix(len(cols))
  for j,i in enumerate(ix):
   u=x[i]**m;v=y[i]**m;Q[j,j]=1;Q[j,j+1]=-u-v;Q[j,j+2]=u*v
  for j,t in enumerate(cols):Q[len(cols)-2,j]=A[t].real;Q[len(cols)-1,j]=B[t].real
  out.append(mp.det(Q))
 return out

