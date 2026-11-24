import numpy as np
from scipy.spatial.transform import Rotation
from scipy.linalg import null_space
from scipy.optimize import root
from scipy.optimize._numdiff import approx_derivative
U=np.sqrt(np.pi/4);Z=(1-np.pi/4)/U;T=np.sqrt(1-U*U-Z*Z);L=1-U*U
r0=2*T*U/np.sqrt(L)
A=Rotation.from_quat([T,0,Z,U]).as_matrix();B=Rotation.from_quat([-T,0,Z,U]).as_matrix()
d=np.array([-Z*r0/T,L*r0/(U*T),0]);x0=(np.array([0,0,r0])+d)/2;y0=(np.array([0,0,r0])-d)/2
Ex=null_space(x0.reshape(1,3));Ey=null_space(y0.reshape(1,3))
co=np.array([0,1.039559368275690,-.2110211053606824/2,4.080124741024757/6,11.19097485006615/24])
def rot(v,axis,ang):
 return v*np.cos(ang)+np.cross(axis,v)*np.sin(ang)+axis*np.dot(axis,v)*(1-np.cos(ang))
bp_power=3
def f(q,k):
 x=x0+Ex@q[:2];x=x/np.linalg.norm(x);y=y0+Ey@q[2:];y=y/np.linalg.norm(y)
 v=x+y;r=np.linalg.norm(v);h=r-r0;z=v[2]
 a=sum(co[i]*h**i for i in range(5));ap=sum(i*co[i]*h**(i-1) for i in range(1,5))
 theta=k*h**bp_power+ap*z
 xx=rot(x,v/r,theta);yy=rot(y,v/r,theta)
 xx=rot(xx,np.array([0,0,1]),a);yy=rot(yy,np.array([0,0,1]),a)
 xx=A.T@xx;yy=B.T@yy
 return np.r_[Ex.T@(xx-x),Ey.T@(yy-y)]
print('base norms',np.linalg.norm(x0),np.linalg.norm(y0),'r',r0,'base residual',f(np.zeros(4),-.2),flush=True)
J=approx_derivative(lambda q:f(q,-.2),np.zeros(4),method='3-point',abs_step=1e-5)
print('J',J,'singular values',np.linalg.svd(J)[1],flush=True)
rng=np.random.default_rng(2)
for k in []:
 for eps in [1e-8,1e-9]:
  target=np.array([.2,.3,-.6,.4]);target=eps*target/np.linalg.norm(target)
  sols=[]
  for i in range(300):
   q=rng.normal(size=4)*.02
   rr=root(lambda q:f(q,k)-target,q,tol=1e-10)
   if np.linalg.norm(f(rr.x,k)-target)<1e-10 and np.linalg.norm(rr.x)<.2 and all(np.linalg.norm(rr.x-v)>1e-5 for v in sols):sols.append(rr.x)
  signs=[]
  for q in sols:
   jj=approx_derivative(lambda q:f(q,k),q,method='3-point',abs_step=1e-5)
   signs.append(int(np.sign(np.linalg.det(jj))))
  print('k,eps',k,eps,'roots',len(sols),'signs',signs,'degree sum',sum(signs),'norms',[np.linalg.norm(q) for q in sols],flush=True)
UU,SS,VVt=np.linalg.svd(J); VV=VVt.T; orient=int(round(np.linalg.det(UU)*np.linalg.det(VV)))
for a2,k,bp_power in [(-.2110211053606824,k,3) for k in [-.2,-1.]]:
 co[2]=a2/2
 J=approx_derivative(lambda q:f(q,k),np.zeros(4),method='3-point',abs_step=1e-5)
 UU,SS,VVt=np.linalg.svd(J); VV=VVt.T; orient=int(round(np.linalg.det(UU)*np.linalg.det(VV)))
 print('case a2,k,power',a2,k,bp_power,'singular vals',SS,flush=True)
 for rho in [.003]:
  gs=[];prev=np.zeros(2)
  for angle in np.linspace(0,2*np.pi,401):
   tt=rho*np.array([np.cos(angle),np.sin(angle)])
   def gg(ss): return UU[:,:2].T@f(VV[:,:2]@ss+VV[:,2:]@tt,k)
   rr=root(gg,prev,tol=1e-10);prev=rr.x
   q=VV[:,:2]@rr.x+VV[:,2:]@tt
   gs.append(UU[:,2:].T@f(q,k))
  gs=np.array(gs);args=np.unwrap(np.arctan2(gs[:,1],gs[:,0]));wind=(args[-1]-args[0])/(2*np.pi)
  print('Reduced degree',k,rho,'winding',wind,'orientation',orient,'index',orient*round(wind),'minnorm',np.min(np.linalg.norm(gs,axis=1)),flush=True)
from pathlib import Path
Path('workspace/agent3_local_degree_numeric.py').write_text(Path('scratchpad.py').read_text())
