import numpy as np
from scipy.optimize import minimize, check_grad
from scipy.special import logsumexp
from pathlib import Path
rng=np.random.default_rng(167)
n=128
freq=np.fft.fftfreq(n)
H=np.fft.ifft((-1j*np.sign(freq))[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
# Remove Nyquist; H is real skew and H^2=-I on mean-zero non-Nyquist signals.
Proj=-H@H
masks=[]
for l in range(1,n+1):
 for j in range(n):
  v=np.zeros(n);v[(np.arange(l)+j)%n]=1/l;masks.append(v)
B=np.array(masks)
r=30.
gamma=1.
def fun(x,detail=False):
 u=Proj@x[:n];v=H@u;t=x[n:];lam=np.exp(t);inv=1/lam
 rho=u*u+v*v+1e-15
 p00=u*u/rho;p11=v*v/rho;p01=u*v/rho
 k=lam-inv
 w00=lam-k*p00;w11=lam-k*p11;w01=-k*p01
 s00=B@w00;s11=B@w11;s01=B@w01
 det=s00*s11-s01*s01
 ld=np.log(np.maximum(det,1e-300));la=logsumexp(r*ld)/r
 probs=np.exp(r*ld-r*la)
 # Gradient of la wrt weight components.
 g00=B.T@(probs*s11/det);g11=B.T@(probs*s00/det);g01=B.T@(-2*probs*s01/det)
 du00=2*u*v*v/rho**2;dv00=-2*u*u*v/rho**2
 du11=-du00;dv11=-dv00
 du01=v*(v*v-u*u)/rho**2;dv01=u*(u*u-v*v)/rho**2
 gu=-k*(g00*du00+g11*du11+g01*du01)
 gv=-k*(g00*dv00+g11*dv11+g01*dv01)
 gt=g00*(lam-(lam+inv)*p00)+g11*(lam-(lam+inv)*p11)+g01*(-(lam+inv)*p01)
 out=np.dot(rho,lam);inp=np.dot(rho,inv)
 ln=.5*(np.log(out)-np.log(inp))
 common=lam/out-inv/inp
 dnu=u*common;dnv=v*common;dnt=.5*rho*(lam/out+inv/inp)
 grad_u=Proj.T@(dnu-gamma*gu+H.T@(dnv-gamma*gv))
 grad_t=dnt-gamma*gt
 obj=ln-gamma*la
 if detail==2:return ln,la,np.r_[Proj.T@(dnu+H.T@dnv),dnt],np.r_[Proj.T@(gu+H.T@gv),gt]
 if detail:return np.exp(ln),np.max(det),np.exp(la),obj
 return -obj,-np.r_[grad_u,grad_t]
x0=np.r_[rng.normal(size=n),np.full(n,1.)]
print('gradient absolute error',check_grad(lambda x:fun(x)[0],lambda x:fun(x)[1],x0))
best=None
for i in range(2):
 x0=np.r_[rng.normal(size=n),rng.uniform(.1,4,size=n)]
 res=minimize(fun,x0,jac=True,method='L-BFGS-B',bounds=[(None,None)]*n+[(0.,15.)]*n,options={'maxiter':800,'ftol':1e-12,'maxls':50})
 dets=fun(res.x,True)
 print(i,res.success,res.nit,'norm / max_char / smooth_char / logobjective:',dets,flush=True)
 if best is None or dets[-1]>best[-2]:best=(*dets,res.x)
x=best[-1]
for target in [3.,10.,30.,100.,300.,1000.]:
 def obj2(x):
  ln,la,gn,ga=fun(x,2);return -ln,-gn
 def con(x):
  ln,la,gn,ga=fun(x,2);return np.log(target)-la
 def conjac(x):return -fun(x,2)[3]
 res=minimize(obj2,x,jac=True,method='SLSQP',bounds=[(-100.,100.)]*n+[(0.,15.)]*n,constraints={'type':'ineq','fun':con,'jac':conjac},options={'maxiter':1500,'ftol':1e-10})
 x=res.x
 print('target constrained',target,res.success,res.nit,fun(x,True),flush=True)
np.savez('workspace/agent3_phase_search.npz',x=x,H=H,B=B)
Path('workspace/agent3_phase_search.py').write_text(Path('scratchpad.py').read_text())
