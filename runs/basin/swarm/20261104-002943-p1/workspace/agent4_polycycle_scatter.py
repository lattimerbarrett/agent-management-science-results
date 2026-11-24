import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path

def data(t,delta,mu):
 C=64-delta*delta;tt=t*t;P0=tt*tt-10*tt+17;R=P0*P0-delta*delta;D=(tt-1)*(tt-5)*(tt-9);ev=np.array([1,t,tt,0]);l=2*D/C*ev
 A=np.array([(8*t*(tt+5)/C+20*t*P0/R)*ev-np.array([0,1,t,0]),8*(tt-5)/C*ev-np.array([0,0,1,0]),-4*t*(4/C+P0/R)*ev,-P0*ev]);pm=(mu*mu-5)**2-8-delta;Dm=(mu*mu-1)*(mu*mu-5)*(mu*mu-9);J=8*delta*(mu+t)*(mu*mu+tt-10)*pm/R;B1=8*delta*(mu*mu-5)*pm/C;B2=-8*delta*(mu+t)*pm*((mu*mu-5)*D-C)/(C*R);B0=J-t*B1-tt*B2;b=np.array([B0,B1,B2,-8*delta*pm]);beta=np.r_[-(Dm*mu**np.arange(3)-D*np.array([1,t,tt]))/(C*(mu-t)),-2/C];return A,b,beta

for delta in [7.,7.9]:
 C=64-delta*delta;nu0=np.sqrt(2*delta*delta-64);mu=np.sqrt(5+np.sqrt(8-nu0));ml=-mu;mr=mu
 U=solve_ivp(lambda t,y:(data(t,delta,ml)[0]@y.reshape(4,4)).ravel(),[-1,1],np.eye(4).ravel(),rtol=1e-13,atol=1e-15,dense_output=True).y[:,-1].reshape(4,4);UI=np.linalg.inv(U)
 _,bl,bel=data(-1,delta,ml);_,br,ber=data(1,delta,mr);SL=np.eye(4)-2*np.outer(bl,bel)/(bel@bl);SR=np.eye(4)-2*np.outer(br,ber)/(ber@br);M=SL@UI@SR@U;ee,V=np.linalg.eig(M);ii=[i for i,e in enumerate(ee) if abs(e.imag)<1e-7 and 0<e.real<.99][0];rho=ee[ii].real;X1=V[:,ii].real;X1*=-np.sign(X1[3]);X2=U@X1;X3=SR@X2;X4=UI@X3
 def kl(x):return x[0]-x[1]+x[2]
 def kr(x):return x[0]+x[1]+x[2]
 def beta(t,mu,X):return data(t,delta,mu)[2]@X
 rates=[(-beta(-1,ml,X1),-128*kl(X1)/C,beta(-1,mr,X1)),(128*(-kr(X2))/C,beta(1,mr,X2),beta(1,ml,X2)),(-beta(1,mr,X3),128*kr(X3)/C,beta(1,ml,X3)),(128*kl(X4)/C,beta(-1,ml,X4),beta(-1,mr,X4))]
 L=[]
 for j,(c,e,tr) in enumerate(rates):
  if j in [0,2]:L.append(np.array([[-tr/e,1],[c/e,0]]))
  else:L.append(np.array([[c/e,0],[-tr/e,1]]))
 B=L[3]@L[2]@L[1]@L[0];ee2,V2=np.linalg.eig(B);print('DELTA',delta,'rho',rho,'rates',rates,'B',B,'EIG',ee2,flush=True)
 for j,vv in enumerate(ee2):
  eig=V2[:,j].real;eig*=np.sign(eig[0]);chain=[eig.copy()]
  for mat in L:chain.append(mat@chain[-1])
  print('eig',vv,'chain',chain,'rho_nu',rho*vv)
 np.savez('workspace/agent4_polycycle_'+str(delta)+'.npz',delta=delta,C=C,mu=mu,U=U,SL=SL,SR=SR,M=M,rho=rho,Xs=np.array([X1,X2,X3,X4]),rates=np.array(rates),B=B,logs_mats=L)
