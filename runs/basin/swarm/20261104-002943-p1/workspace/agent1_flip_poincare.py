import sys;sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
bits=(0,1,0,0);mu=np.sqrt(5+2*np.sqrt(2));g.setup(bits,mu)

def evup(t,z):return z[0]
evup.direction=1;evup.terminal=True
def evdn(t,z):return z[0]
evdn.direction=-1;evdn.terminal=True

def poincare(phys,rtol=1e-8):
 # phys=(K1,K2,E,A+,A-), K0=1
 zz=np.r_[0,np.linalg.solve(g.L,np.r_[1,phys[:3]]),phys[3:]]
 sol=solve_ivp(g.flow,(0,50),zz,rtol=rtol,atol=rtol/100,events=[evup,g.evF,g.evU],max_step=.05)
 if not len(sol.t_events[0]):return None
 z=sol.y[:,-1];z[0]=0
 ss=solve_ivp(g.flow,(0,50),z,rtol=rtol,atol=rtol/100,events=[evdn,g.evF,g.evU],max_step=.05)
 if not len(ss.t_events[0]):return None
 out=ss.y[:,-1];ph=g.L@out[1:5];scale=ph[0]
 return np.r_[ph[1:]/scale,out[5:]/scale],scale,sol.t[-1]+ss.t[-1]
