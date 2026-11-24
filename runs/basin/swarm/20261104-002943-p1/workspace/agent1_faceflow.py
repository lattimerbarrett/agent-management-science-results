import sys;sys.path.insert(0,'workspace');import agent1_slowode as m
import numpy as np
from scipy.integrate import solve_ivp
missing=5;D=np.load('workspace/agent1_pellface5.npz');m.x=D['lam'];m.V=np.array([m.x**j for j in range(4)]).T;m.p=D['p'];m.q=D['q'];m.C=float(D['C']);m.w0=D['w0'];U=D['U']
A=np.vstack([np.ones(8),(m.V*m.p[:,None]).T,np.eye(8)[missing]]);_,s,vt=np.linalg.svd(A);T=vt[6:].T

def ff(t,z):
 dz=m.ode(t,np.r_[m.w0+T@z[:2],z[2:]])
 return np.r_[T.T@dz[:8],dz[8:]]
def event(t,z):return min(np.delete(m.w0+T@z[:2],missing))-1e-7
event.terminal=True;event.direction=-1
