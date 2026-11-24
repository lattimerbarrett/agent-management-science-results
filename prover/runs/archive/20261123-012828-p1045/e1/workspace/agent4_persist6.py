import sys,time,pickle
sys.path.insert(0,'workspace')
import numpy as np
from agent4_flags6 import build
from agent1_type4flags6 import build as build4
from agent3_highs import PersistentLP

def main(a=.09,b=.48,maxiter=1000):
 gs,C0,C1,Ms=build();extra=build4()
 if isinstance(extra,tuple):print('TYPE4TUPLE',type(extra),flush=True);return
 Ms+=list(extra)
 cap=np.array([b]*120+[a]*120);C=C0*cap[:,None]-C1
 path=f'workspace/agent4_persist_{a}_{b}.pkl'
 cuts=[];vecs=[];start=0
 try:
  d=pickle.load(open(path,'rb'));cuts=d['cuts'];vecs=d['vectors'];start=d['iteration']+1
 except FileNotFoundError:pass
 lp=PersistentLP(len(gs),list(-C)+cuts)
 lp.H.setOptionValue('solver','ipm')
 lp.H.changeColsCost(len(gs),np.arange(len(gs),dtype=np.int32),np.random.default_rng(4).uniform(-1,1,len(gs)))
 for it in range(start,maxiter):
  ok,x=lp.run()
  if not ok:
   ray=lp.ray();pickle.dump({'cuts':cuts,'vectors':vecs,'ray':ray,'iteration':it,'a':a,'b':b},open(path,'wb'))
   print('INFEASIBLE',it,'ray',ray[0],flush=True);return
  new=[];worst=0
  for mi,M in enumerate(Ms):
   mat=np.einsum('ijk,k->ij',M,x);ev,ve=np.linalg.eigh((mat+mat.T)/2);worst=min(worst,ev[0])
   for j,e in enumerate(ev):
    if e < -1e-8:
     v=ve[:,j];v=v/max(abs(v));v=np.round(v*100000)/100000
     cf=-np.einsum('i,j,ijk->k',v,v,M)
     new.append(cf);vecs.append((mi,v))
  cuts.extend(new)
  pickle.dump({'cuts':cuts,'vectors':vecs,'iteration':it,'a':a,'b':b,'x':x,'worst':worst},open(path,'wb'))
  if it%10==0:print(it,worst,len(cuts),flush=True)
  if worst>=-1e-8:print('FEASIBLE',it,worst,flush=True);return
  lp.add(new)
 print('MAXITER',it,worst,flush=True)
if __name__=='__main__':main()
