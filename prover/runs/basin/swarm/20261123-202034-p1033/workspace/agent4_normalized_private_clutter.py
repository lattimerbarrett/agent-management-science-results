import itertools,z3,time,json,random
import numpy as np
from scipy.optimize import linprog
start=time.time();rng=random.Random(538)
def run(r,trial):
 U=set(range(2*r-2));pairs=[]
 for A in itertools.combinations(U,r-1):
  A=set(A);B=U-A
  if tuple(sorted(A))<tuple(sorted(B)):pairs.append((A,B))
 H=[]
 for j,(A,B) in enumerate(pairs):H.extend([A|{len(U)+j},B|{len(U)+j}])
 blocks=[{i} for i in range(len(U)+len(pairs))];merges=[]
 while True:
  vertices=sorted(set.union(*H));vs={v:z3.Bool('x%d'%v) for v in vertices};s=z3.Solver()
  s.add(z3.PbLe([(x,1) for x in vs.values()],r))
  for E in H:s.add(z3.Or([vs[v] for v in E]))
  possible=list(itertools.combinations(vertices,2));rng.shuffle(possible);found=False
  for v,w in possible:
   status=s.check(vs[v],vs[w]);assert status!=z3.unknown
   if status==z3.unsat:
    H=[(E-{w})|({v} if w in E else set()) for E in H]
    H=[set(e) for e in set(frozenset(E) for E in H)];merges.append((v,w));found=True;break
  if not found:break
 vertices=sorted(set.union(*H));ren={v:i for i,v in enumerate(vertices)};H=[{ren[v] for v in E} for E in H];n=len(vertices)
 s=z3.Solver();vs=[z3.Bool('z%d'%i) for i in range(n)];s.add(z3.PbLe([(x,1) for x in vs],r-1))
 for E in H:s.add(z3.Or([vs[v] for v in E]))
 assert s.check()==z3.unsat
 B=[]
 for C in itertools.combinations(range(n),r):
  if all(set(C)&E for E in H):B.append(C)
 assert all(any(v in C and w in C for C in B) for v,w in itertools.combinations(range(n),2))
 mat=np.zeros((n,len(B)))
 for j,C in enumerate(B):mat[list(C),j]=1
 lp=linprog(np.zeros(len(B)),A_eq=mat,b_eq=np.ones(n),bounds=(0,None),method='highs')
 item=dict(r=r,trial=trial,n=n,edges=len(H),mincovers=len(B),fractional_perfect=bool(lp.success),H=[sorted(E) for E in H],B=B,merges=merges)
 print({k:v for k,v in item.items() if k not in ('H','B','merges')},'time',time.time()-start,flush=True)
 return item
res=[]
for r,trials in [(4,3),(5,5),(6,2)]:
 for trial in range(trials):
  res.append(run(r,trial))
  with open('workspace/agent4_normalized_private_clutter.json','w') as f:json.dump(res,f,indent=2)
with open('workspace/agent4_normalized_private_clutter.py','w') as f:f.write(open(__file__).read())
