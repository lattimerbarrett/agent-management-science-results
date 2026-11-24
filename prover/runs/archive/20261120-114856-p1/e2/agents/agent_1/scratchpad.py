import sys,numpy as np,itertools,time,pickle
from numpy.polynomial.legendre import leggauss
sys.path.insert(0,'workspace')
from agent2_mixed_billiards import Billiard
rng=np.random.default_rng(291);start=time.time();found=[];ncand=0;nodes0,weights0=leggauss(96)
def calc(b):
 L,R=b.left,b.right;mid=(L+R)/2;c=b.mat(mid)[1]*b.q(mid)/np.prod(mid-b.core);t=(R-L)/2*nodes0+(R+L)/2;wq=(R-L)/2*weights0
 WW=(b.d*b.q(b.core))[None,:]*(b.core[None,:]-t[:,None]);Hs=np.einsum('ni,ij,ik->njk',WW,b.X,b.X);ell=np.array([np.ones(len(t)),t,t*t]).T;bb=b.h/(4*b.q(t)[:,None])*np.linalg.solve(Hs,ell[...,None])[...,0]
 zz=np.sqrt(abs(b.q(t)*b.p(L)/(b.p(t)*b.q(L))));u=(wq*zz)@bb;U=np.eye(3)+np.outer(u,c);out={'U':U,'c':c}
 for side,x in [('L',L),('R',R)]:
  _,vr,D,F,E=b.mat(x,False);out.update({side+'growth':D,side+'energy':E,side+'reflect':[np.eye(3)-2*np.outer(F[:,j],D[j])/(D[j]@F[:,j])for j in range(len(b.extra))]})
 return out

def ep(m,side,aa,word,krow,n):
 D=m[side+'growth'];SS=m[side+'reflect'];Z=np.vstack([np.zeros(n),np.eye(n)]);checks=[]
 for j in word:
  g=np.r_[krow@aa,D@aa]
  if g[j+1]<=1e-8:return None
  tau=Z[j+1]/g[j+1];checks.append(tau.copy());Z-=np.outer(g,tau);checks.append(Z[0].copy());checks.extend(Z[k+1].copy()for k in range(n)if k!=j);aa=SS[j]@aa
  if m[side+'energy']@aa<=1e-8:return None
 g=np.r_[krow@aa,D@aa]
 if g[0]<=1e-8:return None
 tau=Z[0]/g[0];checks.append(tau.copy());Z-=np.outer(g,tau);checks.extend(Z[1:].copy());return Z[1:],checks
for it in range(10000):
 core6=np.r_[-1.,np.sort(rng.uniform(-.95,.95,4)),1.]
 if min(np.diff(core6))<.025:continue
 chi=np.poly(core6);crit=np.sort(np.roots(np.polyder(chi)).real);depth=min(-np.polyval(chi,crit[[0,2,4]]));h=depth*rng.uniform(.025,.46);pp=chi.copy();pp[-1]+=h;rt=np.sort(np.roots(pp).real);picks=rng.integers(0,2,3);pc=np.poly(rt[[2*j+picks[j]for j in range(3)]]);qc=np.poly(rt[[2*j+1-picks[j]for j in range(3)]]);drop=1;L,R=core6[3:5];pe=chi.copy();pe[-1]+=2*h;ex=np.sort(np.roots(pe).real);ex=ex[ex>core6[drop]]
 if len(ex)!=4:continue
 b=Billiard(np.delete(core6,drop),ex,pc,qc,h,L,R)
 try:m=calc(b)
 except Exception as error:
  if it<20:print(type(error).__name__,str(error))
  continue
 U=m['U'];UI=np.linalg.inv(U);gap=R-L;mid=(L+R)/2;vrow=b.mat(mid)[1];kl=b.mat(L+1e-5*gap)[1]/(1e-5*gap);kr=-b.mat(R-1e-5*gap)[1]/(1e-5*gap);words=[(j,)for j in range(4)]+list(itertools.permutations(range(4),2))+[w for w in itertools.product(range(4),repeat=3)if w[0]!=w[1]and w[1]!=w[2]];LS=[];RS=[]
 for w in words:
  sl=np.eye(3);sr=np.eye(3)
  for j in w:sl=m['Lreflect'][j]@sl;sr=m['Rreflect'][j]@sr
  LS.append(sl);RS.append(sr)
 for il,ir in itertools.product(range(len(words)),repeat=2):
  C=LS[il]@UI@RS[ir]@U;vs,vc=np.linalg.eig(C)
  for j,rho in enumerate(vs):
   if abs(rho.imag)>1e-5 or rho.real<=0 or rho.real>=.98:continue
   if not any(abs(v.imag)<1e-5 and v.real>1.05 for kk,v in enumerate(vs)if kk!=j):continue
   a=vc[:,j].real;a*=np.sign(m['Lenergy']@a);a/=np.linalg.norm(a);ar=U@a;arb=RS[ir]@ar;al=UI@arb
   if m['Renergy']@ar<=1e-8 or m['Renergy']@arb<=1e-8 or m['Lenergy']@al<=1e-8 or vrow@a<=1e-8 or vrow@UI@arb>=-1e-8:continue
   right=ep(m,'R',ar.copy(),words[ir],kr,4);left=ep(m,'L',al.copy(),words[il],kl,4)
   if right is None or left is None:continue
   ncand+=1;P=left[0]@right[0];lv,lvc=np.linalg.eig(P)
   for jj,ll in enumerate(lv):
    if abs(ll.imag)>1e-4 or ll.real<=1.05:continue
    x=lvc[:,jj].real;x*=np.sign(sum(x));x/=np.linalg.norm(x)
    if min(x)<1e-6 or min(row@x for row in right[1])<=1e-8:continue
    xl=right[0]@x
    if min(row@xl for row in left[1])<=1e-8:continue
    item=dict(core6=core6,h=h,picks=picks,extra=ex,wl=words[il],wr=words[ir],rho=rho.real,a=a,P=P,lam=ll.real,seed=x,pc=pc,qc=qc,L=L,R=R)
    print('FOUND MULTISEED',item,flush=True);found.append(item)
 if it%100==0:print('it',it,'candidates',ncand,'found',len(found),'time',time.time()-start,flush=True)
 if found:break
with open('workspace/agent1_multichannel_found.pkl','wb')as f:pickle.dump(found,f)
print('FINISH',it,ncand,len(found),time.time()-start)
