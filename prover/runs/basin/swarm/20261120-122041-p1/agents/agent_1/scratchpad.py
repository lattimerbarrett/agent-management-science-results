import numpy as np,pickle
rng=np.random.default_rng(924)
lam=np.array([-4.,-3,-2,-1,1,2,3,4]);P=np.poly(lam);cr=np.sort(np.roots(np.polyder(P)))
hmax=min(-np.polyval(P,t) for t in cr if np.polyval(np.polyder(P,2),t)>0)
V=np.array([lam**i for i in range(4)]).T;f=lam**4
c=np.array([1/np.prod(np.delete(lam[i]-lam,i)) for i in range(8)])
print('hmax',hmax,flush=True)
cands=[]
for seed in range(200):
 h=hmax*rng.uniform(.02,.98);Ph=P.copy();Ph[-1]+=h;roots=np.sort(np.roots(Ph)).real
 qcoef=np.poly(roots[::2]);qpcoef=np.poly(roots[1::2]);dcoef=qpcoef-qcoef;dlead=dcoef[1]
 q=np.polyval(qcoef,lam);qp=np.polyval(qpcoef,lam);dd=np.polyval(dcoef,lam)
 wc=c*qp*dd/dlead
 if min(wc)<0:print('badwc',wc);continue
 eps=10**rng.uniform(-5,-2);w=wc*(1+eps*rng.normal(size=8));w/=sum(w);wi=w.copy();hist=[]
 for k in range(50000):
  pp=np.linalg.solve(V.T@(w[:,None]*V),V.T@(w*f));qv=f-V@pp;hh=w@(qv*qv);w=w*qv*qv/hh
  if k%20==0:hist.append(np.r_[w,hh])
 hist=np.array(hist);path=hist[:,:8];travel=np.sum(np.linalg.norm(np.diff(path,axis=0),axis=1));enddist=np.linalg.norm(path[-1]-path[0]);spread=np.max(np.ptp(path[-400:],axis=0))
 if travel>1 or (travel>.1 and enddist<.1):
  print('CAND',seed,'travel',travel,'enddist',enddist,'spread',spread,flush=True);cands.append((seed,lam,wi,hist,h,wc))
 pickle.dump(cands,open('umbilic8.pkl','wb'))
print('num',len(cands))
