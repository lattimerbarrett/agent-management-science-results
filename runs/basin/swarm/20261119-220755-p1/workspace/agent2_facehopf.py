import sys;sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
import numpy as np
from scipy.linalg import eig
from scipy.optimize import brentq
from scipy.integrate import solve_bvp
from scipy.special import expit,logit
from pathlib import Path
z=np.load('workspace/agent2_rational_positive_eq_0.4.npz');ob=BlowupODE(z['base'],z['f'],z['g'],float(z['N']),z['mus']);eq=z['y'];J=z['J'];ev,V=np.linalg.eig(J);Vi=np.linalg.inv(V);target=np.argmin(abs(ev-(.5+2.319j)));pair=[target,np.argmin(abs(ev-ev[target].conjugate()))];P=(V[:,pair]@Vi[pair,:]).real;D=np.diag([0,1,1,1,1,0,0])@P
kh=brentq(lambda k:sorted([a for a in np.linalg.eigvals(J-k*D) if a.imag>0],key=lambda a:abs(a.imag-2.37))[0].real,.8,1.2)
evh,Vh=np.linalg.eig(J-kh*D);ih=np.argmin(abs(evh-(0+2.37j)));vv=Vh[:,ih];vv/=abs(vv[0]);VR=vv.real;VI=vv.imag;others=[j for j in range(7) if j not in pair];BB=np.column_stack([VR,VI]+[V[:,j].real if abs(ev[j].imag)<1e-3 else (V[:,j].real if ev[j].imag>0 else V[:,j].imag) for j in others]);
# Use pseudoinverse of target real/imag supplemented with ORIGINAL complementary eigenspace basis.
cols=[VR,VI];used=set(pair)
for j,a in enumerate(ev):
 if j in used:continue
 if abs(a.imag)<1e-4:cols.append(V[:,j].real);used.add(j)
 elif a.imag>0:cols.extend([V[:,j].real,V[:,j].imag]);used.add(j);used.add(np.argmin(abs(ev-a.conjugate())))
BB=np.column_stack(cols);CC=np.linalg.inv(BB)
print('Hopf',kh,'eig',evh[ih],'Dnorm',np.linalg.norm(D),'basiscondition',np.linalg.cond(BB),flush=True)
def decode(a):
 y=a.copy();y[0]=-expit(a[0]);y[-2:]=np.exp(np.clip(a[-2:],-700,80));return y

def encode(y):
 a=y.copy();a[0]=logit(-y[0]);a[-2:]=np.log(y[-2:]);return a

def ff(a,k):
 y=decode(a);th=-y[0];w=y[1:5];Z=y[-2:];H=ob.nodes-th;wv=ob.V@w;p=ob.N*H/(ob.d*ob.fv);pp=H*ob.fv/ob.d;M=ob.V.T@(p[:,None]*ob.V);Mp=ob.V.T@(pp[:,None]*ob.V)
 dg=np.linalg.solve(Mp,-ob.V.T@((H*wv/ob.d)*ob.gv));dn=ob.N**2*np.sum(H*wv/(ob.d*ob.fv**2));ratio=(ob.gv*wv+ob.fv*(ob.V@dg)-dn)/ob.N;wf=-np.linalg.solve(M,ob.V.T@(p*ob.fv*ratio**2)+4*ob.Vmu.T@(Z*ob.fm));i=np.argmin(abs(ob.nodes-(0 if th<.5 else 1)));xdot=2*ratio[i]/(1-th) if th<.5 else -2*ratio[i]/th;growth=2+2*((ob.Vmu@w)/ob.fm+(ob.Vmu@dg)/ob.gm)-2*dn/ob.N
 return np.r_[xdot,w+wf-k*(D@(y-eq))[1:5],growth]
mesh=np.linspace(0,1,101);amp0=1e-4;yorig=np.column_stack([eq+amp0*(VR*np.cos(2*np.pi*t)-VI*np.sin(2*np.pi*t)) for t in mesh]);ys=np.column_stack([encode(y) for y in yorig.T]);pp=np.array([2*np.pi/evh[ih].imag,kh]);oldamp=amp0
for amp in [1e-4,3e-4,.001,.003,.01,.03,.06,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6]:
 if amp!=oldamp:
  orig=np.column_stack([decode(ys[:,j]) for j in range(ys.shape[1])]);orig=eq[:,None]+amp/oldamp*(orig-eq[:,None]);
  if np.all((orig[0]<0)&(orig[0]>-1)) and np.all(orig[-2:]>0):ys=np.column_stack([encode(y) for y in orig.T])
 def fun(t,a,par):return par[0]*np.column_stack([ff(a[:,j],par[1]) for j in range(a.shape[1])])
 def bc(a,b,par):cc=CC@(decode(a)-eq);return np.r_[a-b,cc[1],cc[0]-amp]
 try:
  sol=solve_bvp(fun,bc,mesh,ys,p=pp,max_nodes=6000,tol=2e-5)
  orig=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);print('amp',amp,'status',sol.status,'params',sol.p,'res',max(sol.rms_residuals),'theta',-orig[0].max(),-orig[0].min(),flush=True)
  np.savez('workspace/agent2_facehopf_'+str(amp)+'.npz',x=sol.x,a=sol.y,y=orig,p=sol.p,D=D,B=BB,eq=eq)
  if sol.status!=0:break
  mesh=np.linspace(0,1,max(201,min(801,len(sol.x))));ys=sol.sol(mesh);pp=sol.p;oldamp=amp
 except Exception as e:print('FAILED',amp,type(e),e);break
Path('workspace/agent2_facehopf.py').write_text(Path('scratchpad.py').read_text())
