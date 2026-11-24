import numpy as np,sys
sys.path.insert(0,'workspace')
from agent1_fast_face import decode
from agent2_blowup_ode import BlowupODE
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline
z=np.load('workspace/agent1_GENUINE_s4_periodic.npz');S=z['base'];L=float(z['L']);eq=z['eq'];B=z['B'];C=np.linalg.inv(B);D=np.zeros((7,7));ob=BlowupODE(S,z['f'],z['g'],L,z['mus']);V=ob.V;Vm=ob.Vmu
# Independent actual vector field: fixed damping matrix is zero.
text=open('workspace/agent1_fast_face.py').read();block=text[text.index('  def fun'):text.index('  def bc')];exec('\n'.join(line[2:]for line in block.splitlines()))
actual=fun

def fun(t,a,par):return actual(t,a,np.r_[par[0],0.])
def bc(a,b,par):return np.r_[a-b,(C@(decode(a)-eq))[1]]
def jac(t,a,par):
 h=1e-20;ja=np.empty((7,7,a.shape[1]));jp=np.empty((7,1,a.shape[1]))
 for j in range(7):
  ac=a.astype(complex);ac[j]+=h*1j;ja[:,j,:]=fun(t,ac,par).imag/h
 pc=par.astype(complex);pc[0]+=h*1j;jp[:,0,:]=fun(t,a,pc).imag/h
 return ja,jp
if __name__=='__main__':
 mesh=np.linspace(0,1,1001);aa=CubicSpline(z['x'],z['a'],axis=1)(mesh)
 sol=solve_bvp(fun,bc,mesh,aa,p=z['p'],tol=1e-9,max_nodes=30000,fun_jac=jac)
 Y=decode(sol.y);print('status',sol.status,'period',sol.p,'theta',-Y[0].max(),-Y[0].min(),'maxres',max(sol.rms_residuals))
 assert sol.status==0
 np.savez('workspace/agent1_GENUINE_s4_periodic_refined.npz',x=sol.x,a=sol.y,y=Y,p=sol.p,B=B,eq=eq,f=z['f'],g=z['g'],L=L,mus=z['mus'],base=S,q1=z['q1'],q2=z['q2'])
