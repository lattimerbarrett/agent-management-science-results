import numpy as np
from scipy.spatial.transform import Rotation
p=.394922939913524;m=np.sqrt(1-p*p);U=.886226925452758;Z=.242152241642755;d0=np.arctan2(Z,U)
r=1.;z=.2;disc=(r*r-4*p*p)**2+16*p*p*z*z
xw=(r*r-2*z*z-4*p*p+np.sqrt(disc))/(2*(r*r-z*z))
w=np.sqrt(xw);k=np.sqrt(m*m-xw);a=2*d0-2*np.arccos(w/m);b=2*np.arctan2(z*(1-xw),r*w*k)
V=np.sqrt(r*r-z*z);v=np.array([V,0,z]);d=np.array([-k*z/p,(1-xw)*z/(p*w),k*V/p]);x=(v+d)/2;y=(v-d)/2
A=Rotation.from_quat([p,0,k,w]).as_matrix()
axis=v/r
ax=A@x
print('computedphase',np.arctan2(np.dot(axis,np.cross(x,ax)),np.dot(x,ax)-np.dot(x,axis)**2),'formula',b)
print('sumconstraint',A@x+Rotation.from_quat([-p,0,k,w]).as_matrix()@y-v)
print('params',a,b,x,y)
from scipy.linalg import null_space
from scipy.optimize._numdiff import approx_derivative
x=Rotation.from_rotvec([0,0,-a/2]).apply(x);y=Rotation.from_rotvec([0,0,-a/2]).apply(y)
A0=Rotation.from_quat([p,0,Z,U]).as_matrix();B0=Rotation.from_quat([-p,0,Z,U]).as_matrix()
E=null_space(x.reshape(1,3));F=null_space(y.reshape(1,3))
def rot(vec,axis,ang):
 return vec*np.cos(ang)+np.cross(axis,vec)*np.sin(ang)+axis*np.dot(axis,vec)*(1-np.cos(ang))
def fun(q):
 xx=x+E@q[:2];xx/=np.linalg.norm(xx);yy=y+F@q[2:];yy/=np.linalg.norm(yy)
 vv=xx+yy;rr=np.linalg.norm(vv)
 x1=rot(xx,vv/rr,b);y1=rot(yy,vv/rr,b)
 x1=rot(x1,np.array([0,0,1]),a);y1=rot(y1,np.array([0,0,1]),a)
 return np.r_[E.T@(A0.T@x1-xx),F.T@(B0.T@y1-yy)]
print('correctedres',fun(np.zeros(4)),'det',np.linalg.det(approx_derivative(fun,np.zeros(4))))
from pathlib import Path
Path('workspace/agent3_sheet_orientation_numeric.py').write_text(Path('scratchpad.py').read_text())
