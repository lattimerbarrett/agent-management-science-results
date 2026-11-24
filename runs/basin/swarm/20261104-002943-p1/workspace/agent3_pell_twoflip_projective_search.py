import numpy as np,sys,pickle,time
from scipy.integrate import solve_ivp
sys.path.insert(0,'workspace');import agent2_pell_fourminus_ode as m
w=m.w0.copy();n=m.n;s=m.s;B=np.column_stack([m.ode(0,np.r_[w,np.eye(s)[j],np.zeros(4)])[:n] for j in range(s)]);_,sv,vh=np.linalg.svd(B);hk=vh[-1];fuelrow=(w*m.p**3)@m.V/m.C;hk/=-(fuelrow@hk)
rng=np.random.default_rng(909)
def rhs(t,z):
 f=m.ode(t,z);D=.25*np.sum((m.C+m.p[:8]**2)*f[:8]**2/z[:8])/m.C+sum(4*(m.C+m.p[8:]**2)*z[-4:]**2)/m.C
 f[n:]+=D*z[n:]
 return f
def boundary(t,z):return min(z[:8])-1e-8
boundary.terminal=True;boundary.direction=-1
def blow(t,z):return 1e8-max(abs(z[n:]))
blow.terminal=True;blow.direction=-1
results=[];best=None;start=time.time()
for j in range(120):
 pair=list(__import__('itertools').combinations(range(4),2))[j%6]
 hh=rng.normal(size=4);hh*=10**rng.uniform(-2,.3)/max(abs(m.p*(m.V@hh)));hh+=hk*(-1-fuelrow@hh)
 A=np.zeros(4);A[list(pair)]=10**rng.uniform(-4,-.5,size=2)
 z0=np.r_[w,hh,A]
 try:
  sol=solve_ivp(rhs,(0,20),z0,rtol=2e-7,atol=2e-10,max_step=.2,events=[boundary,blow])
  result=(sol.t[-1],j,pair,min(sol.y[:8,-1]),max(abs(sol.y[n:,-1])),np.linalg.norm(sol.y[:8,-1]-w[:8]))
  results.append((result,z0,sol.t,sol.y));
  if best is None or result[0]>best[0][0]:best=results[-1];print('best',result,'elapsed',time.time()-start,flush=True)
 except Exception as e:
  import traceback;traceback.print_exc();raise
 if time.time()-start>115:break
pickle.dump(results,open('workspace/agent3_pell_twoflip_projective_search.pkl','wb'))
print('COMPLETE',len(results),'best',best[0])
for result,z0,ts,ys in sorted(results,key=lambda r:r[0][0],reverse=True)[:12]:
 sol=solve_ivp(rhs,(20,500),ys[:,-1],rtol=2e-8,atol=2e-11,max_step=1,events=[boundary,blow])
 print('CONTINUE',result[1:3],sol.t[-1],min(sol.y[:8,-1]),'wchange',np.linalg.norm(sol.y[:8,-1]-w[:8]),'amps',sol.y[-4:,-1],flush=True)
