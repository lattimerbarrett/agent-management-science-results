import numpy as np
from numpy.polynomial.polynomial import polymul,polydiv,polyval
act=np.array([-3,-np.sqrt(5),-1,1,np.sqrt(5),3.]);Dcoef=np.array([-45.,0,59,0,-15,0,1]);V=act[:,None]**np.arange(4)
def trans(t,delta):
 C=64-delta**2;pc=np.array([17-delta,0,-10.,0,1]);qc=pc.copy();qc[0]+=2*delta;P=polyval(act,pc);Q=polyval(act,qc);w0=np.where(abs(abs(act)-np.sqrt(5))<1e-10,(8-delta)/32,(8+delta)/64);w=w0*(1-t/act);M=V.T@(w[:,None]*V);z=w*P*P/C;Mz=V.T@(z[:,None]*V);cols=[]
 for hc in np.eye(4):
  u=w*P*(V@hc);a=-np.linalg.solve(M,V.T@(u*P));av=V@a;F=sum(u*P*P);z1=(u*P*P+2*w*P*av-z*F)/C;b=-np.linalg.solve(Mz,V.T@(z1*Q));bv=V@b;F1=sum(z1*Q*Q);o1=(z1*Q*Q+2*z*Q*bv-w*F1)/C;dr=o1-u;dw=-w0/act;v=(dr@dw)/(dw@dw);rr=polymul(qc,a)+polymul(pc,b);rr[0]-=F;num=polymul([-t,1],rr);num[0]+=C*v/2;K,rem=polydiv(num,Dcoef);cols.append(np.r_[K[:3],F])
 return np.array(cols).T
for delta in [5.7,6.,7.,4*np.sqrt(2)]:
 for t in [-.7,.23,.6]:
  C=64-delta*delta;P=t**4-10*t*t+17-delta;L=2*delta*(8-delta)
  guess=np.array([[0,L*(t**4-5*t*t-delta-8)/P,-L*t,5*L*(t**4-5*t*t-delta-8)/P],[0,0,L,-L*t],[0,L*(5-t*t)/P,0,L*(t**4-15*t*t+42-delta)/P],[-2*delta*C,2*delta*C*t,-10*delta*C,10*delta*C*t]])
  assert np.linalg.norm(trans(t,delta)-guess)<1e-8
print('General-delta physical transformation checked against direct moment variations at 12 parameter points.')
