import sys;sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
mu=np.sqrt(5+2*np.sqrt(2));g.setup((0,1,1,0),mu);m=g.m;perm=[5,4,3,2,1,0,7,6]
G=m.V.T@((m.w0*m.p*m.p)[:,None]*m.V)
SS=[]
for j in range(4):
 u=m.w0*m.p*m.V[:,j];zz=m.weightjet([m.w0,u],m.p)[1][perm]
 SS.append(np.linalg.solve(G,m.V.T@(m.p*zz)))
SS=np.column_stack(SS);AA=np.array([[0,abs(m.p[7])/np.sqrt(m.C)],[abs(m.p[6])/np.sqrt(m.C),0]])
print('Serr',np.linalg.norm(SS@SS-np.eye(4)),np.linalg.norm(g.L[0]@SS+g.L[0]),np.linalg.norm(g.L[3]@SS-g.L[3]),'AA',AA,flush=True)

def evup(t,z):return z[0]
evup.direction=1;evup.terminal=True

def halfmap(phys,details=False):
 z0=np.r_[0,np.linalg.solve(g.L,np.r_[1,phys[:3]]),phys[3:]]
 sol=solve_ivp(g.flow,(0,50),z0,rtol=2e-7,atol=1e-9,events=[evup,g.evF,g.evU],max_step=.05)
 if not len(sol.t_events[0]):return None
 z=sol.y[:,-1];hnew=SS@z[1:5];anew=AA@z[5:];ph=g.L@hnew;scale=ph[0]
 if scale<=0:return None
 return np.r_[ph[1:]/scale,anew/scale],scale,sol.t[-1]
