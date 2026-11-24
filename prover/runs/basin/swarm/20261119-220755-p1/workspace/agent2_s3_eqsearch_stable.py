import numpy as np,itertools,sys
from scipy.optimize import brentq
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
rng=np.random.default_rng(131)
def dat(ob,th,pair):
 H=ob.nodes-th;p=ob.N*H/(ob.d*ob.fv);pp=H*ob.fv/ob.d;V=ob.V
 M=V.T@(p[:,None]*V);Mp=V.T@(pp[:,None]*V);G=-np.linalg.solve(Mp,V.T@((H*ob.gv/ob.d)[:,None]*V));dn=ob.N**2*np.sum((H/(ob.d*ob.fv**2))[:,None]*V,axis=0);R=(ob.gv[:,None]*V+ob.fv[:,None]*(V@G)-dn)/ob.N;B=2*np.mean(H[:,None]*R,axis=0);Vm=ob.Vmu[pair,:];fm=ob.fm[pair];gm=ob.gm[pair];Lm=2*(Vm/fm[:,None]+Vm@G/gm[:,None])-2*dn/ob.N
 w=np.linalg.solve(np.vstack([B,Lm]),[0,-2,-2]);v=w-np.linalg.solve(M,V.T@(p*ob.fv*(R@w)**2));F=-4*np.linalg.solve(M,Vm.T*fm);normal=np.cross(F[:,0],F[:,1]);normal/=np.linalg.norm(normal);scalar=normal@v;Z=np.linalg.lstsq(F,-v,rcond=None)[0];return scalar,w,Z,dn@w
count=0
for trial in range(500):
 nodes=np.array([-3.,-1.,1.,2.,3.]);P=np.poly(nodes);c=rng.uniform(nodes[0]-1,nodes[-1]+1);L=10**rng.uniform(-3,1)
 fg=np.polymul(P,[1,-c]);fg[-1]+=L;rr=np.roots(fg)
 if max(abs(rr.imag))>1e-7:continue
 rr=np.sort(rr.real);neg=fg.copy();neg[-1]+=L;mm=np.roots(neg)
 if max(abs(mm.imag))>1e-7:continue
 mm=np.sort(mm.real)
 for ix in itertools.combinations(range(6),3):
  f=np.poly(rr[list(ix)])[::-1];g=np.poly(rr[[j for j in range(6) if j not in ix]])[::-1];ob=BlowupODE(nodes,f,g,L,mm)
  for j in range(4):
   a,b=nodes[j:j+2];mid=(a+b)/2
   if min(L*(nodes-mid)/(ob.d*ob.fv))<=0:continue
   for pair in itertools.combinations(range(6),2):
    pair=list(pair);grid=np.linspace(a+.0001*(b-a),b-.0001*(b-a),18)
    try:vv=[dat(ob,x,pair)[0] for x in grid]
    except np.linalg.LinAlgError:continue
    for aa,bb,fa,fb in zip(grid[:-1],grid[1:],vv[:-1],vv[1:]):
     if fa*fb>0:continue
     try:
      th=brentq(lambda x:dat(ob,x,pair)[0],aa,bb,xtol=1e-12);err,w,Z,dn=dat(ob,th,pair)
      if np.linalg.norm(w)>1e7 or abs(err)>1e-5:continue
      count+=1
      if min(Z)>1e-8 and dn<-1e-5 and np.linalg.norm(w)<1e3 and np.linalg.norm(BlowupODE(nodes,f,g,L,mm[pair])(0,np.r_[-th,w,Z]))<1e-5:
       print('PHYSICAL',trial,th,w,Z,dn,'nodes',nodes,'c,L',c,L,'partition',ix,'pair',pair,flush=True);np.savez('workspace/agent2_s3_foundEQ.npz',nodes=nodes,f=f,g=g,N=L,mus=mm[pair],y=np.r_[-th,w,Z]);raise SystemExit
     except (ValueError,np.linalg.LinAlgError):pass
 if trial%20==0:print('trial',trial,'eqcount',count,flush=True)
print('DONE',count)
