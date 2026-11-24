import sys,numpy as np,pickle,time,itertools
from scipy.integrate import solve_ivp
sys.path.insert(0,'workspace');import agent1_generic_flip_flow as g
rng=np.random.default_rng(788);records=[];best=None;start=time.time();mi=np.sqrt(5-2*np.sqrt(2));mo=np.sqrt(5+2*np.sqrt(2))
for j in range(1000):
 bits=[(0,0,1,1),(0,1,0,1),(0,1,1,0)][j%3];pair=[(-mi,mi),(-mi,mo),(-mo,mi),(-mo,mo)][(j//3)%4]
 g.setup(bits,mi);g.m.x[-2:]=pair;g.m.V=g.m.x[:,None]**np.arange(4);g.m.p=g.Pp(g.m.x);g.m.q=g.Qp(g.m.x)
 S=g.m.V[:6].T@((g.wref[:6]*g.m.p[:6]**2)[:,None]*g.m.V[:6]);L=g.L.copy()
 X=np.array([1.,rng.uniform(-3,3),10**rng.uniform(-1,1),10**rng.uniform(-1,1.5)]);A=10**rng.uniform(-3,.5,size=2);h=np.linalg.solve(L,X);norm=np.sqrt(h@S@h+A@A);z0=np.r_[0.,h/norm,A/norm]
 def rhs(t,z):
  out=g.flow(t,z);r=z[1:5]@S@out[1:5]+z[5:]@out[5:];out[1:]-=r*z[1:];return out
 def evU(t,z):return 50-abs(z[0])
 evU.terminal=True;evU.direction=-1
 try:
  sol=solve_ivp(rhs,(0,200),z0,rtol=5e-7,atol=2e-9,events=[g.evF,evU],max_step=.2)
  tt=np.tanh(sol.y[0]);cross=np.sum((tt[:-1]*tt[1:]<0)&(sol.t[1:]>1e-4));turns=np.sum((np.diff(tt)[:-1]*np.diff(tt)[1:]<0)&(abs(tt[1:-1])<.99));rec=(int(cross),int(turns),sol.t[-1],j,bits,pair,X,A)
  records.append((rec,z0,sol.t,sol.y));
  if best is None or rec[:2]>best[0][:2]:best=records[-1];print('BEST',rec[:6], 'X,A',X,A,'elapsed',time.time()-start,flush=True)
 except Exception as e:print('FAILED',j,str(e),flush=True)
 if time.time()-start>115:break
pickle.dump(records,open('workspace/agent3_balanced_norm_projective_search.pkl','wb'))
print('COMPLETE',len(records),'BEST',best[0])
