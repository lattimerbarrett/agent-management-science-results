import numpy as np
from scipy.integrate import solve_ivp

def data(delta):
 C=64-delta*delta
 def AA(t):
  P0=t**4-10*t*t+17;R=P0*P0-delta*delta;K=np.array([1,t,t*t,0.]);a0=8*t*(t*t+5)/C+20*t*P0/R;a1=8*(t*t-5)/C;a2=-4*t*(4/C+P0/R)
  return np.vstack([a0*K-[0,1,t,0],a1*K-[0,0,1,0],a2*K,-P0*K])
 sol=solve_ivp(lambda t,z:(AA(t)@z.reshape(4,4)).ravel(),(-1,1),np.eye(4).ravel(),rtol=2e-12,atol=1e-13,max_step=.02,dense_output=True)
 U=sol.y[:,-1].reshape(4,4);Ui=np.linalg.inv(U);gam=np.sqrt(2*delta*delta-64);mus=[]
 for sg in [-1,1]:
  for st in [-1,1]:
   mu=np.sqrt(5+st*np.sqrt(8+sg*gam));mus.extend([-mu,mu])
 mus=np.sort(mus)
 def burst(t,mu):
  D=(t*t-1)*(t*t-5)*(t*t-9);Pm=mu**4-10*mu*mu+17-delta;P0=t**4-10*t*t+17;R=P0*P0-delta*delta;Dm=(mu*mu-1)*(mu*mu-5)*(mu*mu-9)
  J=8*delta*(mu+t)*(mu*mu+t*t-10)*Pm/R;B1=8*delta*(mu*mu-5)*Pm/C;B2=-8*delta*(mu+t)*Pm*((mu*mu-5)*D-C)/(C*R);B0=J-t*B1-t*t*B2;bf=-8*delta*Pm;b=np.array([B0,B1,B2,bf]);beta=np.r_[-Dm*np.array([1,mu,mu*mu])/(C*(mu-t)),-2/C]
  S=np.eye(4)-2*np.outer(b,beta)/(beta@b)
  return S,b,beta
 return C,U,Ui,mus,burst,sol
found=[]
for delta in [5.7,6,7,7.5,7.8,7.9,7.99]:
 C,U,Ui,mus,burst,sol=data(delta)
 for ml in mus[:4]:
  SL,bL,beL=burst(-1,ml)
  for mr in mus[4:]:
   SR,bR,beR=burst(1,mr);M=SL@Ui@SR@U;evals,evec=np.linalg.eig(M)
   for j,ev in enumerate(evals):
    if abs(ev.imag)>1e-7 or not (.000001<ev.real<.99999):continue
    X=evec[:,j].real;X*=-np.sign(X[3]);X/=abs(X[3]);XR=U@X;XRout=SR@XR;XLin=Ui@XRout
    checks=[-(np.array([1,-1,1,0])@X),np.array([1,1,1,0])@XRout,beR@XR,beL@XLin]
    if min(checks)>1e-7:
     print('FOUND delta',delta,'mus',ml,mr,'rho',ev.real,'X',X,'CHECKS',checks,'Fstates',[X[3],XR[3],XRout[3],XLin[3],(SL@XLin)[3]],flush=True)
     found.append((delta,ml,mr,ev.real,X,checks))
np.savez('workspace/agent1_scattering_scan.npz',found=np.array(found,dtype=object))