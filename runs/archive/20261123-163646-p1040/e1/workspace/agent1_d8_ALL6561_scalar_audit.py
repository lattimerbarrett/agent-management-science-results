import sys,time,numpy as np,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent1_scalar_magnus_audit import WORDS,IX,M,build,comm
from scipy.sparse import load_npz
from agent3_tensor_commutators import commutator_seed
ops=build();E=np.zeros((M,3),dtype=np.int32);E[:3]=np.eye(3,dtype=np.int32)
ix=[j for j,w in enumerate(WORDS) if len(w)>=5]
F=np.load('workspace/agent3_gamma3_tensor_seeds.npz')['seeds'].reshape(729,-1)
t=time.time();count=0
for g in range(9):
 N=load_npz(f'workspace/agent4_tensor_N_{g}.npz');H=(F+(N@F.T).T)%3
 for k,(f,h) in enumerate(zip(F,H)):
  a=k//81;b=k//9%9;c=k%9
  w=comm(comm(comm((a+1,),(b+1,)),(c+1,)),(-g-1,))
  V=E.copy()
  for s in reversed(w):V=(ops[s]@V)%3
  V=(V-E)%3
  expected=commutator_seed(f,h,g).reshape(-1)
  assert not V[:120].any(),(g,k,'lowerterms')
  got=V[ix].T.reshape(-1)
  assert np.array_equal(got,expected),(g,k,'seedmismatch')
  count+=1
 print('ALL729SCALARseeds for g',g,'PASS,elapsed',time.time()-t,flush=True)
print('EXHAUSTIVEPASS',count)
json.dump({'checked':count,'all_pass':True,'seconds':time.time()-t},open('workspace/agent1_d8_ALL6561_scalar_audit.json','w'))
Path('workspace/agent1_d8_ALL6561_scalar_audit.py').write_text(Path('scratchpad.py').read_text())
