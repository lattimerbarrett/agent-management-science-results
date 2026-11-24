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

from collections import Counter
B=matrix.identity(ZZ,9)
for c in range(1,7):
 t=time.time()
 if c>1:
  Ds=[fromcoords(list(v),c) for v in B.rows()]
  rows=[]
  for D in Ds:
   for e in E:
    T=bracket_e(D,e)
    rows.append(sum((coords(P,c+1) for P in T),[]))
  A=matrix(ZZ,rows)
  weights=[tuple(w.count(j)-(j==i) for j in range(3)) for i in range(3) for w in LW[c+1]]
  colgroups=defaultdict(list);rowgroups=defaultdict(list)
  for j,w in enumerate(weights):colgroups[w].append(j)
  for i,row in enumerate(A.rows()):
   nz=row.nonzero_positions()
   if nz:
    wt=weights[nz[0]];assert all(weights[j]==wt for j in nz)
    rowgroups[wt].append(i)
  basis=[];ed=[]
  for wt,rs in rowgroups.items():
   cs=colgroups[wt]
   H=A.matrix_from_rows_and_columns(rs,cs).hermite_form(algorithm='flint',include_zero_rows=False)
   ed+=list(H.elementary_divisors())
   for hr in H.rows():
    row=[0]*A.ncols()
    for j,x in zip(cs,hr):row[j]=x
    basis.append(row)
  B=matrix(ZZ,basis)
 else:ed=[1]*9
 print('degree',c,'rank',B.nrows(),'ambient',B.ncols(),'Smith',Counter(map(int,ed)),'seconds',round(time.time()-t,2),flush=True)
 with open(f'workspace/agent4_johnson_full_degree{c}.pickle','wb') as f:pickle.dump({'basis':B,'lyndon_words':LW[c+1],'smith':ed},f)
