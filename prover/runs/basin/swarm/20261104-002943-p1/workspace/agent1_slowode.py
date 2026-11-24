import numpy as np,pickle
D=pickle.load(open('workspace/agent4_nonmax_normal_jet.pkl','rb'))
x=np.array(D['x'],float)/8;V=np.array([x**j for j in range(4)]).T
p=np.array(D['q'],float).ravel()/8**4;q=np.array(D['Q'],float).ravel()/8**4;C=float(D['C'])/8**8
w0=np.array(D['w0'],float).ravel()

def jet(w,u,p,C):
 M=V.T@(w[:,None]*V)
 aa=-V@np.linalg.solve(M,V.T@(u*p))
 bb=-V@np.linalg.solve(M,V.T@(u*aa))
 d=np.dot(u,p*p);e=np.dot(u,p*aa)
 z=w*p*p/C
 z1=(u*p*p+2*w*p*aa-z*d)/C
 z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*d-z*e)/C
 return z,z1,z2

def ode(t,z):
 w=z[:8];h=V@z[8:];u=w*p*h
 zz,z1,z2=jet(w,u,p,C)
 # secondstep with both linear+quadratic inputs
 M=V.T@(zz[:,None]*V)
 aa=-V@np.linalg.solve(M,V.T@(z1*q))
 bb=-V@np.linalg.solve(M,V.T@(z2*q+z1*aa))
 dd=np.dot(z1,q*q);ee=np.dot(z2,q*q)+np.dot(z1,q*aa)
 f1=(z1*q*q+2*zz*q*aa-w*dd)/C
 f2=(z2*q*q+2*z1*q*aa+zz*(aa*aa+2*q*bb)-f1*dd-w*ee)/C
 b=f1-u
 G=V.T@((w*p*p)[:,None]*V)
 hd=np.linalg.solve(G,V.T@(p*(f2-b*p*h)))
 return np.r_[b,hd]
