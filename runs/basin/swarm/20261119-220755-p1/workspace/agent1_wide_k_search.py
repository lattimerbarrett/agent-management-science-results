import numpy as np,itertools
from scipy.optimize import brentq
from scipy.integrate import quad_vec
from pathlib import Path
rng=np.random.default_rng(8391);best=(-1,None);bad=[];count=0
for trial in range(1500):
 gaps=10**rng.uniform(-1.5,1.5,4);S=np.r_[0,np.cumsum(gaps)];S=(S-S.mean())/(S[-1]-S[0]);a,b=S[2:4];c=rng.uniform(S[0]+1e-5*(S[2]-S[0]),S[2]-.001*(S[2]-S[0]));roots=np.sort(np.r_[S,c]);
 def P(x):return np.prod(x-roots)
 crit=[]
 for l,r in zip(roots[::2],roots[1::2]):
  dd=(r-l)*1e-10;crit.append(brentq(lambda x:np.sum(1/(x-roots)),l+dd,r-dd,xtol=1e-15))
 lim=min(-P(x)for x in crit);N=lim*10**rng.uniform(-9,-.32)
 def getroots(L):
  oo=[]
  for l,m,r in zip(roots[::2],crit,roots[1::2]):
   oo.extend([brentq(lambda x:P(x)+L,l,m,xtol=5e-16),brentq(lambda x:P(x)+L,m,r,xtol=5e-16)])
  return np.array(oo)
 rt=getroots(N);mus=getroots(2*N)
 # identify nearest realnegativelevels lefta andrightb
 mu=max(x for x in mus if x<a);nu=min(x for x in mus if x>b)
 ds=np.array([np.prod(S[i]-np.delete(S,i))for i in range(5)])
 for bits in itertools.product([0,1],repeat=3):
  fi=np.array([2*j+bits[j]for j in range(3)]);gr=rt[np.setdiff1d(np.arange(6),fi)];fr=rt[fi];fv=np.prod(S[:,None]-fr,axis=1);p=N*(S-(a+b)/2)/(ds*fv)
  if min(p)<0:continue
  f2=-sum(fr);g2=-sum(gr)
  def R(x):return np.prod(x-gr)/np.prod(x-fr)
  Ra,Rb=R(a),R(b)
  if min(Ra,Rb)<=0:continue
  def integr(t):
   q=np.sqrt(R(t));return np.array([(q+1/q)/2,((2*t+f2)*q+(2*t+g2)/q)/2])
  J=quad_vec(integr,a,b,epsabs=1e-10,epsrel=2e-10)[0];J0,J1=J
  def force(z,e,RR):
   ff=np.prod(z-fr)**2;return np.array([N+ff,(N+ff)*(z+e)+N*f2+ff*g2,(N+RR*ff)/((z-e)*np.sqrt(RR))])
  F0=force(mu,a,Ra);F1=force(nu,b,Rb);F1[:2]+=J*F1[2]
  L0=np.array([mu,1,np.sqrt(N)/(mu-a)]);L1=np.array([nu,1,np.sqrt(N)/(nu-b)-nu*J0-J1]);C=np.array([[L0@F0,L0@F1],[L1@F0,L1@F1]])
  count+=1;k=C[0,1]*C[1,0]/np.prod(np.diag(C))
  if C[0,1]<0 and C[1,0]<0:
   if k>best[0]:best=(k,(S,c,N,bits,mu,nu,C,J))
   if k>1.0001:
    bad.append((k,trial,S,c,N,bits,mu,nu,C,J));print('BAD',bad[-1],flush=True)
 if trial%100==0:print('trial',trial,'count',count,'best',best[0],'bad',len(bad),flush=True)
np.savez('workspace/agent1_wide_k_search.npz',best=np.array(best,dtype=object),bad=np.array(bad,dtype=object),count=count);print('FINAL',count,'best',best,'bad',len(bad))
