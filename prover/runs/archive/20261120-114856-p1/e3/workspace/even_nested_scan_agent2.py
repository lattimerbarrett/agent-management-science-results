import numpy as np,itertools,time,pickle
from pathlib import Path
rng=np.random.default_rng(787)
def scan(V,H,N=30000,Bp=80):
 U=1.;dif=np.sqrt((V-U)**2+4*H);co=np.sqrt([(U+V+dif)/2,(U+V-dif)/2]);lam=np.sort(np.r_[-co,co]);di=np.sqrt((V-U)**2-4*H);ex=np.sort(np.r_[-np.sqrt([(U+V+di)/2,(U+V-di)/2]),np.sqrt([(U+V+di)/2,(U+V-di)/2])]);subs=[i for num in (2,3,4)for i in itertools.combinations(range(4),num)]
 A=np.array([np.ones(4),lam,lam**2,lam**3]);inv=np.linalg.inv(A);w0=inv@np.array([1,0,U,0]);w1=inv@np.array([0,1,0,U]);lo=max(-w0[w1>0]/w1[w1>0]);hi=min(-w0[w1<0]/w1[w1<0]);LL=[];logs=[];labels=[]
 for sub in subs:
  eig=np.r_[lam,ex[list(sub)]];l=np.r_[eig,np.zeros(8-len(eig))]
  for trial in range(Bp):
   for tr in range(100):
    m=rng.uniform(lo*.999,hi*.999);h=10**rng.uniform(-7,-.3);z=h*rng.normal(0,4);extra=h*h*10**rng.uniform(-5,2,len(sub));mom=np.array([1-extra.sum(),m,U+h,U*m+z])-np.array([np.sum(extra*ex[list(sub)]**j)for j in range(4)])+np.array([extra.sum(),0,0,0]);cw=inv@mom
    if min(cw)>0:break
   else:continue
   ww=np.r_[cw,extra,np.zeros(8-len(eig))];ww/=ww.sum();logs.append(np.log(ww,where=ww>0,out=np.full(8,-np.inf)));LL.append(l);labels.append(sub)
 LL=np.array(LL);lw=np.array(logs);start=lw.copy();B=len(lw);cnt=np.zeros(B,int);side=np.zeros(B,int);best=[];r=hi-lo;t0=time.time()
 for k in range(N):
  for parity in range(2):
   w=np.exp(lw);m=np.sum(w*LL,axis=1);m2=np.sum(w*LL**2,axis=1);m3=np.sum(w*LL**3,axis=1);qa=(m*m2-m3)/(m2-m*m);qb=-m2-qa*m;q=LL**2+qa[:,None]*LL+qb[:,None];lw+=2*np.log(np.abs(q));M=np.max(lw,axis=1);lw-=M[:,None]+np.log(np.sum(np.exp(lw-M[:,None]),axis=1))[:,None]
  if k%5==0:
   w=np.exp(lw);m=np.sum(w*LL,axis=1);ss=np.where(m<lo+.2*r,-1,np.where(m>hi-.2*r,1,0));cnt+=(ss!=0)&(ss!=side);side=np.where(ss!=0,ss,side)
 print('SCAN',V,H,'max',cnt.max(),'counts',[(n,int(sum(cnt>=n)))for n in (3,5,10,20)],'sec',time.time()-t0,flush=True)
 ix=np.argsort(cnt)[-10:];return [(int(cnt[i]),V,H,labels[i],LL[i],start[i],lw[i],lo,hi)for i in ix]
res=[]
for V in [1.2,2.,4.,10.,100.]:
 for frac in [.001,.1,.5,.9,.999]:
  H=frac*min(V,(V-1)**2/4)
  res+=scan(V,H,15000,24)
  pickle.dump(res,open('workspace/even_nested_scan_agent2.pkl','wb'))
Path('workspace/even_nested_scan_agent2.py').write_text(Path(__file__).read_text())
