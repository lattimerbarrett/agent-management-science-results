import sys,numpy as np
sys.path.insert(0,'workspace');import agent2_genuine_field as gf
from agent2_blowup_ode import BlowupODE
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
z=np.load('workspace/agent1_actualQ_-0.72.npz');gf.ob=BlowupODE(z['base'],z['f'],z['g'],float(z['L']),z['mus']);gf.S=gf.ob.nodes;gf.V=gf.ob.V;gf.Vm=gf.ob.Vmu;gf.L=gf.ob.N;T=float(z['p'][0]);B=z['B'];Bi=np.linalg.inv(B);y=CubicSpline(z['x'],z['y'],axis=1)
def J(s):return T*Bi@gf.jac(y(s))@B
print('Jmax',max(abs(J(s)).max()for s in np.linspace(0,1,101)),'Bcond',np.linalg.cond(B),flush=True)
sol=solve_ivp(lambda s,M:(J(s)@M.reshape(7,7)).ravel(),[0,1],np.eye(7).ravel(),method='DOP853',rtol=1e-11,atol=1e-12,dense_output=True);M=sol.y[:,-1].reshape(7,7);ev,V=np.linalg.eig(M);print('status',sol.success,'steps',len(sol.t),'Mmax',abs(M).max(),'EV',ev,flush=True)
np.savez('workspace/agent1_floatFloquetPhysical.npz',B=B,M=M,ev=ev,V=V,T=T)
