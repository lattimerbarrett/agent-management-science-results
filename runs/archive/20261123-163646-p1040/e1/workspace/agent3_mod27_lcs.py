from sage.all import *
from scipy.sparse import load_npz
import sys,numpy as np,time,gc,json,os
sys.path.insert(0,'workspace')
from agent3_howell9 import fastmat,tonumpy,module9
from agent3_howell27 import normalize27
ix=np.array([i*9801+j for i in range(3) for j in range(81,9801)])
Ns=[load_npz(f'workspace/agent3_mod27_tensor_N_{j}.npz')[ix,:][:,ix] for j in range(9)]
def smallmodule9(A):
 A=np.asarray(A,dtype=np.int16)%9;U=[]
 while True:
  nz=np.argwhere(A%3)
  if not len(nz):break
  row,col=map(int,nz[0]);u=A[row].copy();u=u*pow(int(u[col]),-1,9)%9
  U.append(u)
  # Clear this unit column from all generators, in memory-limited blocks.
  for start in range(0,len(A),128):
   V=A[start:start+128];V[:]=(V-V[:,col,None]*u[None,:])%9
 assert not (A%3).any()
 A//=3;E=[]
 while True:
  nz=np.argwhere(A)
  if not len(nz):break
  row,col=map(int,nz[0]);e=A[row].copy()*pow(int(A[row,col]),-1,3)%3;E.append(e)
  for start in range(0,len(A),128):
   V=A[start:start+128];V[:]=(V-V[:,col,None]*e[None,:])%3
 # New unit rows may have entries at earlier chosen unit columns? cleared by
 # construction, so all pivot columns remain independent; row generators exact.
 out=np.array(U+[3*e for e in E],dtype=np.uint8)
 if not len(out):out=np.empty((0,A.shape[1]),dtype=np.uint8)
 return out,(len(U),len(E))
def next_module(B,c):
 t=time.time();B3=np.load(f'workspace/agent3_gamma{c}_tensor_exact.npy')
 P=list(fastmat(B3).pivots());r=len(P);del B3
 chunks=[];coeffparts=[]
 for j,N in enumerate(Ns):
  C=((N@B.T).T%27).astype(np.uint8)
  fn=f"workspace/agent3_mod27_tmp_chunk{j}.npy";np.save(fn,C);chunks.append(fn);coeffparts.append(C[:,P]%3)
 del C
 coeff=np.vstack(coeffparts);del coeffparts
 Q=fastmat(coeff.T);rows=list(Q.pivots());del Q,coeff;gc.collect()
 assert len(rows)==r
 mmapchunks=[np.load(fn,mmap_mode="r") for fn in chunks]
 C=np.vstack([mmapchunks[k//len(B)][k%len(B)] for k in rows]);del mmapchunks
 U,Pu=normalize27(C);del C
 Pu=list(fastmat(U%3).pivots());assert np.array_equal(U[:,Pu],np.eye(r,dtype=np.uint8))
 U9=fastmat(U,27);E=np.empty((0,B.shape[1]),dtype=np.uint8)
 print('gamma',c,'unitrank',r,'selected','elapsed',time.time()-t,flush=True)
 for j,filename in enumerate(chunks):
  C=np.load(filename)
  R9=fastmat(C,27)-fastmat(C[:,Pu],27)*U9
  R=tonumpy(R9);assert not (R%3).any()
  E,invE=smallmodule9(np.vstack((E,R//3)));del R9,R;gc.collect();s=invE
  print('gamma',c,'chunk',j,'extra3rank',s,'elapsed',time.time()-t,flush=True)
 out=np.vstack((U,3*E));return out,(r,)+invE
if __name__=='__main__':
 B=np.load('workspace/agent3_mod27_gamma4_tensor_basis.npy')
 for c in (5,6,7):
  filename=f'workspace/agent3_mod27_gamma{c}_tensor_basis.npy'
  if os.path.exists(filename):B=np.load(filename);continue
  B,invs=next_module(B,c)
  np.save(filename,B)
  open(f'workspace/agent3_mod27_gamma{c}_invariants.json','w').write(json.dumps(list(invs)))
  print('FINAL GAMMA',c,'Z9 invariants',invs,flush=True)
