import itertools,z3,time,json
out=[]
for r,n in [(3,8),(3,9),(3,10),(4,10),(4,11)]:
 st=time.time();E=list(itertools.combinations(range(n),r));idx={e:i for i,e in enumerate(E)};vs=[z3.Bool('e%d_%d_%d'%(r,n,i)) for i in range(len(E))];s=z3.Solver();s.set(timeout=30000)
 R=set(range(n//2));S=set(range(n))-R
 for i,e in enumerate(E):
  es=set(e)
  disj=[idx[f] for f in itertools.combinations([v for v in range(n) if v not in es],r)]
  if es<=R or es<=S:
   s.add(z3.Not(vs[i]));s.add(z3.Or([vs[j] for j in disj])) # no mono rank-r mincover
  for j in disj:
   if j<i:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
 for c in itertools.combinations(range(n),r-1):
  comp=[v for v in range(n) if v not in c];s.add(z3.Or([vs[idx[f]] for f in itertools.combinations(comp,r)]))
 status=s.check();d=dict(r=r,n=n,R=sorted(R),status=str(status),seconds=time.time()-st)
 if status==z3.sat:
  m=s.model();H=[e for i,e in enumerate(E) if z3.is_true(m.eval(vs[i]))]
  assert all(set(e)&set(f) for e in H for f in H)
  assert all(any(not set(c)&set(e) for e in H) for c in itertools.combinations(range(n),r-1))
  for c in E:
   if set(c)<=R or set(c)<=S:assert any(not set(c)&set(e) for e in H)
  d['H']=H
 out.append(d);print(d,flush=True)
open('workspace/agent4_uniform_polar_propertyB.py','w').write(open(__file__).read());json.dump(out,open('workspace/agent4_uniform_polar_propertyB.json','w'))
