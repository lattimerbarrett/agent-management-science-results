import numpy as np
from scipy.optimize import linprog
import pickle,sys
sys.path.insert(0,'workspace')
from agent4_flags6 import build
from agent1_type4flags6 import build as build4

def solve(a=169/1875,b=913/1875-1/10000,maxiter=1000):
 gs,C0,C1,Ms=build();Ms+=list(build4())
 C=C0*np.array([b]*120+[a]*120)[:,None]-C1
 cuts=[r for r in C];meta=[('book',i) for i in range(len(C))]
 Mints=[np.rint(M*720).astype(np.int64) for M in Ms]
 for it in range(maxiter):
  mat=np.column_stack([-np.array(cuts),-np.ones(len(cuts))])
  sol=linprog(np.r_[np.zeros(len(gs)),1],A_ub=mat,b_ub=np.zeros(len(cuts)),A_eq=[np.r_[np.ones(len(gs)),0]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
  if not sol.success:print('LPERROR',sol.message,flush=True);break
  if it%10==0:print('iter',it,'delta',sol.fun,'cuts',len(cuts),flush=True)
  if sol.fun>1e-8:
   out=dict(a=a,b=b,cuts=np.array(cuts),meta=meta,x=sol.x,duals=-sol.ineqlin.marginals,Mints=Mints)
   Path('workspace/agent1_certificate_candidate.pkl').write_bytes(pickle.dumps(out))
   print('POSITIVE GAP',it,sol.fun,flush=True);return out
  worst=0;added=0
  for mi,M in enumerate(Ms):
   mm=np.einsum('ijk,k->ij',M,sol.x[:-1]);ev,vs=np.linalg.eigh((mm+mm.T)/2);worst=min(worst,ev[0])
   for j,e in enumerate(ev):
    if e< -1e-8:
     v=np.rint(vs[:,j]*1000000).astype(np.int64)
     coef=np.einsum('i,j,ijk->k',v.astype(float),v.astype(float),Mints[mi])/(720*1e12)
     cuts.append(coef);meta.append(('psd',mi,v));added+=1
  if not added:
   print('PSD FEASIBLE',it,'worst',worst,flush=True)
   np.savez('workspace/agent1_flags6_feasible.npz',a=a,b=b,x=sol.x[:-1]);return None
 print('MAXITER',flush=True)
if __name__=='__main__':solve()
