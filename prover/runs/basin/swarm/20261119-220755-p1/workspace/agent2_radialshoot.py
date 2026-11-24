import sys;sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from pathlib import Path
z=np.load('workspace/agent2_positive_eq.npz');ob=BlowupODE(z['base'],z['f'],z['g'],float(z['N']),z['mus']);y=z['y'];J=z['J'];ev,evec=np.linalg.eig(J)
ics=[j for j,a in enumerate(ev) if a.imag>1e-3];irs=[np.argmin(abs(ev-a)) for a in [-1,1,2]]
cols=[]
for j in ics:cols.extend([evec[:,j].real,evec[:,j].imag])
cols.extend([evec[:,j].real for j in irs]);B=np.column_stack([v/np.linalg.norm(v) for v in cols]);BI=np.linalg.inv(B);rad=B[:,5:7];left=BI[5:7];eps=.001
v=B[:,0]
def event(t,yy):return min(-yy[0]+1e-8,yy[0]+1+1e-8,1e5-np.linalg.norm(yy))
event.terminal=True

def integrate(ab,T):
 ini=y+eps*v+eps**2*(rad@ab)
 return solve_ivp(lambda t,yy:ob(t,yy,True),(0,T),ini,rtol=2e-9,atol=2e-11,events=event,max_step=.1)

ab=np.zeros(2)
for T in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
 def fun(par):
  try:
   sol=integrate(par,T);tt=sol.t[-1];return (left@(sol.y[:,-1]-y))*np.exp(-np.array([1,2])*tt)/eps**2
  except Exception:return np.array([1e8,1e8])
 rr=root(fun,ab,options={'eps':1e-4,'xtol':1e-7,'maxfev':80});ab=rr.x;sol=integrate(ab,T);theta=-sol.y[0]
 print('T',T,'ok',rr.success,'res',fun(ab),'ab',ab,'tend',sol.t[-1],'theta',min(theta),max(theta),'Z',sol.y[-2:,-1],flush=True)
 np.savez('workspace/agent2_radialshoot_T'+str(T)+'.npz',ab=ab,t=sol.t,yy=sol.y,eq=y,B=B,eps=eps)
 if sol.t[-1]<T-.001:break
Path('workspace/agent2_radialshoot.py').write_text(Path('scratchpad.py').read_text())
