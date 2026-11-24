import numpy as np,itertools,json,time
from scipy.integrate import quad
rng=np.random.default_rng(918)
def data(a,L,theta):
 v=a+L;d=a*L;coef=np.array([1,-(1+v),d+v,-d,0.])
 crit=np.roots(np.polyder(coef));crit=np.sort(crit.real[abs(crit.imag)<1e-9]);middle=[x for x in crit if a<x<1]
 if not middle:return
 H=theta*np.polyval(coef,middle[0]);pc=coef.copy();pc[-1]-=H;core=np.roots(pc);pn=coef.copy();pn[-1]+=H;extra=np.roots(pn)
 if max(abs(core.imag))>1e-8 or max(abs(extra.imag))>1e-8:return
 core=np.sort(core.real);extra=np.sort(extra.real);ml,mr=1-core[2],1-core[1]
 def integr(m):
  D=d+m*m+(v-2)*m-v+1;R=m*(m-1)*D;T=d+2*m*m+(v-3)*m-v+1
  return T/(2*np.sqrt(R))
 J=quad(integr,ml,mr,epsabs=1e-8,epsrel=1e-8)[0]/np.sqrt(H)
 F=np.array([[1,J],[0,1.]]);Fi=np.array([[1,-J],[0,1.]])
 def refl(e):
  out=[]
  for x in extra:
   k=d*(x-1)/((v-1)*x-d);R=np.eye(2)+2*np.outer([1,k-e],[x-e,-1])/(k-x)
   out.append(R)
  return out
 return v,d,H,core,extra,J,F,Fi,refl(core[2]),refl(core[1])
def words(R,nmax=3):
 out=[]
 for n in range(1,nmax+1):
  for w in itertools.product(range(4),repeat=n):
   if any(w[j]==w[j+1]for j in range(n-1)):continue
   M=np.eye(2)
   for j in w:M=R[j]@M
   out.append((w,M))
 return out
def adwords(R,e,extra,sgn,nmax=6):
 out=[]
 def intersect(lo,hi,A,B):
  if abs(B)<1e-20:return (lo,hi) if A>0 else (1,0)
  if B>0:lo=max(lo,-A/B)
  else:hi=min(hi,-A/B)
  return lo,hi
 def rec(word,M,lo,hi):
  for j in range(4):
   if word and word[-1]==j:continue
   ell=np.array([-1,1/(extra[j]-e)])@M
   l,r=intersect(lo,hi,-ell[0],ell[1])
   if l>=r:continue
   MM=R[j]@M
   l,r=intersect(l,r,MM[0,0],-MM[0,1])
   if l>=r:continue
   # completed word ends with outward core velocity
   ll,rr=intersect(l,r,sgn*MM[1,0],-sgn*MM[1,1])
   if ll<rr:out.append((word+(j,),MM))
   # continuation keeps core velocity inward
   if l<r and len(word)+1<nmax:rec(word+(j,),MM,l,r)
 rec((),np.eye(2),0 if sgn>0 else -np.inf,np.inf if sgn>0 else 0)
 return out
def valid(word,X,R,e,extra,incomingsign):
 X=X.copy()
 for jj,j in enumerate(word):
  fit=-X[0]+X[1]/(extra[j]-e)
  if fit<=1e-9:return False
  old=X.copy();X=R[j]@X
  if not(old[0]<X[0]<-1e-9):return False
 return X[1]*incomingsign<0
start=time.time()
for tr in range(4000):
 a=1-np.exp(rng.uniform(np.log(1e-5),np.log(.2)));L=1+np.exp(rng.uniform(np.log(.01),np.log(20)));theta=np.exp(rng.uniform(np.log(1e-3),np.log(.99)))
 D=data(a,L,theta)
 if D is None:continue
 v,d,H,core,extra,J,F,Fi,RL0,RR0=D
 fracL=rng.uniform(.999,1);fracR=rng.uniform(.999,1)
 RL=[np.eye(2)+fracL*(R-np.eye(2)) for R in RL0];RR=[np.eye(2)+fracR*(R-np.eye(2)) for R in RR0]
 WL=adwords(RL,core[2],extra,1,1);WR=adwords(RR,core[1],extra,-1,1)
 for wl,ML in WL:
  for wr,MR in WR:
   M=ML@Fi@MR@F; ev,vec=np.linalg.eig(M)
   for j,rho in enumerate(ev):
    if abs(rho.imag)>1e-7 or not(.0001<rho.real<.9999):continue
    X=vec[:,j].real;X=-X/abs(X[0]) if X[0]>0 else X/abs(X[0])
    if X[1]>=0:continue
    XR=F@X
    if not(XR[0]<0 and valid(wr,XR,RR,core[1],extra,-1)):continue
    XL=Fi@MR@XR
    if not(XL[0]<0 and valid(wl,XL,RL,core[2],extra,1)):continue
    print('FOUND',tr,'aLtheta',a,L,theta,'H',H,'words',wl,wr,'fractions',fracL,fracR,'rho',rho,'X',X,'J',J,flush=True)
    np.savez('workspace/billiard_found_agent2.npz',a=a,L=L,H=H,core=core,extra=extra,J=J,wl=wl,wr=wr,rho=rho,X=X,M=M,fracL=fracL,fracR=fracR)
    raise SystemExit
 if tr%200==0:print('trial',tr,'wordcounts',len(WL),len(WR),'time',time.time()-start,flush=True)
print('none',time.time()-start)
from pathlib import Path
Path('workspace/billiard_words_agent2.py').write_text(Path(__file__).read_text())
