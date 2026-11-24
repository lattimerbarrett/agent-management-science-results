import sys,numpy as np,time
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
mi=np.sqrt(5-2*np.sqrt(2));mo=np.sqrt(5+2*np.sqrt(2));g.setup((0,1,0,1),mi);g.m.x[-2:]=[-mo,mi];g.m.V=g.m.x[:,None]**np.arange(4);g.m.p=g.Pp(g.m.x);g.m.q=g.Qp(g.m.x);L=g.L.copy()
X=np.array([1.,-2.84035686,8.61381647,28.58541989]);A=np.array([.63408396,.06748922]);X/=X[3];A/=28.58541989
x0=np.r_[np.log(X[0]),X[1],np.log(X[2]),np.log(A)]
count=0;best=(1e100,None,None);start=time.time()
def up(t,z):return z[0]
up.direction=1;up.terminal=True
def down(t,z):return z[0]
down.direction=-1;down.terminal=True
def fun(xx):
 global count,best
 count+=1;Xp=np.array([np.exp(xx[0]),xx[1],np.exp(xx[2]),1.]);Ap=np.exp(xx[3:]);z=np.r_[0.,np.linalg.solve(L,Xp),Ap]
 try:
  s1=solve_ivp(g.flow,(0,300),z,rtol=2e-7,atol=2e-10,max_step=.2,events=[up,g.evF,g.evU])
  if not len(s1.t_events[0]):return np.ones(7)*100
  z1=s1.y[:,-1];z1[0]=1e-9;s2=solve_ivp(g.flow,(s1.t[-1],300),z1,rtol=2e-7,atol=2e-10,max_step=.2,events=[down,g.evF,g.evU])
  if not len(s2.t_events[0]):return np.ones(7)*100
  Y=L@s2.y[1:5,-1];rho=Y[3];Y/=rho;Ao=s2.y[5:,-1]/rho
  if min(Y[0],Y[2],rho,min(Ao))<=0:return np.ones(7)*100
  r=np.r_[np.log(Y[0])-xx[0],Y[1]-xx[1],np.log(Y[2])-xx[2],np.log(Ao)-xx[3:],10*max(0,.1+np.min(np.tanh(s1.y[0]))),10*max(0,.1-np.max(np.tanh(s2.y[0])))]
  val=np.linalg.norm(r)
  if val<best[0]:best=(val,xx.copy(),(Y,Ao,rho,s2.t[-1]));print('BEST',count,val,'xx',xx,'rho,T',rho,s2.t[-1],flush=True)
  return r
 except Exception:return np.ones(7)*100
res=least_squares(fun,x0,bounds=([-10,-20,-10,-15,-15],[10,20,10,5,5]),max_nfev=150,diff_step=1e-4,ftol=1e-9,xtol=1e-9,gtol=1e-9)
print('COMPLETE',res.message,'count',count,'best',best,'time',time.time()-start)
np.savez('workspace/agent3_balanced_fuel_shoot.npz',bestnorm=best[0],bestx=best[1],resultx=res.x,fun=res.fun)
