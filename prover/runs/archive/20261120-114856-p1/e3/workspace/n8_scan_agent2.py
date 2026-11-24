import numpy as np
rng=np.random.default_rng(194)
core=np.array([-np.sqrt((5+2*np.sqrt(6))/4),-np.sqrt((5-2*np.sqrt(6))/4),np.sqrt((5-2*np.sqrt(6))/4),np.sqrt((5+2*np.sqrt(6))/4)])
extra=np.array([-np.sqrt((5+2*np.sqrt(2))/4),-np.sqrt((5-2*np.sqrt(2))/4),np.sqrt((5-2*np.sqrt(2))/4),np.sqrt((5+2*np.sqrt(2))/4)])
lam=np.r_[core,extra];A=np.array([np.ones(4),core,core**2,core**3]);Inv=np.linalg.inv(A)
v0=Inv@np.array([1,0,.75,-.75]);v1=Inv@np.array([0,1,-1,1.75])
lo=max(-v0[v1>0]/v1[v1>0]);hi=min(-v0[v1<0]/v1[v1<0]);print('mline',lo,hi,flush=True)
N=3000;m=rng.uniform(lo+1e-4,hi-1e-4,N);r=10**rng.uniform(-5,-1,N);h=r*rng.normal(size=N);z=r*rng.normal(size=N)
wc=np.array([np.ones(N),m,.75-m+h,1.75*m-.75-h+z]).T@Inv.T
we=(r*r)[:,None]*np.exp(rng.uniform(-12,4,(N,4)))
w=np.c_[wc,we];w=w[(w>0).all(axis=1)];w/=w.sum(axis=1)[:,None]
print('valid',len(w),flush=True);initial=w.copy()
def T(w):
 m=w@lam;m2=w@(lam**2);m3=w@(lam**3);a=(m*m2-m3)/(m2-m*m);b=-m2-a*m
 q=lam[None,:]**2+a[:,None]*lam+b[:,None];w=w*q*q;return w/w.sum(axis=1)[:,None]
last=w@lam;direction=np.zeros(len(w));turns=np.zeros(len(w),int);maxturn=0;hist=[]
for k in range(200001):
 w=T(T(w))
 if k%1000==0:
  mm=w@lam;delta=mm-last;sign=np.where(abs(delta)>1e-7,np.sign(delta),0)
  turns+=((sign*direction)<0);direction=np.where(sign!=0,sign,direction);last=mm
  hist.append(mm)
  if turns.max()>maxturn:
   maxturn=turns.max();ix=np.argmax(turns);print('newmaxturn',k,maxturn,'ix',ix,'m',mm[ix],flush=True)
   np.savez('workspace/n8_multiturn_agent2.npz',lam=lam,w0=initial[ix],index=ix,hist=np.array(hist)[:,ix],turns=turns)
 if k%20000==0:print('iter',k,'turns',np.unique(turns,return_counts=True),flush=True)
np.savez('workspace/n8_scan_agent2.npz',lam=lam,initial=initial,w=w,turns=turns,hist=np.array(hist))
from pathlib import Path
Path('workspace/n8_scan_agent2.py').write_text(Path(__file__).read_text())
