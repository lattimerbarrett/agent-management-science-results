import numpy as np
from scipy.spatial.transform import Rotation
from scipy.linalg import null_space
from scipy.optimize import root
from scipy.optimize._numdiff import approx_derivative
from pathlib import Path
def rot(v,axis,ang):return v*np.cos(ang)+np.cross(axis,v)*np.sin(ang)+axis*np.dot(axis,v)*(1-np.cos(ang))
def setup(xsq):
 U=np.sqrt(xsq);Z=(1-xsq)/U;T=np.sqrt(1-U*U-Z*Z);L=1-U*U;r0=2*T*U/np.sqrt(L)
 AA=Rotation.from_quat([T,0,Z,U]).as_matrix();BB=Rotation.from_quat([-T,0,Z,U]).as_matrix()
 d=np.array([-Z*r0/T,L*r0/(U*T),0]);x0=(np.array([0,0,r0])+d)/2;y0=(np.array([0,0,r0])-d)/2
 Ex=null_space(x0.reshape(1,3));Ey=null_space(y0.reshape(1,3));b=np.pi/(4*r0*r0)
 def F(x,y,c):
  v=x+y;r=np.linalg.norm(v);z=v[2];a=-(b+3*c)*r0*r0;beta=a+b*r*r+3*c*z*z;theta=2*b*r*z
  if r<1e-10:xx=x;yy=y
  else:xx=rot(x,v/r,theta);yy=rot(y,v/r,theta)
  return AA.T@rot(xx,np.array([0,0,1]),beta),BB.T@rot(yy,np.array([0,0,1]),beta)
 def resq(q,c):
  x=x0+Ex@q[:2];x/=np.linalg.norm(x);y=y0+Ey@q[2:];y/=np.linalg.norm(y);xx,yy=F(x,y,c)
  return np.r_[Ex.T@(xx-x),Ey.T@(yy-y)]
 def minor(c):return np.linalg.det(approx_derivative(lambda q:resq(q,c),np.zeros(4),method='3-point',abs_step=2e-5)[:3,:3])
 m0=minor(0);m1=minor(1);c=-m0/(m1-m0)
 def point(u,base,E):
  ss=u@u;return ((1-ss)*base+2*E@u)/(1+ss)
 def res(q):
  xx,yy=F(point(q[:2],x0,Ex),point(q[2:],y0,Ey),c)
  return np.r_[(Ex.T@xx)/(1+xx@x0)-q[:2],(Ey.T@yy)/(1+yy@y0)-q[2:]]
 return c,b,r0,F,res,point,x0,y0,Ex,Ey
rng=np.random.default_rng(127)
for xsq in [.52,.55,.6,.65,.7,.8,.85,.9,.95,.98,.99,.995]:
 c,b,r0,F,res,point,x0,y0,Ex,Ey=setup(xsq);sol=[]
 for i in range(250):
  start=rng.normal(size=4)*rng.choice([.2,.5,1,2,5])
  rr=root(res,start,tol=1e-9)
  if np.linalg.norm(res(rr.x))<1e-7:
   x=point(rr.x[:2],x0,Ex);y=point(rr.x[2:],y0,Ey);p=np.r_[x,y]
   if all(np.linalg.norm(p-pp)>1e-3 for pp in sol):sol.append(p)
 print('xsq,C,B,r0,roots',xsq,c,b,r0,len(sol)+1,'rz',sorted([(round(np.linalg.norm(p[:3]+p[3:]),3),round((p[:3]+p[3:])[2],3)) for p in sol]),flush=True)
Path('workspace/agent4_cubic_scan.py').write_text(Path('scratchpad.py').read_text())