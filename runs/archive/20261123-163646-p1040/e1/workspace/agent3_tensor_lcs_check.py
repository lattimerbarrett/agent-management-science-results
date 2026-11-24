"""Exact lower-central-series subspaces in finite mod3 tensor action.
Prerequisites: run agent3_tensor_seeds.py and agent4_tensor_operators_full.py.
This calculation finds NO degree6 Johnson-kernel detection in this finite image.
"""
from sage.all import *
from scipy.sparse import load_npz
import numpy as np,time,os
from agent3_tensor_commutators import commutator_seed
fun,args=matrix(GF(3),[[1]]).__reduce__()
def fastmat(A):
 a=list(args);a[1]=MatrixSpace(GF(3),*A.shape);a[4]=(1,True,A.astype(np.uint8,copy=False).tobytes());return fun(*a)
def asnumpy(M):return np.frombuffer(M.__reduce__()[1][4][2],dtype=np.uint8).reshape(M.nrows(),M.ncols())
def echelon(A):
 M=fastmat(A);M.echelonize();return asnumpy(M[:M.rank(),:])
if not os.path.exists('workspace/agent3_gamma4_tensor_seedmatrix.npy'):
 F=np.load('workspace/agent3_gamma3_tensor_seeds.npz')['seeds'].reshape(729,-1)
 F=np.unique(F,axis=0);F=F[np.any(F,axis=1)];rows=[]
 for j in range(9):
  N=load_npz(f'workspace/agent4_tensor_N_{j}.npz');H=(F+(N@F.T).T)%3
  for f,h in zip(F,H):
   r=commutator_seed(f,h,j).reshape(-1)
   if r.any():rows.append(r)
 A=np.unique(np.array(rows,dtype=np.uint8),axis=0)
 np.save('workspace/agent3_gamma4_tensor_seedmatrix.npy',A)
B=echelon(np.load('workspace/agent3_gamma4_tensor_seedmatrix.npy'))
assert len(B)==3338
ix=np.array([i*9801+j for i in range(3) for j in range(81,9801)])
Ns=[load_npz(f'workspace/agent4_tensor_N_{j}.npz')[ix,:][:,ix] for j in range(9)]
# Exact invariant-subspace check, proving seeds span full normal closure.
for j,N in enumerate(Ns):
 C=((N@B.T).T%3).astype(np.uint8)
 D=echelon(np.vstack((B,C)))
 assert len(D)==len(B)
 B=D;print('gamma4 invariance checked',j,flush=True)
np.save('workspace/agent3_gamma4_tensor_closed.npy',B)
expected={5:(3217,297),6:(2920,805),7:(2115,2115)}
for c in (5,6,7):
 S=np.empty((0,B.shape[1]),dtype=np.uint8)
 for N in Ns:
  C=((N@B.T).T%3).astype(np.uint8)
  S=echelon(np.vstack((S,C)))
 B=S;np.save(f'workspace/agent3_gamma{c}_tensor_exact.npy',B)
 starts=[(3**k-1)//2 for k in range(10)]
 cols=[i*9720+j for i in range(3) for j in range(starts[c+1]-starts[5],starts[c+2]-starts[5])]
 ranklead=fastmat(B[:,cols]).rank()
 assert (len(B),ranklead)==expected[c]
 print('gamma',c,'dimension',len(B),'leading rank',ranklead,flush=True)
print('No degree6 extra direction in this finite image:',2920-805,'=',2115)
