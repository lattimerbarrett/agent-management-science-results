import numpy as np,sys
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline
from agent2_blowup_ode import BlowupODE

def decode(a):
 y=a.copy();y[0]=-1/(1+np.exp(-a[0]));y[-2:]=np.exp(a[-2:]);return y

def continuation(oldname,params,prefix,amp=.6,tol=2e-5):
 z=np.load('workspace/agent2_rational_positive_eq_0.4.npz');old=np.load(oldname);S=z['base'];eq=old['eq'];D=old['D'];B=old['B'];C=np.linalg.inv(B);mu0=z['mus'];mesh=np.linspace(0,1,401);aa=CubicSpline(old['x'],old['a'],axis=1)(mesh);pp=old['p'];out=[]
 for v,q1,q2,L in params:
  P=np.poly1d(np.poly(S))*np.poly1d(np.poly([q1,q2]));rt=np.sort(np.roots(P+L));f=np.poly(rt[[0,3,5,6]])[::-1];g=np.poly(rt[[1,2,4,7]])[::-1];rr=np.roots(P+2*L);mus=np.array([rr[np.argmin(abs(rr-vv))]for vv in mu0]);
  if max(abs(np.r_[f,g,mus].imag))>1e-7:print('complex',v,flush=True);break
  ob=BlowupODE(S,f.real,g.real,L,mus.real);V=ob.V;Vm=ob.Vmu
  def fun(t,a,par):
   Y=decode(a);th=-Y[0];W=Y[1:5].T;Z=Y[-2:].T;H=S[None,:]-th[:,None];wv=W@V.T;p=L*H/(ob.d*ob.fv);pa=H*ob.fv/ob.d;M=np.einsum('ni,nj,bn->bij',V,V,p);Mp=np.einsum('ni,nj,bn->bij',V,V,pa);dg=np.linalg.solve(Mp,(-((H*wv/ob.d)*ob.gv)@V)[...,None])[...,0];dn=L**2*np.sum(H*wv/(ob.d*ob.fv**2),axis=1);ratio=(ob.gv*wv+ob.fv*(dg@V.T)-dn[:,None])/L
   wf=-np.linalg.solve(M,((p*ob.fv*ratio**2)@V+4*(Z*ob.fm)@Vm)[...,None])[...,0];ix=np.where(th.real<.5,2,3);rat=ratio[np.arange(len(th)),ix];xd=np.where(th.real<.5,2*rat/(1-th),-2*rat/th);grow=2+2*((W@Vm.T)/ob.fm+(dg@Vm.T)/ob.gm)-2*dn[:,None]/L;dw=W+wf-par[1]*((Y-eq[:,None]).T@D.T)[:,1:5];return par[0]*np.vstack([xd,dw.T,grow.T])
  def bc(a,b,par):cc=C@(decode(a)-eq);return np.r_[a-b,cc[1],cc[0]-amp]
  def jac(t,a,par):
   h=1e-20;ja=np.empty((7,7,a.shape[1]));jp=np.empty((7,2,a.shape[1]))
   for j in range(7):
    ac=a.astype(complex);ac[j]+=h*1j;ja[:,j,:]=fun(t,ac,par).imag/h
   for j in range(2):
    pc=par.astype(complex);pc[j]+=h*1j;jp[:,j,:]=fun(t,a,pc).imag/h
   return ja,jp
  try:sol=solve_bvp(fun,bc,mesh,aa,p=pp,tol=tol,max_nodes=15000,fun_jac=jac)
  except Exception as e:print('ERR',v,e,flush=True);break
  Y=decode(sol.y);print('v',v,'status',sol.status,'Tκ',sol.p,'θ',-Y[0].max(),-Y[0].min(),'Z',Y[-2:].min(),'err',max(sol.rms_residuals),flush=True)
  if sol.status:break
  name=prefix+str(round(v,5))+'.npz';np.savez(name,x=sol.x,a=sol.y,y=Y,p=sol.p,D=D,B=B,eq=eq,f=f.real,g=g.real,L=L,mus=mus.real,q1=q1,q2=q2);out.append((v,sol.p[1],name))
  mesh=np.linspace(0,1,max(401,min(1001,len(sol.x))));aa=sol.sol(mesh);pp=sol.p
 return out
