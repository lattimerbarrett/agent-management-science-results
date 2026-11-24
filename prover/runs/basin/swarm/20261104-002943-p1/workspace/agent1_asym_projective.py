import sys;sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
import numpy as np
from scipy.integrate import solve_ivp
g.setup((0,1,0,0),np.sqrt(5+2*np.sqrt(2)));m=g.m;S=m.V.T@((g.wref*m.p*m.p)[:,None]*m.V)

def projflow(t,z):
 dz=g.flow(t,z);h=z[1:5];aa=z[5:];hd=dz[1:5];ad=dz[5:];rr=(h@S@hd+aa@ad)/(h@S@h+aa@aa)
 return np.r_[dz[0],hd-rr*h,ad-rr*aa]

def evF(t,z):return g.fuel(z)
evF.direction=-1;evF.terminal=True
