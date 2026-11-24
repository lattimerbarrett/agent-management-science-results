import sys,numpy as np,time
sys.path.insert(0,'workspace');import agent1_flip_poincare as p
from pathlib import Path
startphys=np.array([-1.0477114,.5604081,6.033125,.443492,.026175]);v=np.r_[np.arcsinh(startphys[:2]),np.log(startphys[2:])]
calls=0
def calc(v):
 global calls
 if max(abs(v))>15:return None
 phys=np.r_[np.sinh(v[:2]),np.exp(v[2:])]
 try:o=p.poincare(phys,rtol=3e-9)
 except (ValueError,np.linalg.LinAlgError,OverflowError):return None
 calls+=1
 if o is None or o[1]<=0 or min(o[0][2:])<=0:return None
 out=o[0];P=np.r_[np.arcsinh(out[:2]),np.log(out[2:])];return P-v,o
best=calc(v);print('INITIAL',np.linalg.norm(best[0]),best[0],flush=True)
for it in range(100):
 val=calc(v)
 if val is None:break
 r,o=val;norm=np.linalg.norm(r);J=np.empty((5,5));bad=False
 for j in range(5):
  ep=2e-5*(1+abs(v[j]));vv=v.copy();vv[j]+=ep;op=calc(vv);vv[j]-=2*ep;om=calc(vv)
  if op is not None and om is not None:J[:,j]=(op[0]-om[0])/(2*ep)
  elif op is not None:J[:,j]=(op[0]-r)/ep
  elif om is not None:J[:,j]=(r-om[0])/ep
  else:bad=True;break
 if bad:print('jacboundary');break
 accepted=False
 for lm in [0,1e-6,1e-4,.01,.1,1,10,100,1000]:
  step=-np.linalg.lstsq(J.T@J+lm*np.eye(5),J.T@r,rcond=None)[0]
  if np.linalg.norm(step)>3:step*=3/np.linalg.norm(step)
  for fac in [1,.5,.25,.125,.0625,.03125,.015625,.0078125]:
   vn=v+fac*step;nn=calc(vn)
   if nn is not None and np.linalg.norm(nn[0])<norm*(1-1e-4*fac):v=vn;accepted=True;break
  if accepted:break
 print('ITER',it,'norm',norm,'v',v,'scale',o[1],'time',o[2],'accepted',accepted,'calls',calls,flush=True)
 np.savez('workspace/agent4_poincare_shoot.npz',v=v,residual=calc(v)[0])
 if norm<1e-7 or not accepted:break
print('FINAL',np.r_[np.sinh(v[:2]),np.exp(v[2:])],calc(v),'calls',calls)
