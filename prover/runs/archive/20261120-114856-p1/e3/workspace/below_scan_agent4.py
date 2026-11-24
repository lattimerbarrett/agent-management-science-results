import numpy as np,time
rng=np.random.default_rng(392);starts=[];ls=[];Hs=[];ends=[];pars=[]
for j in range(12000):
 if j%2:a,L=np.sort(rng.uniform(.02,.98,2))
 else:a=rng.uniform(.02,.98);L=1+10**rng.uniform(-1.5,1.5)
 v=a+L;d=a*L;Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,crit);H=10**rng.uniform(-4,-.001)*min(-lev[0],lev[1],-lev[2])
 if H<1e-10:continue
 pc=Q.copy();pc[-1]=-H;core=np.sort(np.roots(pc));pe=Q.copy();pe[-1]=H;ex=np.sort(np.roots(pe));left=1-core[2];right=1-core[1];m=rng.uniform(left,right);eps=10**rng.uniform(-4,-.3);r=H*eps;z=rng.uniform(-5,5)*r;h=(r+(v-1)*z)/d;ew=H*eps*eps*np.exp(rng.uniform(-12,3,4));lam=np.r_[core,ex]
 moments=np.array([1,m,m+h,m+h+z])-np.array([sum(ew*ex**k)for k in range(4)]);cw=np.linalg.solve(np.vstack([core**k for k in range(4)]),moments);w=np.r_[cw,ew]
 if min(w)<=1e-250:continue
 logs=np.log(w);starts.append(logs);ls.append(lam);Hs.append(H);ends.append((left,right));pars.append((a,L,H))
ls=np.array(ls);alllogs=np.array(starts);Hs=np.array(Hs);ends=np.array(ends);pars=np.array(pars);ids=np.arange(len(ls));logs=alllogs.copy();lam=ls.copy();counts=np.zeros(len(ids),int);state=np.zeros(len(ids),int);globalcounts=np.zeros(len(ids),int);best=0;t0=time.time();print('N',len(ids),flush=True)
for it in range(100000):
 w=np.exp(logs);m=(w*lam).sum(1);m2=(w*lam**2).sum(1);m3=(w*lam**3).sum(1);aa=(m3-m*m2)/(m2-m*m);bb=m2-aa*m;q=lam**2-aa[:,None]*lam-bb[:,None];hn=(w*q*q).sum(1);logs+=2*np.log(abs(q));logs-=logs.max(1)[:,None];logs-=np.log(np.exp(logs).sum(1))[:,None]
 if it%2==1:
  crossed=hn>Hs[ids]*(1+1e-8);x=((np.exp(logs)*lam).sum(1)-ends[ids,0])/(ends[ids,1]-ends[ids,0]);new=np.where(x<.1,-1,np.where(x>.9,1,0));sw=(new!=0)&(state!=0)&(new!=state)&~crossed;counts+=sw;state=np.where(new!=0,new,state);globalcounts[ids]=counts
  if counts.max(initial=0)>best:
   best=counts.max();ix=np.argmax(counts);print('BEST',best,'iter',it,'id',ids[ix],'pars',pars[ids[ix]],'x',x[ix],'Hratio',hn[ix]/Hs[ids[ix]],flush=True);np.savez('workspace/below_candidate_agent4.npz',logs0=alllogs[ids[ix]],lam=lam[ix],pars=pars[ids[ix]],count=best,logs=logs[ix],it=it)
  if it%200==199:
   good=~crossed;ids=ids[good];logs=logs[good];lam=lam[good];counts=counts[good];state=state[good]
   if not len(ids):break
 if it%10000==9999:print('iter',it,'remaining',len(ids),'best',best,'time',time.time()-t0,flush=True)
np.savez('workspace/below_scan_agent4.npz',ls=ls,starts=alllogs,pars=pars,counts=globalcounts,remaining=ids,lastlogs=logs)
print('DONE',it,len(ids),best,time.time()-t0)
from pathlib import Path
Path('workspace/below_scan_agent4.py').write_text(Path('scratchpad.py').read_text())
