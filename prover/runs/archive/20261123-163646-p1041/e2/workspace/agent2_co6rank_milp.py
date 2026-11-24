import numpy as np,itertools,math,json,time
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from pathlib import Path

def partitions(n,k,lo=1):
 if not k:
  if not n:yield ()
  return
 for x in range(lo,n//k+1):
  for rest in partitions(n-x,k-1,x):yield(x,)+rest
results=[]
for ns in partitions(14,4):
 if ns in [(1,1,1,11),(1,1,2,10),(1,1,3,9),(1,1,4,8),(1,1,5,7),(1,1,6,6),(1,2,2,9)]:continue
 points=list(itertools.product(*[range(n+1) for n in ns]));index={a:i for i,a in enumerate(points)};N=len(points);weights=[math.prod(math.comb(n,b) for n,b in zip(ns,a)) for a in points]
 rows=[];low=[];upp=[];lb=[0.]*N;ub=[0. if w>156 else 1. for w in weights]
 for a in [(0,0,0,0)]+[tuple(int(i==j) for i in range(4)) for j in range(4)]:lb[index[a]]=1
 for a in points:
  if sum(a)>8:
   subs=list(itertools.product(*[[b for b in range(x+1) if b&x==b] for x in a]));aux=len(lb);lb.append(0.);ub.append(float(len(subs)//2));row={index[b]:1. for b in subs};row[aux]=-2.;rows.append(row);low.append(0);upp.append(0)
 rows.append(dict(enumerate(weights)));low.append(64);upp.append(156)
 A=lil_matrix((len(rows),len(lb)),dtype=float)
 for i,row in enumerate(rows):
  for j,v in row.items():A[i,j]=v
 c=np.zeros(len(lb));c[:N]=weights;t0=time.time()
 res=milp(c,integrality=np.ones(len(lb)),bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),low,upp),options={'time_limit':15,'mip_rel_gap':0})
 results.append((ns,int(res.status),str(res.message),time.time()-t0));print(results[-1],flush=True)
 if res.x is not None:
  vals=np.rint(res.x).astype(int);assert np.max(abs(res.x-vals))<1e-4
  assert all(l-1e-5<=sum(v*vals[j] for j,v in row.items())<=u+1e-5 for row,l,u in zip(rows,low,upp))
  active={a for a in points if vals[index[a]]};S=[]
  for x in range(1<<14):
   a=[];off=0
   for n in ns:a.append(((x>>off)&((1<<n)-1)).bit_count());off+=n
   if tuple(a) in active:S.append(x)
  assert len(S)<=156;assert 0 in S and all(1<<i in S for i in range(14))
  ss=set(S);f=[int(x in ss) for x in range(1<<14)]
  for i in range(14):
   for x in range(1<<14):
    if x>>i&1:f[x]^=f[x^(1<<i)]
  assert max(x.bit_count() for x,v in enumerate(f) if v)<=8
  json.dump({'ns':ns,'support':S},open('workspace/agent2_co6rank_milp_HIT.json','w'));print('VERIFIED HIT',len(S),flush=True);break
json.dump(results,open('workspace/agent2_co6rank_milp_results.json','w'))
Path('workspace/agent2_co6rank_milp.py').write_text(Path(__file__).read_text())
