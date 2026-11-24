import numpy as np,pickle,sympy as S
from pathlib import Path
D=pickle.loads(Path('workspace/agent1_extremal_vectors7_exact.pkl').read_bytes());x=np.array(D['tripartite_num'],dtype=object)
M=np.load('workspace/agent1_type5flags7.npz')['M'];out=[]
def exact_psd(H):
 A=H.copy();rank=0
 while A.rows:
  ds=[A[i,i] for i in range(A.rows)];assert all(d>=0 for d in ds)
  if not any(ds):assert A==S.zeros(A.rows);return rank
  i=next(i for i,d in enumerate(ds) if d>0);ids=[j for j in range(A.rows) if j!=i]
  A=A.extract(ids,ids)-A.extract(ids,[i])*A.extract([i],ids)/A[i,i];rank+=1
 return rank
for i,m in enumerate(M):
 H=S.Matrix((np.rint(m*5040).astype(np.int64).astype(object)@x).tolist());ns=H.nullspace()
 assert all(H*v==S.zeros(32,1) for v in ns)
 rank=exact_psd(H);assert rank==32-len(ns);out.append(ns)
 print(i,'rank',rank,flush=True)
Path('workspace/agent1_type5_nullspaces7.pkl').write_bytes(pickle.dumps(out))
