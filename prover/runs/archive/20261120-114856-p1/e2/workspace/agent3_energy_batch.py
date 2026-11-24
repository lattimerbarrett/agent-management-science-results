import numpy as np,sys
sys.path.insert(0,'workspace')
from agent2_edge_ode import CORE,EXTRA,h,d,Lc,Le,DCORE,p,q
Z=np.vstack([np.ones(5),Lc.T*p(CORE)]);Zi=np.linalg.pinv(Z)[:,1:];pc=p(CORE);qc=q(CORE);wt=-DCORE*qc

def fun(Y):
 th=np.clip(Y[:,0],1+1e-7,2-1e-7);a1=np.clip(Y[:,1],-1e3,1e3);a2=np.clip(Y[:,2],-1e3,1e3)
 A=np.column_stack([1/(2*d)-(2-th)*a1-(7-2*th)*a2,a1,a2]);M=np.exp(np.clip(Y[:,3:5],-700,10));w=DCORE*qc*(CORE-th[:,None]);H=np.einsum('ij,ni,ik->njk',Lc,w,Lc);HA=np.einsum('nij,nj->ni',H,A);dw=(-HA)@Zi.T;wp=w*pc**2/h;ap=A@Lc.T;dwp=(dw*pc**2+2*w*pc*ap+wp)/h
 H1=np.einsum('ij,ni,ik->njk',Lc,wp,Lc);b=-np.linalg.solve(H1,((dwp*qc)@Lc)[:,:,None])[:,:,0];Rc=qc*ap+pc*(b@Lc.T)+1;Re=q(EXTRA)*(A@Le.T)+p(EXTRA)*(b@Le.T)+1;V=np.sum(wt*(2*w*Rc/h),axis=1)/(wt@wt)
 QQ=-np.linalg.solve(H,(((w*Rc**2*pc)@Lc)/h**2+4*(M*p(EXTRA))@Le)[:,:,None])[:,:,0];LL=2*d*np.column_stack([np.ones(len(Y)),2-th,7-2*th]);LP=np.array([0.,-2*d,-4*d]);D=-(np.sum(LL*QQ,axis=1)+(A@LP)*V);Ad=QQ+D[:,None]*A
 return np.column_stack([V,Ad[:,1:],(4-2*Re)/h+2*D[:,None],-D])
def integrate(initial,T=40,dt=.005):
 states=initial.copy();alive=np.ones(len(states),bool);color=np.zeros(len(states),int);time=np.zeros(len(states))
 for k in range(round(T/dt)):
  ids=np.where(alive)[0]
  if len(ids)==0:break
  yy=states[ids];k1=fun(yy);k2=fun(yy+dt*k1/2);k3=fun(yy+dt*k2/2);k4=fun(yy+dt*k3);new=yy+dt*(k1+2*k2+2*k3+k4)/6;states[ids]=new
  bad=(new[:,0]<1.000001)|(new[:,0]>1.999999)|(np.max(np.abs(new[:,1:3]),axis=1)>100)|(np.max(new[:,3:5],axis=1)>10)|(~np.all(np.isfinite(new),axis=1));bids=ids[bad]
  alive[bids]=False;time[bids]=dt*(k+1);nb=new[bad];color[bids]=np.where(nb[:,0]<1.000001,1,np.where(nb[:,0]>1.999999,2,np.where(nb[:,1]>0,3,4)))
 return states,alive,color,time
