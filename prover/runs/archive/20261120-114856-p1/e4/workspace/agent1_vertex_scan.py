import numpy as np,itertools,json,time
from pathlib import Path
rng=np.random.default_rng(913)
choices=list(itertools.product([1,2],[3,4],[5,6]))
def realroots(p):
 rr=np.roots(p)
 if max(abs(rr.imag))>1e-6:return None
 return np.sort(rr.real)
found=[];valid=0;pos_eta=0;start=time.time()
for it in range(2000):
 cen=np.sort(rng.uniform(-1,1,4))
 if min(np.diff(cen))<.15:continue
 sep=rng.uniform(.05,.3,4)*min(np.diff(cen))
 sig=rng.choice([-1,1],4)
 qa=cen-sig*sep;ra=cen+sig*sep
 qp=np.poly(qa);rp=np.poly(ra);F=np.polymul(qp,rp)
 cr=realroots(np.polyder(F))
 if cr is None:continue
 cv=np.polyval(F,cr);pos=cv[cv>0];neg=-cv[cv<0]
 if len(pos)!=3 or len(neg)!=4:continue
 H=min(min(pos),np.sort(neg)[-3])*rng.uniform(.05,.8)
 PP=F.copy();PP[-1]-=H;xx=realroots(PP)
 if xx is None:continue
 NP=F.copy();NP[-1]+=H;rr=np.roots(NP);betas=np.sort(rr.real[abs(rr.imag)<1e-6])
 if len(betas)<6:continue
 bands=np.array([next(j for j in range(4) if xx[2*j]<z<xx[2*j+1]) for z in betas])
 Jlist=[J for J in itertools.combinations(range(len(betas)),3) if len(set(bands[list(J)]))==3]
 scale=np.sqrt(H);q=np.polyval(qp,xx)/scale;r=np.polyval(rp,xx)/scale
 qb=np.polyval(qp,betas)/scale;rb=np.polyval(rp,betas)/scale
 f=np.array([xx**j for j in range(4)]).T;fb=np.array([betas**j for j in range(4)]).T
 valid+=1
 for bits,mid in enumerate(choices):
  inds=[0,*mid,7];z=xx[inds]
  cc=np.array([1/np.prod(z[j]-np.delete(z,j)) for j in range(5)])
  weights=cc/q[inds];weights/=sum(weights)
  if min(weights)<=0:raise Exception('notpositive')
  W=np.zeros(8);W[inds]=weights
  G=f.T@(W[:,None]*f);Gp=f.T@((W*q*q)[:,None]*f)
  try:RR=-np.linalg.solve(Gp,G); dh=(W[:,None]*(r-q)[:,None]*f).sum(axis=0);L=rb[:,None]*fb+qb[:,None]*(fb@RR)+dh;C=4*np.linalg.solve(G,(qb[:,None]*fb).T);A=L@C
  except np.linalg.LinAlgError:continue
  for J in Jlist:
   try:eta=np.linalg.solve(A[np.ix_(J,J)],np.ones(3))
   except np.linalg.LinAlgError:continue
   if min(eta)>1e-9:
    pos_eta+=1
    v=C[:,J]@eta;alpha=-dh@v
    if alpha<=0:continue
    dr=RR@v;E=r*(f@v)+q*(f@dr)-dh@v;rates=2*E
    data=dict(it=it,qa=qa.tolist(),ra=ra.tolist(),H=float(H),xx=xx.tolist(),betas=betas.tolist(),J=list(J),vertex=inds,eta=eta.tolist(),alpha=float(alpha),rates=rates.tolist())
    found.append(data);print('FOUND',json.dumps(data),flush=True)
 if found:break
 if valid%100==0:print('valid',valid,'elapsed',time.time()-start,flush=True)
