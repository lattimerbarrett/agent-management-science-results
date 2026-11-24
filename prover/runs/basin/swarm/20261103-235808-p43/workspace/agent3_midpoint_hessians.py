import pathlib
import sympy as sp
import numpy as np
from scipy.spatial.transform import Rotation
x=sp.Matrix(sp.symbols('x:3'));y=sp.Matrix(sp.symbols('y:3'));C=sp.symbols('C',real=True)
s=x+y; rr=s.dot(s); den=1+C*C*rr
xp=((1-C*C*rr)*x+2*C*s.cross(x)+2*C*C*s*s.dot(x))/den
yp=((1-C*C*rr)*y+2*C*s.cross(y)+2*C*C*s*s.dot(y))/den
DF=sp.lambdify([list(x)+list(y),C],xp.col_join(yp).jacobian(list(x)+list(y)),'numpy')
Omega=np.kron(np.eye(2),np.array([[0,1],[-1,0]]))
def bas(x):
 e=np.eye(3)[np.argmin(abs(x))]; e=e-x*(e@x);e/=np.linalg.norm(e);f=np.cross(x,e);return np.array([e,f]).T
for k in [1.,3.,10.,100.]:
 A=Rotation.from_rotvec([2*np.arctan(k),0,0]).as_matrix(); B=Rotation.from_rotvec([0,2*np.arctan(k),0]).as_matrix();AB=np.block([[A,np.zeros((3,3))],[np.zeros((3,3)),B]])
 t=np.sqrt(1+k*k)/(k*k+2)
 for sign in [-1,1]:
  p=sign*np.sqrt(2*k*k+3)/(k*k+2);xx=np.array([p,t,k*t]);yy=np.array([t,p,-k*t]); E=np.block([[bas(xx),np.zeros((3,2))],[np.zeros((3,2)),bas(yy)]])
  L=E.T@AB@DF(list(xx)+list(yy),k*np.sqrt(1+k*k))@E
  S=2*Omega@(np.eye(4)-L)@np.linalg.inv(np.eye(4)+L)
  print(k,sign,'symm error',np.max(abs(S-S.T)),'S evals',np.linalg.eigvalsh((S+S.T)/2),'L eig',np.linalg.eigvals(L))
