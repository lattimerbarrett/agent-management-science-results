import numpy as np,time
D=np.longdouble
f=np.load('workspace/alternateH_0.001_agent3.npz');lam=f['l'].astype(D);w=f['start'][24].astype(D)
# Reconstruct exactalgebraicspectrumratherthanroundedloadedfloat.
H=D('.001');
coreT=np.sqrt(D('6.25')-4*(D('.5625')-H));extraT=np.sqrt(D('6.25')-4*(D('.5625')+H))
lam=np.array([-np.sqrt((D('2.5')+coreT)/2),-np.sqrt((D('2.5')-coreT)/2),np.sqrt((D('2.5')-coreT)/2),np.sqrt((D('2.5')+coreT)/2),-np.sqrt((D('2.5')+extraT)/2),-np.sqrt((D('2.5')-extraT)/2),np.sqrt((D('2.5')-extraT)/2),np.sqrt((D('2.5')+extraT)/2)])
logw=np.log(w);lam2=lam*lam;lam3=lam2*lam

def T(logw):
 w=np.exp(logw-np.max(logw));w/=w.sum();m=w@lam;m2=w@lam2;m3=w@lam3
 a=(m*m2-m3)/(m2-m*m);b=-m2-a*m;q=lam2+a*lam+b
 logw=logw+2*np.log(abs(q));return logw-np.max(logw)
state=0;cross=[];hist=[];start=time.time()
for k in range(2000001):
 logw=T(T(logw))
 if k%100==0:
  w=np.exp(logw-np.max(logw));w/=w.sum();m=w@lam
  side=-1 if m<D('-1.25') else (1 if m>D('-.75') else 0)
  if side and side!=state:
   cross.append((k,float(m),float(logw.min())));state=side;print('CROSS',cross[-1],flush=True)
  if k%10000==0:hist.append([k,m,*logw]);
 if k%100000==0:
  print('iter',k,'crosses',len(cross),'time',time.time()-start,flush=True)
  np.savez('workspace/logorbit_agent2.npz',hist=np.array(hist),cross=np.array(cross),logw=logw,lam=lam,w0=f['start'][24])
from pathlib import Path
Path('workspace/logorbit_agent2.py').write_text(Path(__file__).read_text())
