import sys;sys.path.insert(0,'workspace');from agent1_faceflow import *
from scipy.special import logsumexp
inds=np.array([j for j in range(8) if j!=missing]);Ai=A[:5,inds];vv=m.V[inds];pp=m.p[inds];qq=m.q[inds];cc=m.C

def logode(t,z):
 w=np.exp(z[:7]);hc=z[7:];h=vv@hc
 M=vv.T@(w[:,None]*vv);aa=-vv@np.linalg.solve(M,vv.T@(w*pp*pp*h));bb=-vv@np.linalg.solve(M,vv.T@(w*pp*h*aa))
 d=np.dot(w,pp**3*h);e=np.dot(w,pp*pp*h*aa)
 zz=w*pp*pp/cc;L1=pp*h+2*aa/pp-d/cc;L2=aa*aa/pp**2+2*bb/pp+2*h*aa-L1*d/cc-e/cc
 K=vv.T@(zz[:,None]*vv);a2=-vv@np.linalg.solve(K,vv.T@(zz*L1*qq));b2=-vv@np.linalg.solve(K,vv.T@(zz*(L2*qq+L1*a2)))
 dd=np.dot(zz*L1,qq*qq);ee=np.dot(zz*L2,qq*qq)+np.dot(zz*L1,qq*a2)
 f1= L1+2*a2/qq-dd/cc
 R=f1-pp*h
 f2=L2+2*L1*a2/qq+a2*a2/qq**2+2*b2/qq-f1*dd/cc-ee/cc
 G=vv.T@((w*pp*pp)[:,None]*vv);hd=np.linalg.solve(G,vv.T@(w*pp*(f2-R*pp*h)))
 # exact tangent correction plus offmanifold feedback
 corr=np.linalg.solve((Ai*w[None,:])@Ai.T,Ai@(w*R)+.3*(Ai@w-np.array([1,0,0,0,0])))
 R-=Ai.T@corr
 return np.r_[R,hd]
