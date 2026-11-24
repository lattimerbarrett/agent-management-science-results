import sys;sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
import numpy as np
from scipy.integrate import solve_bvp
from scipy.special import expit,logit
from pathlib import Path
z=np.load('workspace/agent2_positive_eq.npz');ob=BlowupODE(z['base'],z['f'],z['g'],float(z['N']),z['mus']);eq=z['y']
s=np.load('workspace/agent2_radialshoot_T2.npz');B=s['B'];BI=np.linalg.inv(B);eps=float(s['eps'])
def decode(a):
 y=a.copy();y[0]=-expit(np.clip(a[0],-30,30));y[-2:]=np.exp(np.clip(a[-2:],-50,30));return y

def encode(y):
 a=y.copy();a[0]=logit(-y[0]);a[-2:]=np.log(y[-2:]);return a

def field(a):
 y=decode(a);v=ob(0,y,True);th=-y[0];v[0]=-v[0]/(th*(1-th));v[-2:]/=y[-2:];return v

def bc(a,b):
 ca=BI@(decode(a)-eq);cb=BI@(decode(b)-eq);tar=np.r_[eps,0.,0.,0.,0.]
 return np.r_[ca[:5]-tar,cb[5:]]

mesh=np.linspace(0,1,101);ys=np.column_stack([encode(np.array([np.interp(tt,s['t'],s['yy'][j]) for j in range(7)])) for tt in mesh*2])
for T in range(2,17):
 def fun(t,a):return T*np.column_stack([field(a[:,j]) for j in range(a.shape[1])])
 try:
  sol=solve_bvp(fun,bc,mesh,ys,max_nodes=10000,tol=2e-5,verbose=0)
  orig=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);th=-orig[0]
  print('T',T,'status',sol.status,'nodes',len(sol.x),'res',max(sol.rms_residuals),'bc',max(abs(bc(sol.y[:,0],sol.y[:,-1]))),'theta',min(th),max(th),'wend',np.linalg.norm(orig[1:5,-1]),'Zend',orig[-2:,-1],flush=True)
  np.savez('workspace/agent2_radial_bvp_T'+str(T)+'.npz',t=sol.x*T,a=sol.y,yy=orig,eq=eq,B=B,eps=eps)
  if sol.status!=0:break
  mesh=sol.x;ys=sol.y
 except Exception as e:print('FAILED T',T,type(e),e);break
Path('workspace/agent2_radial_bvp.py').write_text(Path('scratchpad.py').read_text())
