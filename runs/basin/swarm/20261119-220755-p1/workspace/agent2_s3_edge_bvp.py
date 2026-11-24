import sys;sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
from scipy.integrate import solve_bvp
from scipy.special import expit,logit
import numpy as np
from pathlib import Path
nodes=np.array([-3.,-1.,1.,2.,3.]);f=np.array([5.,-7.,0.,1.]);g=np.array([-5.,-7.,0.,1.]);mus=np.sort(np.roots([1,0,-7,np.sqrt(14)]).real);mus=mus[mus>0];ob=BlowupODE(nodes,f,g,11,mus);print('mus',mus)
def decode(a):
 y=a.copy();y[0]=-1-expit(np.clip(a[0],-30,30));y[-2:]=np.exp(np.clip(a[-2:],-50,30));return y

def field(a):
 y=decode(a);v=ob(0,y,True);th=-y[0];v[0]=-v[0]/((th-1)*(2-th));v[-2:]/=y[-2:];return v

def bc(a,b):
 aa=decode(a);bb=decode(b)
 return np.r_[aa[0]+1.5,ob(0,aa,True)[0],a[-2:]-np.log(.001),bb[1],bb[3]]
mesh=np.linspace(0,1,101);ys=np.tile(np.r_[0.,np.zeros(3),np.log(.001),np.log(.001)][:,None],(1,len(mesh)))
for T in list(np.arange(.2,2.01,.2))+list(np.arange(2.5,10.01,.5)):
 try:
  sol=solve_bvp(lambda t,a:T*np.column_stack([field(a[:,j]) for j in range(a.shape[1])]),bc,mesh,ys,max_nodes=6000,tol=8e-5)
  yy=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);th=-yy[0];print('T',round(T,2),'status',sol.status,'res',max(sol.rms_residuals),'bc',max(abs(bc(sol.y[:,0],sol.y[:,-1]))),'theta',min(th),max(th),'Zend',yy[-2:,-1],flush=True)
  np.savez('workspace/agent2_s3_edge_bvp_T'+str(round(T,2))+'.npz',t=sol.x*T,a=sol.y,yy=yy)
  if sol.status!=0:break
  mesh=np.linspace(0,1,501);ys=sol.sol(mesh)
 except Exception as e:print('FAILED',T,type(e),e);break
Path('workspace/agent2_s3_edge_bvp.py').write_text(Path('scratchpad.py').read_text())
