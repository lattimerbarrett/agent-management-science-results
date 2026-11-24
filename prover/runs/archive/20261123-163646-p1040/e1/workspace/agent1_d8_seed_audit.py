import sys,time,json
import numpy as np
sys.path.insert(0,'workspace')
from agent3_cvec_basis import CVecBasis
from scipy.sparse import load_npz
from agent3_tensor_commutators import commutator_seed

def select():
 B=CVecBasis(29160);t=time.time()
 L5=np.load('workspace/agent3_independent_gamma5_cvec.npy')
 for row in L5:B.insert(row)
 print('initial',B.info()[0],time.time()-t,flush=True)
 A=np.load('workspace/agent3_gamma4_tensor_seedmatrix.npy');sel=[]
 for j,row in enumerate(A):
  if B.insert(row):sel.append(j)
 print('accepted',len(sel),time.time()-t,flush=True)
 json.dump(sel,open('workspace/agent1_d8_121_seed_indices.json','w'))
 # Recover each selected seed's provenance in actual729tripleactions.
 wanted={A[j].tobytes():j for j in sel};found={}
 F0=np.load('workspace/agent3_gamma3_tensor_seeds.npz')['seeds'].reshape(729,-1)
 for g in range(9):
  N=load_npz(f'workspace/agent4_tensor_N_{g}.npz');H=(F0+(N@F0.T).T)%3
  for k,(f,h) in enumerate(zip(F0,H)):
   row=commutator_seed(f,h,g).reshape(-1).astype(np.uint8)
   key=row.tobytes()
   if key in wanted:found[wanted[key]]=[k,g]
 print('provenance',len(found),time.time()-t,flush=True)
 assert len(found)==121
 json.dump(found,open('workspace/agent1_d8_121_seed_provenance.json','w'))
 return found
if __name__=='__main__':select()
