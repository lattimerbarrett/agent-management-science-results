import sys;sys.path.insert(0,'workspace');from agent1_flip_physical_flow import *
from scipy.special import expit

def smoothw(u):
 tt=np.tanh(u);w=wref.copy();w[:6]*=1-tt/m.x[:6];w[2]=wref[2]*2*expit(2*u);w[3]=wref[3]*2*expit(-2*u)
 return tt,w

def smoothflow(t,z):
 tt,w=smoothw(z[0]);zz=m.ode(t,np.r_[w,z[1:]]);P=tt**4-10*tt*tt+11
 ud=24*(z[2]+5*z[4])*(tt*tt-5)*(tt*tt-9)/P
 return np.r_[ud,zz[8:]]
def fuelS(z):return 12*(z[1]+5*z[3]-np.tanh(z[0])*(z[2]+5*z[4]))
def evFS(t,z):return fuelS(z)
evFS.terminal=True;evFS.direction=-1
def evNorm(t,z):return 1e7-np.linalg.norm(z[1:])
evNorm.terminal=True;evNorm.direction=-1
