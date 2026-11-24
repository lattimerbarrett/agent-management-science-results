import numpy as np,time
from scipy.optimize import brentq
rng=np.random.default_rng(124681)
B=4096;n=8
spectra=[];initial=[]
for z in range(B):
 gaps=np.exp(rng.uniform(-1.5,1.5,5));core=np.r_[0,np.cumsum(gaps)];core-=core.mean();core/=np.ptp(core)
 co=np.poly(core);extrema=np.sort(np.roots(np.polyder(co)).real);depths=-np.polyval(co,extrema[[0,2,4]])
 h=depths.min()*np.exp(rng.uniform(np.log(.01),np.log(.48)))
 rr=[];ee=[]
 for j in range(3):
  a,b=core[2*j:2*j+2];m=extrema[2*j]
  rr.extend([brentq(lambda x:np.prod(x-core)+h,a,m,xtol=1e-15),brentq(lambda x:np.prod(x-core)+h,m,b,xtol=1e-15)])
  ee.extend([brentq(lambda x:np.prod(x-core)+2*h,a,m,xtol=1e-15),brentq(lambda x:np.prod(x-core)+2*h,m,b,xtol=1e-15)])
 picks=rng.integers(0,2,3);qroots=np.array(rr)[2*np.arange(3)+picks]
 qval=np.prod(core[:,None]-qroots,axis=1)
 c=np.array([1/np.prod(core[i]-np.delete(core,i)) for i in range(6)])
 missing=rng.integers(1,5)
 theta=[rng.uniform(core[1],core[2]),rng.uniform(core[3],core[4])]
 theta[0 if missing in [1,2] else 1]=core[missing]
 w=c*qval*(core-theta[0])*(core-theta[1]);w=np.delete(w,missing);assert min(w)>0
 nex=3
 ex=rng.choice(6,nex,replace=False);sp=np.r_[np.delete(core,missing),np.array(ee)[ex]]
 eps=np.exp(rng.uniform(-8,-3))
 w=np.r_[w*np.exp(rng.uniform(-eps,eps,5)),eps**2*np.exp(rng.uniform(-15,-3,nex))];w/=sum(w)
 ix=np.argsort(sp);spectra.append(sp[ix]);initial.append(np.log(w[ix]))
x=np.array(spectra);lw=np.array(initial);x-=x.mean(axis=1)[:,None];x/=np.ptp(x,axis=1)[:,None]
prev=np.exp(lw);records=[];t0=time.time()
for k in range(1,100001):
 w=np.exp(lw);p0=np.zeros_like(w);p=np.ones_like(w);beta=np.zeros(B)
 for j in range(3):
  norm=np.sum(w*p*p,axis=1);alpha=np.sum(w*x*p*p,axis=1)/norm
  q=(x-alpha[:,None])*p-beta[:,None]*p0
  beta=np.sum(w*q*q,axis=1)/norm;p0,p=p,q
 z=lw+2*np.log(np.maximum(np.abs(p),1e-280));lw=z-np.logaddexp.reduce(z,axis=1)[:,None]
 if k in [1000,10000,30000,100000]:
  wt=np.exp(lw);score=np.linalg.norm(wt-prev,axis=1);prev=wt.copy();records.append(score)
  ix=np.argsort(score)[-8:][::-1]
  print('window',k,'moving',sum(score>.001),'top',[(int(i),float(score[i])) for i in ix],'time',time.time()-t0,flush=True)
ix=np.argsort(records[-1])[-128:][::-1]
np.savez('edge8_candidates.npz',x=x[ix],initial=np.array(initial)[ix],lw=lw[ix],score=np.array(records)[:,ix],indices=ix)
for i in ix[:6]:print('candidate',i,'x',x[i],'w0',np.exp(initial[i]),'wlast',np.exp(lw[i]),flush=True)
