import numpy as np,random,time,json,itertools
from sage.all import GF,matrix
from sage.coding.binary_code import weight_dist
from pathlib import Path
random.seed(277)
xx=np.array([[int(x>>i&1) for x in range(64)] for i in range(6)],dtype=np.uint8)
mon=[np.ones(64,dtype=np.uint8)]+[xx[i] for i in range(6)]+[xx[i]*xx[j] for i in range(6) for j in range(i)]
a=xx[0]*xx[1]*xx[2];b=xx[3]*xx[4]*xx[5]
def quad(c):
 q=np.zeros(64,dtype=np.uint8)
 for i in range(22):
  if c>>i&1:q^=mon[i]
 return q
def samplequad():
 if random.random()<.5:return random.randrange(1<<22)
 c=0
 for _ in range(random.randrange(1,8)):c^=1<<random.randrange(22)
 return c
hits=[];t0=time.time();seen=set()
for trial in range(1500):
 co=[samplequad() for _ in range(4)]
 if trial%3==0:co[2:]=co[:2]
 L=[a,b,quad(co[0]),quad(co[1])];R=[a,b,quad(co[2]),quad(co[3])]
 pl=tuple(np.bincount(sum((L[i].astype(np.int64)<<i) for i in range(4)),minlength=16));pr=tuple(np.bincount(sum((R[i].astype(np.int64)<<i) for i in range(4)),minlength=16))
 if (pl,pr) in seen:continue
 seen.add((pl,pr))
 ones=np.ones(64,dtype=np.uint8)
 rows=[np.ones(4096,dtype=np.uint8)]
 rows +=[np.outer(l,ones).reshape(-1) for l in L]
 rows +=[np.outer(ones,r).reshape(-1) for r in R]
 rows +=[np.outer(L[i],R[j]).reshape(-1) for i in range(4) for j in range(4) if i>=2 or j>=2]
 offset=(np.outer(a,a)^np.outer(b,b)).reshape(-1)
 G=matrix(GF(2),[r.tolist() for r in rows]);G=G.row_space().basis_matrix();dim=G.nrows()
 wb=weight_dist(G);Ga=G.stack(matrix(GF(2),[offset.tolist()]));wa=weight_dist(Ga)
 found=[w for w in [194,198,202,206] if wa[w]>wb[w]]
 if found:
  hit={'weights':found,'coeffs':co,'dim':dim};hits.append(hit);print('HIT',hit,flush=True);break
 if trial%10==0:print('progress',trial,'dim',dim,'elapsed',time.time()-t0,flush=True)
print('DONE',len(seen),'hits',hits,'elapsed',time.time()-t0,flush=True)
json.dump(hits,open('workspace/agent2_twisted_rank4_hits.json','w'))
Path('workspace/agent2_twisted_rank4_search.py').write_text(Path('scratchpad.py').read_text())
