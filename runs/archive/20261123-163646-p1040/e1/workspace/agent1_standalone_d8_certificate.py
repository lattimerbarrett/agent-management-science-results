"""Direct finite-Magnus certificate: no prior seed vectors/Ad matrices used.
Requires NumPy, SciPy, Sage/libgap CVEC (helper code agent3_cvec_basis.py).
Scalar matrices are computed from nine actual IA3 generator words.
"""
import sys,time,json,numpy as np
from pathlib import Path
from scipy.sparse import coo_matrix,kron,eye
sys.path.insert(0,'workspace')
from agent1_scalar_magnus_audit import WORDS,IX,M,build,comm
from agent3_cvec_basis import CVecBasis

def actions(ops):
 ix=[j for j,w in enumerate(WORDS) if len(w)>=5]
 words=[WORDS[j] for j in ix];wi={w:j for j,w in enumerate(words)};m=len(words)
 Ns=[]
 for g in range(9):
  S=ops[g+1];Sinv=ops[-g-1][ix,:][:,ix]
  rr=[];cc=[];vals=[]
  for i in range(3):
   col=S[:,i].tocoo()
   for vv,coef in zip(col.row,col.data):
    v=WORDS[vv]
    for pos,j in enumerate(v):
     for w in words:
      if len(v)+len(w)>9:break
      u=v[:pos]+w+v[pos+1:]
      rr.append(i*m+wi[u]);cc.append(j*m+wi[w]);vals.append(int(coef))
  J=coo_matrix((np.array(vals,dtype=np.int32),(rr,cc)),shape=(3*m,3*m)).tocsr()
  A=(kron(eye(3,dtype=np.int32),Sinv,format='csr')@J-eye(3*m,dtype=np.int32)).tocsr()
  A.data%=3;A.eliminate_zeros();Ns.append(A)
 return Ns

def images(N,B,chunk=64):
 for j in range(0,len(B),chunk):
  for row in ((N@B[j:j+chunk].T).T%3).astype(np.uint8):yield row

def main():
 t=time.time();ops=build();Ns=actions(ops)
 E=np.zeros((M,3),dtype=np.int32);E[:3]=np.eye(3,dtype=np.int32)
 for g in range(1,10):assert np.array_equal((ops[g]@(ops[-g]@E))%3,E)
 B=CVecBasis(29160);nseeds=0
 for a in range(1,10):
  for b in range(1,10):
   for c in range(1,10):
    for g in range(1,10):
     w=comm(comm(comm((a,),(b,)),(c,)),(-g,))
     V=E.copy()
     for s in reversed(w):V=(ops[s]@V)%3
     V=(V-E)%3
     assert not V[:120].any()
     B.insert(V[120:].T.reshape(-1));nseeds+=1
  print('seeds processed',nseeds,'rank',B.info()[0],flush=True)
 r4=B.info()[0];A,piv=B.numpy('workspace/agent1_direct_d8_L4.packed')
 for g,N in enumerate(Ns):
  for row in images(N,A):assert not B.insert(row),('L4invariance',g)
  print('L4invariance',g,'PASS',flush=True)
 S=CVecBasis(29160)
 for g,N in enumerate(Ns):
  for row in images(N,A):S.insert(row)
  print('L5generator block',g,'rank',S.info()[0],flush=True)
 r5=S.info()[0];C,piv=S.numpy('workspace/agent1_direct_d8_L5.packed')
 for g,N in enumerate(Ns):
  for row in images(N,C):assert not S.insert(row),('L5invariance',g)
  print('L5invariance',g,'PASS',flush=True)
 out={'gamma4_dimension':r4,'gamma5_dimension':r5,'quotient_dimension':r4-r5,'actual_simple_commutators_checked':nseeds,'seconds':time.time()-t,'all_invariance_checks':True}
 json.dump(out,open('workspace/agent1_direct_d8_certificate.json','w'))
 print(out,flush=True)
 return out
if __name__=='__main__':main()
