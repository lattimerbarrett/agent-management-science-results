from sage.all import *
from scipy.sparse import load_npz
import sys,numpy as np,time,gc,json,os
sys.path.insert(0,'workspace')
from agent3_howell9 import fastmat,tonumpy,module9
ix=np.array([i*9801+j for i in range(3) for j in range(81,9801)])
Ns=[load_npz(f'workspace/agent3_mod9_tensor_N_{j}.npz')[ix,:][:,ix] for j in range(9)]
def next_module(B,c):
 t=time.time();B3=np.load(f'workspace/agent3_gamma{c}_tensor_exact.npy')
 P=list(fastmat(B3).pivots());r=len(P);del B3
 chunks=[((N@B.T).T%9).astype(np.uint8) for N in Ns]
 coeff=np.vstack([C[:,P]%3 for C in chunks])
 Q=fastmat(coeff.T);rows=list(Q.pivots());del Q,coeff;gc.collect()
 assert len(rows)==r
 C=np.vstack([chunks[k//len(B)][k%len(B)] for k in rows])
 U,inv=module9(C,verbose=False);del C;assert inv==(r,0)
 Pu=list(fastmat(U%3).pivots());assert np.array_equal(U[:,Pu],np.eye(r,dtype=np.uint8))
 U9=fastmat(U,9);E=np.empty((0,B.shape[1]),dtype=np.uint8)
 print('gamma',c,'unitrank',r,'selected','elapsed',time.time()-t,flush=True)
 for j,C in enumerate(chunks):
  R9=fastmat(C,9)-fastmat(C[:,Pu],9)*U9
  R=tonumpy(R9);assert not (R%3).any()
  F=fastmat(np.vstack((E,R//3)));del R9,R;F.echelonize();s=F.rank();E=tonumpy(F[:s,:]);del F;gc.collect()
  print('gamma',c,'chunk',j,'extra3rank',s,'elapsed',time.time()-t,flush=True)
 out=np.vstack((U,3*E));return out,(r,len(E))
if __name__=='__main__':
 B=np.load('workspace/agent3_mod9_gamma4_tensor_basis.npy')
 for c in (5,6,7):
  filename=f'workspace/agent3_mod9_gamma{c}_tensor_basis.npy'
  if os.path.exists(filename):B=np.load(filename);continue
  B,invs=next_module(B,c)
  np.save(filename,B)
  open(f'workspace/agent3_mod9_gamma{c}_invariants.json','w').write(json.dumps(list(invs)))
  print('FINAL GAMMA',c,'Z9 invariants',invs,flush=True)
