import sys,json,time
from pathlib import Path
from itertools import product
from collections import defaultdict
import numpy as np
from scipy.sparse import coo_matrix,eye,load_npz
sys.path.insert(0,'workspace')
from agent3_magnus import K,C,magnus,reduce_word,inverse

def cw(u,v):return reduce_word(tuple(u)+tuple(v)+inverse(tuple(u))+inverse(tuple(v)))
def tw(a,b,c,g):return cw(cw(cw((a+1,),(b+1,)),(c+1,)),(-g-1,))
terms=[tw(0,8,3,1),tw(0,8,3,4),tw(4,3,8,0),inverse(tw(4,7,8,3))]
W=reduce_word(sum(terms,()))
print('candidate formalword length',len(W),'word',W,flush=True)
G=[]
for i in range(1,4):
 for j in range(1,4):
  if i!=j:G.append(K(3,i,j))
 other=[j for j in range(1,4) if j!=i];G.append(C(3,i,*other))
D=5;words=[w for d in range(1,D+1) for w in product(range(3),repeat=d)];ix={w:i for i,w in enumerate(words)};n=len(words)
def mul(P,Q):
 out=defaultdict(int)
 for u,c in P.items():
  for v,e in Q.items():
   if len(u)+len(v)<=D:out[u+v]+=c*e
 return {w:c for w,c in out.items() if c}
def S(g):
 P=[]
 for w in g:
  pp=magnus(w,D);pp.pop((),None);P.append({tuple(i-1 for i in u):int(c) for u,c in pp.items()})
 cache={():{():1}};rr=[];cc=[];vv=[]
 for w in words:
  q=mul(cache[w[:-1]],P[w[-1]]);cache[w]=q
  for u,c in q.items():rr.append(ix[u]);cc.append(ix[w]);vv.append(c)
 return coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(n,n)).tocsr()
Ops={}
for k,(g,gi) in enumerate(G):
 Ops[k+1]=S(g);Ops[-k-1]=S(gi)
 assert (Ops[k+1]@Ops[-k-1]-eye(n,dtype=np.int64)).nnz==0
assert max(int(abs(O).sum(axis=1).max()) for O in Ops.values())<=12 # 12*2^50 <2^63, nooverflow
v=np.zeros((n,3),dtype=np.int64);v[:3,:]=np.eye(3,dtype=np.int64);base=v.copy()
for a in reversed(W):
 v=Ops[a]@v;assert np.max(np.abs(v))<2**50
assert np.array_equal(v,base)
print('PASS actualINTEGERMagnusaction isIDENTITY throughwordlength5: W inA5',flush=True)
v=np.zeros((9840,3),dtype=np.int32);v[:3,:]=np.eye(3,dtype=np.int32);base=v.copy()
for a in reversed(W):v=(load_npz(f'workspace/agent1_scalar_S_{abs(a)-1}_{1 if a>0 else -1}.npz')@v)%3
v=(v-base)%3;assert not v[:120].any()
f=v[120:].T.reshape(-1)
expected=np.load('workspace/agent4_degree4_kernel_candidate_finite_vector.npy')
assert np.array_equal(f,expected)
print('PASS actualSCALARMagnusaction of88letterword matchesindependentfiniteγ4seedvector; nonzero',np.count_nonzero(f),flush=True)
Path('workspace/agent4_degree4_candidate_word.json').write_text(json.dumps(list(W)))
