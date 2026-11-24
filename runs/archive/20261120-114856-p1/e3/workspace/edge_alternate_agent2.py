import numpy as np,time
f=np.load('workspace/alternateH_0.001_agent3.npz');lam=f['l'];starts=f['start'];ends=f['w'];mend=ends@lam
left=24;rights=np.where(mend>-.75)[0];ri=rights[np.argmin(np.linalg.norm(starts[rights]-starts[left],axis=1))]
print('pair',left,ri,'distance',np.linalg.norm(starts[left]-starts[ri]),'mend',mend[left],mend[ri],flush=True)
l2=lam*lam;l3=l2*lam

def iterate(w,steps=100000):
 lw=np.log(w);turns=0;side=0
 for k in range(steps*2):
  ww=np.exp(lw-lw.max());ww/=ww.sum();m=ww@lam;m2=ww@l2;m3=ww@l3;a=(m*m2-m3)/(m2-m*m);b=-m2-a*m;q=l2+a*lam+b;lw+=2*np.log(abs(q));lw-=lw.max()
  if k%2000==0:
   nside=1 if m>-.75 else(-1 if m<-1.25 else 0)
   if nside and nside!=side:turns+=1;side=nside
 ww=np.exp(lw-lw.max());ww/=ww.sum();m=ww@lam;m2=ww@l2;m3=ww@l3;a=(m*m2-m3)/(m2-m*m);b=-m2-a*m;q=l2+a*lam+b;H=ww@(q*q)
 return m,H,turns,lw
lo=0.;hi=1.;hist=[]
for k in range(28):
 mid=(lo+hi)/2;w=(1-mid)*starts[left]+mid*starts[ri];m,H,t,lw=iterate(w)
 print(k,repr(mid),'m,H,turns',m,H,t,flush=True);hist.append([mid,m,H,t])
 if m< -1:lo=mid
 else:hi=mid
 np.savez('workspace/edge_alternate_agent2.npz',hist=np.array(hist),lo=lo,hi=hi,left=starts[left],right=starts[ri],lam=lam,lw=lw)
from pathlib import Path
Path('workspace/edge_alternate_agent2.py').write_text(Path(__file__).read_text())
