import sys,numpy as np,itertools,pickle,time
from scipy.optimize import brentq
sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
act=g.active;V=act[:,None]**np.arange(4);cv=g.cv;C=32.;mi=np.sqrt(5-2*np.sqrt(2));mo=np.sqrt(5+2*np.sqrt(2));mus=np.array([-mo,-mi,mi,mo]);Vm=mus[:,None]**np.arange(4)
records=[];candidates=[];start=time.time()
for bits in itertools.product([0,1],repeat=4):
 g.setup(bits,mi);pc=g.Pp.copy();qc=g.Qp.copy();P=pc(act);Q=qc(act);Pm=pc(mus);Qm=qc(mus)
 def data(t):
  w=C*(act-t)*cv/P;z=w*P*P/C;M=V.T@(w[:,None]*V);Mz=V.T@(z[:,None]*V);ac=-np.linalg.solve(M,C*Mz);Frow=(w*P**3)@V
  z1=((w*P**3)[:,None]*V+2*(w*P)[:,None]*(V@ac)-z[:,None]*Frow)/C;bc=-np.linalg.solve(Mz,V.T@(Q[:,None]*z1));beta=-(Qm[:,None]*(Vm@ac)+Pm[:,None]*(Vm@bc)+Frow)/C;force=4/C*np.linalg.solve(Mz,Vm.T*Pm)
  Az=-pc(t)/g.D6(t);Brow=-2*((z*P/(act-t))@V)/Az;bf=Brow@force
  return force,beta,bf
 for i,j in [(0,2),(0,3),(1,2),(1,3)]:
  def calc(t):
   F,beta,bf=data(t);r=-bf[i]/bf[j];ff=F[:,i]+r*F[:,j];comp=(beta[i]-beta[j])@ff;sc=max(1,np.linalg.norm(beta[i]-beta[j])*np.linalg.norm(ff));kap=beta[i]@ff
   return comp/sc,r,kap
  ts=np.linspace(-.995,.995,101);vals=[calc(t) for t in ts];roots=[]
  if max(abs(a[0]) for a in vals)<1e-9:roots=list(ts)
  else:
   for k in range(len(ts)-1):
    if vals[k][0]*vals[k+1][0]<0:
     roots.append(brentq(lambda t:calc(t)[0],ts[k],ts[k+1],xtol=1e-12))
  for t in roots:
   comp,r,kap=calc(t);rec=(bits,i,j,t,comp,r,kap);records.append(rec)
   if r>0 and kap>1e-5:candidates.append(rec);print('POSITIVE',rec,flush=True)
print('COMPLETE',len(records),'positive',len(candidates),'maxkap',max((r[-1] for r in records if r[-2]>0),default=None),'time',time.time()-start)
pickle.dump(records,open('workspace/agent3_mixed_flip_rayscan.pkl','wb'))
