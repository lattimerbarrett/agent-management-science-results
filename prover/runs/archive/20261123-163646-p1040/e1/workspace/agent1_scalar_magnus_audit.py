import numpy as np,json,time,sys,os
from itertools import product
from collections import defaultdict
from scipy.sparse import coo_matrix,save_npz,load_npz
sys.path.insert(0,'workspace')
from agent3_magnus import K,C,magnus,inverse,product as wp
D=8
WORDS=[w for d in range(1,D+1) for w in product(range(3),repeat=d)]
IX={w:j for j,w in enumerate(WORDS)};M=len(WORDS)
def mul(P,Q):
 o=defaultdict(int)
 for w,c in P.items():
  for v,e in Q.items():
   if len(w)+len(v)<=D:o[w+v]+=c*e
 return {w:c%3 for w,c in o.items() if c%3}
def build():
 G=[]
 for i in range(1,4):
  for j in range(1,4):
   if i!=j:G.append(K(3,i,j))
  other=[j for j in range(1,4) if j!=i];G.append(C(3,i,*other))
 ops={}
 for j,pair in enumerate(G):
  for sign,im in zip([1,-1],pair):
   fname=f'workspace/agent1_scalar_S_{j}_{sign}.npz'
   if os.path.exists(fname):ops[sign*(j+1)]=load_npz(fname);continue
   polys=[]
   for w in im:
    P=magnus(w,D);P.pop((),None)
    polys.append({tuple(a-1 for a in v):c%3 for v,c in P.items() if c%3})
   cache={():{():1}};rows=[];cols=[];vals=[];t=time.time()
   for k,w in enumerate(WORDS):
    P=mul(cache[w[:-1]],polys[w[-1]]);cache[w]=P
    for v,c in P.items():rows.append(IX[v]);cols.append(k);vals.append(c)
   S=coo_matrix((np.array(vals,dtype=np.int32),(rows,cols)),shape=(M,M)).tocsr()
   save_npz(fname,S);ops[sign*(j+1)]=S
   print('built scalar',j,sign,'nnz',S.nnz,'seconds',time.time()-t,flush=True)
 return ops
def comm(u,v):return wp(u,v,inverse(u),inverse(v))
def audit():
 ops=build()
 E=np.zeros((M,3),dtype=np.int32);E[:3]=np.eye(3,dtype=np.int32)
 for j in range(1,10):assert np.array_equal((ops[j]@(ops[-j]@E))%3,E)
 source=json.load(open('workspace/agent1_d8_121_seed_provenance.json'))
 target=np.load('workspace/agent3_gamma4_tensor_seedmatrix.npy')
 ix=np.array([IX[w] for w in WORDS if len(w)>=5])
 results=[]
 for row,(k,g) in source.items():
  a=k//81;b=k//9%9;c=k%9
  w=comm(comm(comm((a+1,),(b+1,)),(c+1,)),(-g-1,))
  V=E.copy()
  for s in reversed(w):V=(ops[s]@V)%3
  V=(V-E)%3
  assert not V[:120].any()
  got=V[ix].T.reshape(-1).astype(np.uint8)
  ok=np.array_equal(got,target[int(row)])
  results.append(ok)
  if not ok:
   print('FAIL',row,k,g,'mismatches',np.count_nonzero(got!=target[int(row)]),flush=True)
   np.save('workspace/agent1_d8_failed_actual.npy',got)
   break
 print('literal scalar-matrix audit',sum(results),'of',len(results),'PASS',all(results),flush=True)
 json.dump(results,open('workspace/agent1_d8_121_scalar_checks.json','w'))
if __name__=='__main__':audit()
