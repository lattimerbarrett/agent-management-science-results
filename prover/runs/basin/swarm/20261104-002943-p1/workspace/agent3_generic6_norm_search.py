import sys,numpy as np,itertools,pickle,time
from scipy.integrate import solve_ivp
from scipy.special import expit
from numpy.polynomial import Polynomial as Poly
sys.path.insert(0,'workspace');import agent1_flip_augode as m
rootslev=lambda d: np.sort(np.r_[np.sqrt((5+np.array([-1,1])*np.sqrt(9+4*d))/2),-np.sqrt((5+np.array([-1,1])*np.sqrt(9+4*d))/2)])
full=np.sort(np.r_[rootslev(1),rootslev(-1)]);delta=1/np.sqrt(2);qroots=np.sort(np.r_[rootslev(delta),rootslev(-delta)]);pairs=qroots.reshape(4,2);C=.5;mus=[-2.,-1.,1.,2.];rng=np.random.default_rng(999);start=time.time();records=[];best=None
for j in range(1600):
 bits=list(itertools.product([0,1],repeat=4))[j%16];ends=list(itertools.product([0,1],repeat=2))[(j//16)%4];mpair=[(-2,1),(-2,2),(-1,1),(-1,2)][(j//64)%4]
 pc=Poly.fromroots(pairs[np.arange(4),bits]);qc=Poly.fromroots(pairs[np.arange(4),1-np.array(bits)]);act=np.delete(full,[1+ends[0],5+ends[1]]);D=Poly.fromroots(act);cv=1/D.deriv()(act);x=np.r_[act,mpair];V=x[:,None]**np.arange(4);p=pc(x);q=qc(x);wref=np.r_[C*act*cv/p[:6],0,0];m.x=x;m.V=V;m.p=p;m.q=q;m.C=C;m.w0=wref
 def coords(hc):
  h=V@hc;u=wref*p*h;M=V.T@(wref[:,None]*V);ac=-np.linalg.solve(M,V.T@(u*p));aa=V@ac;F=sum(u*p*p);z=wref*p*p/C;z1=(u*p*p+2*wref*p*aa-z*F)/C;bc=C*hc;bb=V@bc;FF=sum(z1*q*q);f1=(z1*q*q+2*z*q*bb-wref*FF)/C;b=f1-u;dwt=np.r_[-wref[:6]/act,0,0];v=dwt@b/(dwt@dwt);R=qc*Poly(ac)+pc*Poly(bc)-F;K=(R*Poly([0,1])+C*v/2)//D
  return np.r_[np.pad(K.coef,(0,3-len(K.coef))),-F/C]
 L=np.column_stack([coords(np.eye(4)[k]) for k in range(4)]);S=V[:6].T@((wref[:6]*p[:6]**2)[:,None]*V[:6]);rad=full[4]
 def statew(u):
  th=np.tanh(u);t=rad*th;w=wref.copy();w[:6]*=1-t/act;w[2]=2*wref[2]*expit(2*u);w[3]=2*wref[3]*expit(-2*u);return th,w
 def rhs(t,z):
  th,w=statew(z[0]);out=m.ode(t,np.r_[w,z[1:]]);hc=z[1:5];h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);aa=-V@np.linalg.solve(M,V.T@(u*p));F=sum(u*p*p);zz=w*p*p/C;z1=(u*p*p+2*w*p*aa-zz*F)/C;bb=C*h;F1=sum(z1*q*q);R=2*aa/p+2*bb/q-(F+F1)/C;ud=-R[3]/(1+th) if z[0]>=0 else R[2]/(1-th);out=np.r_[ud,out[8:]];r=hc@S@out[1:5]+z[5:]@out[5:];out[1:]-=r*z[1:];return out
 def evF(t,z):
  _,w=statew(z[0]);return -(w*p**3)@(V@z[1:5])/C
 evF.terminal=True;evF.direction=-1
 def evU(t,z):return 50-abs(z[0])
 evU.terminal=True;evU.direction=-1
 X=np.array([1.,rng.uniform(-3,3),10**rng.uniform(-1,1),10**rng.uniform(-1,1.5)]);A=10**rng.uniform(-3,.5,size=2);hc=np.linalg.solve(L,X);nn=np.sqrt(hc@S@hc+A@A);z0=np.r_[0.,hc/nn,A/nn]
 try:
  sol=solve_ivp(rhs,(0,200),z0,rtol=5e-7,atol=2e-9,max_step=.2,events=[evF,evU]);tt=np.tanh(sol.y[0]);cross=int(np.sum((tt[:-1]*tt[1:]<0)&(sol.t[1:]>1e-4)));rec=(cross,sol.t[-1],j,bits,ends,mpair,X,A);records.append((rec,z0,sol.t,sol.y))
  if best is None or rec[0]>best[0][0]:best=records[-1];print('BEST',rec,'elapsed',time.time()-start,flush=True)
 except Exception as e:print('FAIL',j,str(e),flush=True)
 if time.time()-start>115:break
pickle.dump(records,open('workspace/agent3_generic6_norm_search.pkl','wb'));print('DONE',len(records),'best',best[0])
