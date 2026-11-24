import sys;sys.path.insert(0,'workspace');from agent1_geometry_flip_flow import *
from scipy.optimize import least_squares
from scipy.special import expit,logit
import numpy as np

def logflow(t,z):
 m=g.m;tt,w=g.smoothw(z[0]);hc=z[1:5];h=m.V@hc;u=w*m.p*h;M=m.V.T@(w[:,None]*m.V);aa=-m.V@np.linalg.solve(M,m.V.T@(u*m.p));d=np.dot(u,m.p*m.p);zz=w*m.p*m.p/m.C;L1=m.p*h+2*aa/m.p-d/m.C;N=m.V.T@(zz[:,None]*m.V);cc=-m.V@np.linalg.solve(N,m.V.T@(zz*L1*m.q));dd=np.dot(zz*L1,m.q*m.q);R=2*aa/m.p+2*cc/m.q-(d+dd)/m.C
 ud=-R[3]/(1+tt) if z[0]>=0 else R[2]/(1-tt)
 amps=np.exp(np.clip(z[5:],-350,15));out=m.ode(t,np.r_[w,hc,amps]);beta=-(m.q[6:]*aa[6:]+m.p[6:]*cc[6:]+d)/m.C
 return np.r_[ud,out[8:12],beta]
