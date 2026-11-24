import numpy as np
from scipy.spatial.transform import Rotation
from scipy.linalg import null_space
from scipy.optimize._numdiff import approx_derivative
U=np.sqrt(np.pi/4);Z=(1-np.pi/4)/U;T=np.sqrt(1-U*U-Z*Z);L=1-U*U
r0=2*T*U/np.sqrt(L);theta0=np.pi/2
AA=Rotation.from_quat([T,0,Z,U]).as_matrix();BB=Rotation.from_quat([-T,0,Z,U]).as_matrix()
d=np.array([-Z*r0/T,L*r0/(U*T),0]);x0=(np.array([0,0,r0])+d)/2;y0=(np.array([0,0,r0])-d)/2
Ex=null_space(x0.reshape(1,3));Ey=null_space(y0.reshape(1,3))
def rot(v,axis,ang):return v*np.cos(ang)+np.cross(axis,v)*np.sin(ang)+axis*np.dot(axis,v)*(1-np.cos(ang))
b=theta0/(2*r0*r0)
def residual(q,c):
 a=-(b+3*c)*r0*r0
 x=x0+Ex@q[:2];x=x/np.linalg.norm(x);y=y0+Ey@q[2:];y=y/np.linalg.norm(y)
 v=x+y;r=np.linalg.norm(v);z=v[2]
 beta=a+b*r*r+3*c*z*z;theta=2*b*r*z
 xx=rot(x,v/r,theta);yy=rot(y,v/r,theta)
 xx=rot(xx,np.array([0,0,1]),beta);yy=rot(yy,np.array([0,0,1]),beta)
 xx=AA.T@xx;yy=BB.T@yy
 return np.r_[Ex.T@(xx-x),Ey.T@(yy-y)]
from scipy.optimize import brentq
jfun=lambda c:approx_derivative(lambda q:residual(q,c),np.zeros(4),method='3-point',abs_step=1e-5)
cstar=brentq(lambda c:np.linalg.det(jfun(c)[:3,:3]),-.5,-.1,xtol=1e-13)
print('Cstar',cstar,'singularvalues',np.linalg.svd(jfun(cstar))[1])
JU,JS,JVT=np.linalg.svd(jfun(cstar));JV=JVT.T
for rho in [.01,.003,.001]:
 vals=[]
 for t in np.linspace(0,2*np.pi,2001):
  q=JV[:,2:]@(rho*np.array([np.cos(t),np.sin(t)]))
  vals.append(JU[:,2:].T@(residual(q,cstar)+residual(-q,cstar)-2*residual(np.zeros(4),cstar))/2)
 vals=np.array(vals);ang=np.unwrap(np.arctan2(vals[:,1],vals[:,0]));wind=(ang[-1]-ang[0])/(2*np.pi)
 print('quadratic rho winding min/max',rho,wind,np.min(np.linalg.norm(vals,axis=1))/rho**2,np.max(np.linalg.norm(vals,axis=1))/rho**2)
print('orient',np.linalg.det(JU)*np.linalg.det(JV))
from scipy.optimize import root
def point(u,base,E):
 ss=np.dot(u,u);return ((1-ss)*base+2*E@u)/(1+ss)
def gmap(q):
 x=point(q[:2],x0,Ex);y=point(q[2:],y0,Ey);v=x+y;r=np.linalg.norm(v);z=v[2]
 a=-(b+3*cstar)*r0*r0;beta=a+b*r*r+3*cstar*z*z;theta=2*b*r*z
 if r<1e-12:xx=x;yy=y
 else:xx=rot(x,v/r,theta);yy=rot(y,v/r,theta)
 xx=AA.T@rot(xx,np.array([0,0,1]),beta);yy=BB.T@rot(yy,np.array([0,0,1]),beta)
 return xx,yy
def resst(q):
 xx,yy=gmap(q)
 return np.r_[(Ex.T@xx)/(1+xx@x0)-q[:2],(Ey.T@yy)/(1+yy@y0)-q[2:]]
rng=np.random.default_rng(322);sol=[]
for i in range(1200):
 start=rng.normal(size=4)*rng.choice([.1,.5,1,2,5,10])
 rr=root(resst,start,tol=1e-10)
 if np.linalg.norm(resst(rr.x))<1e-8:
  x=point(rr.x[:2],x0,Ex);y=point(rr.x[2:],y0,Ey);p=np.r_[x,y]
  if all(np.linalg.norm(p-pp)>1e-4 for pp in sol):
   sol.append(p);print('NEWROOT',len(sol),p,'r,z',np.linalg.norm(x+y),(x+y)[2],flush=True)
print('total distinct numerical roots',len(sol))
from pathlib import Path
Path('workspace/agent4_cubic_collective.py').write_text(Path('scratchpad.py').read_text())