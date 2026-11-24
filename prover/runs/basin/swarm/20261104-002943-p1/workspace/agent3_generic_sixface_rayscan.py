import numpy as np,itertools,pickle,time
from scipy.optimize import brentq
from numpy.polynomial import Polynomial as Poly
H=1.;delta=1/np.sqrt(2);C=.5
rootslev=lambda d: np.sort(np.r_[np.sqrt((5+np.array([-1,1])*np.sqrt(9+4*d))/2),-np.sqrt((5+np.array([-1,1])*np.sqrt(9+4*d))/2)])
allact=np.sort(np.r_[rootslev(1),rootslev(-1)]);qroots=np.sort(np.r_[rootslev(delta),rootslev(-delta)]);pairs=qroots.reshape(4,2);mus=np.array([-2.,-1.,1.,2.]);Vm=mus[:,None]**np.arange(4)
records=[];posit=[];start=time.time();cases=0
for bits in itertools.product([0,1],repeat=4):
 pc=Poly.fromroots(pairs[np.arange(4),bits]);qc=Poly.fromroots(pairs[np.arange(4),1-np.array(bits)]);Pm=pc(mus);Qm=qc(mus)
 for free in range(3):
  other=[k for k in range(3) if k!=free]
  for ends in itertools.product([0,1],repeat=2):
   dels=[2*k+1+e for k,e in zip(other,ends)];act=np.delete(allact,dels);D=Poly.fromroots(act);V=act[:,None]**np.arange(4);cv=1/D.deriv()(act);P=pc(act);Q=qc(act);lo,hi=allact[2*free+1:2*free+3]
   def data(t):
    w=C*(act-t)*cv/P;z=w*P*P/C;M=V.T@(w[:,None]*V);Mz=V.T@(z[:,None]*V);ac=-np.linalg.solve(M,C*Mz);Frow=(w*P**3)@V;bc=C*np.eye(4)
    beta=-(Qm[:,None]*(Vm@ac)+Pm[:,None]*(Vm@bc)+Frow)/C;force=4/C*np.linalg.solve(Mz,Vm.T*Pm);Az=-pc(t)/D(t);Brow=-2*((z*P/(act-t))@V)/Az;bf=Brow@force
    return force,beta,bf,min(w)
   if data((lo+hi)/2)[-1]<1e-10:continue
   for i,j in itertools.combinations(range(4),2):
    if not (mus[i]<lo and mus[j]>hi):continue
    cases+=1
    def calc(t):
     F,beta,bf,_=data(t);r=-bf[i]/bf[j];ff=F[:,i]+r*F[:,j];comp=(beta[i]-beta[j])@ff;sc=max(1,np.linalg.norm(beta[i]-beta[j])*np.linalg.norm(ff));kap=beta[i]@ff
     return comp/sc,r,kap
    ts=np.linspace(lo+.001*(hi-lo),hi-.001*(hi-lo),61);vals=[calc(t) for t in ts];rr=[]
    if max(abs(v[0]) for v in vals)<1e-9:rr=list(ts)
    else:
     for k in range(len(ts)-1):
      if vals[k][0]*vals[k+1][0]<0:rr.append(brentq(lambda t:calc(t)[0],ts[k],ts[k+1],xtol=1e-12))
    for t in rr:
     comp,r,kap=calc(t);rec=(bits,free,tuple(dels),i,j,t,comp,r,kap);records.append(rec)
     if r>0 and kap>1e-7:posit.append(rec);print('POSITIVE',rec,flush=True)
print('DONE cases',cases,'roots',len(records),'posit',len(posit),'maxkap',max((r[-1] for r in records if r[-2]>0),default=None),'seconds',time.time()-start)
pickle.dump({'allact':allact,'mus':mus,'records':records,'positive':posit},open('workspace/agent3_generic_sixface_rayscan.pkl','wb'))
