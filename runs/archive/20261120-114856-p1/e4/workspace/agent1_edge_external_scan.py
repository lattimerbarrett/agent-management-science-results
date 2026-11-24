import numpy as np,itertools,json,time
from pathlib import Path
from scipy.optimize import brentq
rng=np.random.default_rng(1177);valid=0;positive=0;found=[];start=time.time()
def rroots(p):
 rr=np.roots(p)
 return np.sort(rr.real) if max(abs(rr.imag))<1e-6 else None
def vertex(xx,q,mid):
 inds=[0,*mid,7];z=xx[inds];cc=np.array([1/np.prod(z[j]-np.delete(z,j)) for j in range(5)]);W=np.zeros(8);ww=cc/q[inds];W[inds]=ww/sum(ww);return W
for it in range(5000):
 cen=np.sort(rng.uniform(-1,1,4))
 if min(np.diff(cen))<.12:continue
 sep=rng.uniform(.05,.4,4)*min(np.diff(cen));sg=rng.choice([-1,1],4)
 qa=cen-sg*sep;ra=cen+sg*sep;qp=np.poly(qa);rp=np.poly(ra);F=np.polymul(qp,rp)
 cr=rroots(np.polyder(F))
 if cr is None:continue
 cv=np.polyval(F,cr);pos=cv[cv>0];neg=-cv[cv<0]
 if len(pos)!=3 or len(neg)!=4:continue
 H=min(min(pos),np.sort(neg)[-3])*rng.uniform(.02,.8)
 PP=F.copy();PP[-1]-=H;xx=rroots(PP)
 if xx is None:continue
 NN=F.copy();NN[-1]+=H;rr=np.roots(NN);bb=np.sort(rr.real[abs(rr.imag)<1e-6])
 if len(bb)<6:continue
 bands=[next(j for j in range(4) if xx[2*j]<z<xx[2*j+1]) for z in bb]
 q=np.polyval(qp,xx)/np.sqrt(H);r=np.polyval(rp,xx)/np.sqrt(H);f=np.array([xx**j for j in range(4)]).T
 qb=np.polyval(qp,bb)/np.sqrt(H);rb=np.polyval(rp,bb)/np.sqrt(H);fb=np.array([bb**j for j in range(4)]).T
 valid+=1
 for empty,mid0,mid1 in [(1,[1,4,5],[1,4,6]),(2,[1,3,6],[2,3,6])]:
  occ=[j for j in range(4) if j!=empty];groups=[[k for k,band in enumerate(bands) if band==j] for j in occ]
  if any(not g for g in groups):continue
  W0=vertex(xx,q,mid0);W1=vertex(xx,q,mid1);dw=W1-W0;idx=np.argmax(abs(dw));ghost=[2*empty,2*empty+1]
  def calc(u,J):
   W=W0+u*dw;G=f.T@(W[:,None]*f);Gp=f.T@((W*q*q)[:,None]*f)
   R=-np.linalg.solve(Gp,G);dh=(W[:,None]*(r-q)[:,None]*f).sum(axis=0)
   EJ=r[:,None]*f+q[:,None]*(f@R)-dh
   ar=2*W[idx]/dw[idx]*EJ[idx]
   L=rb[list(J),None]*fb[list(J)]+qb[list(J),None]*(fb[list(J)]@R)+dh
   C=4*np.linalg.solve(G,(qb[list(J),None]*fb[list(J)]).T)
   eta=np.linalg.solve(L@C,np.ones(3));v=C@eta;E=EJ@v
   return ar@v,eta,-dh@v,E
  for J in itertools.product(*groups):
   samples=[]
   for u in np.linspace(.01,.99,11):
    try:res=calc(u,J)
    except np.linalg.LinAlgError:res=None
    samples.append((u,res))
   for (u,a),(v,b) in zip(samples,samples[1:]):
    if a is None or b is None or a[0]*b[0]>=0:continue
    try:root=brentq(lambda t:calc(t,J)[0],u,v,xtol=1e-10);value,eta,alpha,E=calc(root,J)
    except Exception:continue
    if min(eta)>1e-8:
     positive+=1
     data=dict(qroots=qa.tolist(),rroots=ra.tolist(),H=float(H),core=xx.tolist(),negative=bb.tolist(),J=list(J),empty=empty,u=float(root),eta=eta.tolist(),alpha=float(alpha),E=E.tolist(),ghost_p=(-2*E[ghost]).tolist())
     print('POSITIVE',json.dumps(data),flush=True)
     if alpha>0 and max(E[ghost])<0:found.append(data)
 if found:break
 if valid%100==0:print('valid',valid,'positive',positive,'seconds',time.time()-start,flush=True)
