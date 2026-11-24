import sys,pickle,numpy as np,sympy as S
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_flags6 import build
from agent1_type4flags6 import build as b4
import networkx as nx
from itertools import combinations
D=pickle.loads(Path('workspace/agent1_extremal_vectors7_exact.pkl').read_bytes());x7=np.array(D['tripartite_num'],dtype=object)
F=np.load('workspace/agent3_flags7.npz');x6=np.rint(F['L6']*7).astype(np.int64).astype(object)@x7
M6=build()[3]
pairs=list(combinations(range(4),2));reps=[];seen=[]
for typ in range(64):
 g=nx.Graph();g.add_nodes_from(range(4));g.add_edges_from(p for i,p in enumerate(pairs) if (typ>>i)&1)
 if not any(nx.is_isomorphic(g,h) for h in seen):reps.append(typ);seen.append(g)
Ms=[(M,x6,720) for M in M6]+[(F['M'],x7,5040)]+[(b4()[i],x6,720) for i in reps]
def exact_psd(H):
 A=H.copy();rank=0
 while A.rows:
  ds=[A[i,i] for i in range(A.rows)]
  assert all(d>=0 for d in ds)
  if not any(ds):
   assert A==S.zeros(A.rows);return rank
  i=next(i for i,d in enumerate(ds) if d>0)
  ids=[j for j in range(A.rows) if j!=i]
  A=A.extract(ids,ids)-A.extract(ids,[i])*A.extract([i],ids)/A[i,i]
  rank+=1
 return rank
out=[]
for i,(M,x,den) in enumerate(Ms):
 H=np.rint(M*den).astype(np.int64).astype(object)@x
 H=S.Matrix(H.tolist());ns=H.nullspace();assert all(H*v==S.zeros(H.rows,1) for v in ns);assert exact_psd(H)==H.rows-len(ns);out.append(ns)
 print(i,M.shape[:2],len(ns),flush=True)
for M in np.load('workspace/agent3_type3flags7.npz')['M']:
 H=np.rint(M*1260).astype(np.int64).astype(object)@x7
 H=S.Matrix(H.tolist());ns=H.nullspace();assert all(H*v==S.zeros(H.rows,1) for v in ns);assert exact_psd(H)==H.rows-len(ns);out.append(ns)
Path('workspace/agent1_all_exact_nullspaces7.pkl').write_bytes(pickle.dumps(out))
print('all',len(out))
