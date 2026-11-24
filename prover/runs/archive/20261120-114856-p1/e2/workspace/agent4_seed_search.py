import numpy as np
from scipy.integrate import quad_vec
from agent2_mixed_billiards import Billiard

def matrices(b):
 mid=(b.left+b.right)/2;chi=lambda t:np.prod(t-b.core);c=b.mat(mid,False)[1]*b.q(mid)/chi(mid)
 def fun(t):
  w=b.d*b.q(b.core)*(b.core-t);H=(b.X.T*w)@b.X
  z=np.sqrt(b.q(t)*b.p(b.left)/(b.p(t)*b.q(b.left)))
  return b.h/(4*b.q(t))*np.linalg.solve(H,[1,t,t*t])*z
 u,err=quad_vec(fun,b.left,b.right,epsabs=2e-9,epsrel=2e-10);U=np.eye(3)+np.outer(u,c)
 if not np.isfinite(U).all() or abs(np.linalg.det(U)-abs(b.p(b.left)/b.p(b.right)))>1e-5*max(1,abs(np.linalg.det(U))):return None
 out={'U':U,'c':c}
 for side,t in [('L',b.left),('R',b.right)]:
  _,_,D,F,E=b.mat(t,False);S=[np.eye(3)-2*np.outer(F[:,j],D[j])/(D[j]@F[:,j]) for j in range(2)]
  ix=np.argmin(abs(b.core-t));K=c/(b.d[ix]*b.q(t));out[side]=(D,F,E,S,K)
 return out

def seed(A,word,side):
 Ds,F,E,Ss,kap=side;K=np.array([[0.,0],[1,0],[0,1]]);Hs=[];mn=1e100
 if kap@A>=0 or E@A<=0:return None
 for j in word:
  r=np.r_[kap@A,Ds@A]
  if r[j+1]<=0:return None
  wait=K[j+1]/r[j+1];Hs.append(wait);K-=np.outer(r,wait)
  Hs.extend(K[k].copy() for k in range(3) if k!=j+1)
  A=Ss[j]@A
  if E@A<=0:return None
 r=np.r_[kap@A,Ds@A]
 if r[0]<=0:return None
 wait=K[0]/r[0];Hs.append(wait);K-=np.outer(r,wait);Hs.extend([K[1].copy(),K[2].copy()])
 return K[1:].copy(),np.array(Hs),A

def check(b,maxlen=3):
 d=matrices(b)
 if d is None:return None
 U=d['U'];Ui=np.linalg.inv(U);words=[tuple((f+j)%2 for j in range(n)) for n in range(1,maxlen+1) for f in [0,1]]
 P={}
 for side in ['L','R']:
  P[side]=[]
  for word in words:
   S=np.eye(3)
   for j in word:S=d[side][3][j]@S
   P[side].append(S)
 for i,wl in enumerate(words):
  for j,wr in enumerate(words):
   C=P['L'][i]@Ui@P['R'][j]@U;ev,ve=np.linalg.eig(C)
   for k,rho in enumerate(ev):
    if abs(rho.imag)>1e-8 or not(1e-5<rho.real<.99999):continue
    A=ve[:,k].real;A*=np.sign(d['L'][2]@A);A/=d['L'][2]@A;Ar=U@A
    if d['R'][2]@Ar<=0:continue
    sr=seed(Ar,wr,d['R'])
    if sr is None:continue
    S,HR,Aro=sr;Al=Ui@Aro
    if d['L'][2]@Al<=0:continue
    sl=seed(Al,wl,d['L'])
    if sl is None:continue
    T,HL,Af=sl;Se=T@S;vv,vz=np.linalg.eig(Se)
    for zzz,lam in enumerate(vv):
     if abs(lam.imag)>1e-8 or lam.real<=1.0001:continue
     z=vz[:,zzz].real;z*=np.sign(z[0]);z/=sum(z)
     if min(z)<=0:continue
     vals=np.r_[HR@z,HL@S@z]
     if min(vals)<=1e-9:continue
     # Confirm V signs via scalar conormal; E endpoints already all positive
     vm=b.mat((b.left+b.right)/2,False)[1]
     if vm@A<=0 or vm@Ui@Aro>=0:continue
     return dict(U=U,WL=wl,WR=wr,a=A,rho=rho.real,Seed=Se,Lambda=lam.real,z=z,margin=min(vals))
 return None
