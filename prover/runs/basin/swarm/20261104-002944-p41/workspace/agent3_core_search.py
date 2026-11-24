import z3,itertools,time,json
from math import comb

def search(n,seconds=300):
 ts=list(itertools.combinations(range(n),3));fs=list(itertools.combinations(range(n),4));es=list(itertools.combinations(range(n),2));N=len(ts);m=comb(n,2)-n+1
 S={t:z3.Bool('s'+str(t)) for t in ts};X={f:z3.Bool('x'+str(f)) for f in fs};R={t:z3.Int('r'+str(t)) for t in ts}
 s=z3.Solver();s.set(timeout=seconds*1000)
 for t in ts:s.add(R[t]>=0,z3.Or(R[t]<m,R[t]==N),z3.Implies(R[t]<N,S[t]))
 s.add(z3.Sum([z3.If(R[t]<N,1,0) for t in ts])==m)
 for a,b in itertools.combinations(ts,2):s.add(z3.Or(R[a]==N,R[b]==N,R[a]!=R[b]))
 H={}
 for q in [1,2]:
  for h in itertools.combinations(range(n),q):
   rr=[R[t] for t in ts if set(h)<=set(t)];hh=z3.Int('h'+str(h));H[h]=hh
   s.add(hh>=0,hh<N,z3.Or([hh==r for r in rr]));s.add([hh<=r for r in rr])
 s.add(R[(0,1,2)]==0,R[(0,1,3)]==1)
 for v in range(3,n-1):s.add(H[(v,)]<H[(v+1,)])
 for t in ts:
  ed=list(itertools.combinations(t,2));cnt=z3.Sum([z3.If(H[e]<R[t],1,0) for e in ed])
  s.add(z3.Implies(R[t]<N,z3.Or(R[t]==0,z3.And(cnt>=1,cnt<=2))))
  for v in t:s.add(z3.Implies(z3.And(R[t]<N,H[(v,)]<R[t]),z3.Or([H[e]<R[t] for e in ed if v in e])))
 s.add(z3.Or([z3.Not(S[t]) for t in ts]))
 for f in fs:
  tt=list(itertools.combinations(f,3));rr=[S[t] for t in tt];s.add(X[f]==z3.And(rr))
  for i in range(4):s.add(z3.Or(rr[i],*[z3.Not(rr[j]) for j in range(4) if j!=i]))
 for t in ts:s.add(z3.Implies(S[t],z3.Or([X[tuple(sorted((*t,v)))] for v in range(n) if v not in t])))
 tm=time.time();a=s.check();print(n,a,time.time()-tm,flush=True)
 if a==z3.sat:
  mo=s.model();fac=[f for f in fs if z3.is_true(mo.eval(X[f]))];tri=[t for t in ts if z3.is_true(mo.eval(S[t]))]
  core=sorted([t for t in ts if mo.eval(R[t]).as_long()<N],key=lambda t:mo.eval(R[t]).as_long())
  print('facets',len(fac),'triangles',len(tri),'core',core,flush=True)
  json.dump({'n':n,'facets':fac,'triangles':tri,'core':core},open('workspace/agent3_corecandidate'+str(n)+'.json','w'))
 return a
if __name__=='__main__':
 search(9,300)
