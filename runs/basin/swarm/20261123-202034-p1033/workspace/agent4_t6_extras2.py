import itertools,z3,time,json,os
start=time.time();t=6;k=6;d=2;n=26
cores=[frozenset(range(4*i,4*i+4)) for i in range(t)]
F=[];owner=[];R=[]
for i in range(t):
 for r in itertools.combinations(set(range(n))-cores[i],d):
  R.append(r);F.append(cores[i]|frozenset(r));owner.append(i)
M=[sum(1<<x for x in f) for f in F]
v=[z3.Bool('v'+str(a)) for a in range(len(F))]
conf=[]
for a in range(len(F)):
 for b in range(a):
  if owner[a]!=owner[b] and not M[a]&M[b]:conf.append(z3.Or(z3.Not(v[a]),z3.Not(v[b])))
results=[]
for pattern in [(4,5),(4,8),(4,24),(24,25)]:
 s=z3.Solver();s.set(timeout=45000);s.add(conf)
 s.add(v[next(a for a,r in enumerate(R) if owner[a]==0 and r==pattern)])
 for C in itertools.combinations(range(n),t-1):
  cm=sum(1<<x for x in C)
  s.add(z3.Or([v[a] for a,m in enumerate(M) if not m&cm]))
 print('built',pattern,'variables',len(F),'elapsed',time.time()-start,flush=True)
 status=str(s.check());print(pattern,status,'elapsed',time.time()-start,flush=True)
 res={'status':status,'elapsed':time.time()-start,'first_residual':pattern}
 if status=='sat':
  model=s.model();res['family']=[sorted(f) for a,f in enumerate(F) if z3.is_true(model.eval(v[a]))]
 results.append(res)
 with open('workspace/agent4_t6_extras2.json','w') as out:json.dump(results,out)
with open('workspace/agent4_t6_extras2.py','w') as out:out.write(open(__file__).read())
