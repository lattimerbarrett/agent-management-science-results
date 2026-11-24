import numpy as np
from scipy.integrate import quad_vec
from agent2_mixed_billiards import Billiard

def transport(b):
 mid=(b.left+b.right)/2;chi=lambda t:np.prod(t-b.core);c=b.mat(mid,False)[1]*b.q(mid)/chi(mid)
 def fun(t):
  w=b.d*b.q(b.core)*(b.core-t);H=(b.X.T*w)@b.X;z=np.sqrt(b.q(t)*b.p(b.left)/(b.p(t)*b.q(b.left)))
  return b.h/(4*b.q(t))*np.linalg.solve(H,[1,t,t*t])*z
 u,e=quad_vec(fun,b.left,b.right,epsabs=1e-9,epsrel=2e-10);U=np.eye(3)+np.outer(u,c)
 return U

def vertex(core,pc,qc,h,j,k,xi):
 x=core;X=np.vander(x,3,increasing=True);p=np.polyval(pc,x);q=np.polyval(qc,x);d=1/np.prod(np.where(np.eye(6,dtype=bool),1,x[:,None]-x[None,:]),axis=1);w=d*q*(x-x[j])*(x-x[k]);H=(X.T*w)@X;Hp=(X.T*(w*p*p/h))@X;M=np.linalg.solve(Hp,H);L=(w*(p-q))@X;Rc=q[:,None]*X-(p[:,None]*X)@M+L;pe=np.polyval(pc,xi);qe=np.polyval(qc,xi);Xe=np.array([1,xi,xi*xi]);Re=qe*Xe-pe*Xe@M+L;De=(4*L-2*Re)/h;F=4*pe*np.linalg.solve(H,Xe);S=np.eye(3)-2*np.outer(F,De)/(De@F)
 return {'g':np.vstack([2*Rc/h,De]),'S':S,'L':L}

def switch(a,v,ent,ext):
 r=v['g'][[ent,ext,6]]@a
 if r[0]>=0 or r[1]<=0:return None
 K=np.array([[0.,0],[1,0],[0,1]]);wait=K[1]/r[1];K-=np.outer(r,wait);return K[[0,2]],np.array([wait,K[0].copy(),K[2].copy()])

def pulse(a,v,ent,missing):
 r=v['g'][[ent,missing,6]]@a
 if r[0]>=0 or r[2]<=0 or v['L']@a<=0:return None
 K=np.array([[0.,0],[1,0],[0,1]]);wait=K[2]/r[2];K-=np.outer(r,wait);Hs=[wait,K[0].copy(),K[1].copy()];a=v['S']@a;r=v['g'][[ent,missing,6]]@a
 if r[0]<=0 or v['L']@a<=0:return None
 wait=K[0]/r[0];K-=np.outer(r,wait);Hs.extend([wait,K[1].copy(),K[2].copy()]);return K[[1,2]],np.array(Hs)

def check(core,pc,qc,h,xi):
 # negative Lagrange coefficients determine two allowed facets
 d=1/np.prod(np.where(np.eye(6,dtype=bool),1,core[:,None]-core[None,:]),axis=1);Ls=np.prod(xi-core)*d/(xi-core);neg=[i for i in [1,2,3,4] if Ls[i]<0]
 if len(neg)!=2:return None
 j,k=sorted(neg);jo=3-j;ko=7-k
 b1=Billiard(np.delete(core,j),[xi],pc,qc,h,core[ko],core[k]);b2=Billiard(np.delete(core,k),[xi],pc,qc,h,core[j],core[jo]);U1=transport(b1);U2=transport(b2);U=U2@U1
 A=vertex(core,pc,qc,h,j,ko,xi);B=vertex(core,pc,qc,h,j,k,xi);C=vertex(core,pc,qc,h,jo,k,xi);Ui=np.linalg.inv(U);V=A['S']@Ui@C['S']@U;ev,ve=np.linalg.eig(V)
 for ind,rho in enumerate(ev):
  if abs(rho.imag)>1e-7 or not(1e-6<rho.real<.999999):continue
  a=ve[:,ind].real;a*=np.sign(A['L']@a);a/=A['L']@a;aB=U1@a;aC=U2@aB;ac=C['S']@aC;ab=np.linalg.solve(U2,ac);aa=np.linalg.solve(U1,ab)
  if min(B['L']@aB,C['L']@aC,C['L']@ac,B['L']@ab,A['L']@aa)<=0:continue
  vs1=b1.mat((b1.left+b1.right)/2,False)[1];vs2=b2.mat((b2.left+b2.right)/2,False)[1]
  if min((b1.right-b1.left)*(vs1@a),(b2.right-b2.left)*(vs2@aB),-(b2.right-b2.left)*(vs2@ab),-(b1.right-b1.left)*(vs1@aa))<=0:continue
  bs1=switch(aB,B,k,j);cs=pulse(aC,C,jo,k);bs2=switch(ab,B,j,k);aas=pulse(aa,A,ko,j)
  if any(z is None for z in [bs1,cs,bs2,aas]):continue
  S=np.eye(2);Hs=[]
  for T,H in [bs1,cs,bs2,aas]:Hs.extend(H@S);S=T@S
  ee,zz=np.linalg.eig(S)
  for ii,Lam in enumerate(ee):
   if abs(Lam.imag)>1e-7 or Lam.real<=1.00001:continue
   z=zz[:,ii].real;z*=np.sign(z[0]);z/=sum(z)
   if min(z)<=0:continue
   margin=min(np.array(Hs)@z)
   if margin>1e-8:return dict(a=a,rho=rho.real,Seed=S,Lambda=Lam.real,z=z,margin=margin,U1=U1,U2=U2,j=j,k=k)
 return None
