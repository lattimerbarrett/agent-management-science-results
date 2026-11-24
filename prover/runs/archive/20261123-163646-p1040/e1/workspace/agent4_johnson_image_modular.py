import time,pickle
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict
from sage.all import matrix,ZZ

def add(*Ps):
 out=defaultdict(int)
 for P in Ps:
  for w,c in P.items():out[w]+=int(c)
 return {w:c for w,c in out.items() if c}
def scale(P,c):return {w:int(c)*v for w,v in P.items() if c*v}
def mul(P,Q):
 out=defaultdict(int)
 for u,c in P.items():
  for v,d in Q.items():out[u+v]+=c*d
 return {w:c for w,c in out.items() if c}
def br(P,Q):return add(mul(P,Q),scale(mul(Q,P),-1))
X=[{(i,):1} for i in range(3)]
def lyndon(w):return all(w<w[k:]+w[:k] for k in range(1,len(w)))
LW={d:[w for w in product(range(3),repeat=d) if lyndon(w)] for d in range(1,8)}
LP={}
for d in range(1,8):
 for w in LW[d]:
  if d==1:LP[w]={w:1}
  else:
   k=next(k for k in range(1,d) if w[k:] in LP)
   assert w[:k] in LP
   LP[w]=br(LP[w[:k]],LP[w[k:]])
  assert min(LP[w])==w and LP[w][w]==1

def coords(P,d):
 P=dict(P);out=[]
 for w in LW[d]:
  c=P.get(w,0);out.append(c)
  if c:
   for u,e in LP[w].items():
    v=P.get(u,0)-c*e
    if v:P[u]=v
    else:P.pop(u,None)
 assert not P,P
 return out
def fromcoords(v,d):
 return tuple(add(*(scale(LP[w],int(c)) for w,c in zip(LW[d],v[i*len(LW[d]):(i+1)*len(LW[d])]) if c)) for i in range(3))

def bracket_e(D,e):
 p,q,r=e;out=[]
 for i,Di in enumerate(D):
  val=defaultdict(int)
  if i==p:
   for w,c in add(br(D[q],X[r]),br(X[q],D[r])).items():val[w]+=c
  for w,c in Di.items():
   for k,t in enumerate(w):
    if t==p:
     val[w[:k]+(q,r)+w[k+1:]]-=c
     val[w[:k]+(r,q)+w[k+1:]]+=c
  out.append({w:c for w,c in val.items() if c})
 return tuple(out)
E=[(i,j,k) for i in range(3) for j,k in combinations(range(3),2)]
with open('workspace/agent4_johnson_image_degree5.pickle','rb') as f:B=pickle.load(f)['basis']
results={}
for c in range(6,7):
 t=time.time()
 if c>1:
  Ds=[fromcoords(list(v),c) for v in B.rows()]
  rows=[]
  for D in Ds:
   for e in E:
    T=bracket_e(D,e)
    rows.append(sum((coords(P,c+1) for P in T),[]))
  A=matrix(ZZ,rows)
  print('built',c,A.dimensions(),'seconds',round(time.time()-t,2),flush=True)
  with open('workspace/agent4_johnson_image_degree6_generators.pickle','wb') as f:pickle.dump({'generators':A,'lyndon_words':LW[7]},f)
  from sage.all import GF
  for p in [2,3,5,101]:print('degree6 rank mod',p,A.change_ring(GF(p)).rank(),flush=True)
  Path('workspace/agent4_johnson_image_modular.py').write_text(Path('scratchpad.py').read_text())
  raise SystemExit(0)
 ed=B.elementary_divisors()
 counts={int(x):list(ed).count(x) for x in set(ed)}
 print('degree',c,'rank',B.nrows(),'ambient',B.ncols(),'SNF',counts,'seconds',round(time.time()-t,2),flush=True)
 results[c]={'basis':B,'lyndon_words':LW[c+1],'smith':ed}
 with open(f'workspace/agent4_johnson_image_degree{c}.pickle','wb') as f:pickle.dump(results[c],f)
with open('workspace/agent4_johnson_image_all.pickle','wb') as f:pickle.dump(results,f)
Path('workspace/agent4_johnson_image.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/agent4_johnson_image.py')")[0])