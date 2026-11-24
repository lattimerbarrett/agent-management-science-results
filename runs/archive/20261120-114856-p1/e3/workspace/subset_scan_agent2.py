import numpy as np,itertools,time
rng=np.random.default_rng(736)
D=np.load('workspace/below_candidate_agent4.npz');lam=D['lam'];pars=D['pars'];H=pars[2];base=D['logs0'];l2=lam*lam;l3=l2*lam
subs=list(itertools.combinations(range(4),2))+list(itertools.combinations(range(4),3));Nper=400
logs=[];labels=[]
for ss in subs:
 for j in range(Nper):
  lw=base.copy();lw[:4]+=rng.normal(0,rng.choice([.0001,.001,.01,.1,.5]),4);lw[4:]+=rng.uniform(-15,15,4)
  for i in range(4):
   if i not in ss:lw[i+4]=-np.inf
  logs.append(lw);labels.append(ss)
logs=np.array(logs);startlogs=logs.copy();N=len(logs)
ml,mr=1-lam[2],1-lam[1];side=np.zeros(N,int);count=np.zeros(N,int);alive=np.ones(N,bool)
def T(logs):
 w=np.exp(logs-logs.max(axis=1)[:,None]);w/=w.sum(axis=1)[:,None];m=w@lam;m2=w@l2;m3=w@l3;a=(m*m2-m3)/(m2-m*m);b=-m2-a*m;q=l2+a[:,None]*lam+b[:,None];hh=np.sum(w*q*q,axis=1)
 logs=logs+2*np.log(abs(q));logs-=logs.max(axis=1)[:,None]
 return logs,m,hh
start=time.time();best=0
for k in range(50001):
 logs,m,hh=T(logs);logs,_,_=T(logs)
 if k%10==0:
  alive&=hh<H*(1+1e-7)
  ss=np.where(m<ml+.1*(mr-ml),-1,np.where(m>ml+.9*(mr-ml),1,0));hit=alive&(ss!=0)&(ss!=side);count+=hit;side=np.where(hit,ss,side)
  if count.max()>best:
   best=count.max();ix=np.argmax(count);print('NEW',k,best,'id',ix,'subset',labels[ix],'ratio',hh[ix]/H,flush=True)
   np.savez('workspace/subset_best_agent2.npz',logw0=startlogs[ix],lam=lam,pars=pars,subset=labels[ix],count=best,iteration=k)
 if k%5000==0:print('iter',k,'alive',alive.sum(),'max',best,'time',time.time()-start,flush=True)
 if not alive.any():break
np.savez('workspace/subset_scan_agent2.npz',logs0=startlogs,lam=lam,pars=pars,logs=logs,count=count,alive=alive,labels=np.array([sum(1<<j for j in x)for x in labels]))
from pathlib import Path
Path('workspace/subset_scan_agent2.py').write_text(Path(__file__).read_text())
