import itertools,z3,time,json
start=time.time();results=[]
patterns=[ds for ds in itertools.combinations_with_replacement(range(5),5) if sum(ds)==9 and ds.count(0)<=1]
for ds in patterns:
 for extras in [0,2]:
  t=5;k=5;pos=0;cores=[]
  for d in ds:
   cores.append(frozenset(range(pos,pos+k-d)));pos+=k-d
  n=pos+extras;F=[];owner=[]
  for i,d in enumerate(ds):
   for r in itertools.combinations(set(range(n))-cores[i],d):F.append(cores[i]|frozenset(r));owner.append(i)
  M=[sum(1<<x for x in f) for f in F];v=[z3.Bool('v%d'%a) for a in range(len(F))]
  s=z3.Solver();s.set(timeout=20000)
  for a in range(len(F)):
   for b in range(a):
    if owner[a]!=owner[b] and not M[a]&M[b]:s.add(z3.Or(z3.Not(v[a]),z3.Not(v[b])))
  for C in itertools.combinations(range(n),t-1):
   cm=sum(1<<x for x in C)
   s.add(z3.Or([v[a] for a,m in enumerate(M) if not m&cm]))
  status=str(s.check());res=dict(ds=ds,n=n,k=k,status=status,variables=len(F),elapsed=time.time()-start)
  if status=='sat':
   model=s.model();res['family']=[sorted(f) for a,f in enumerate(F) if z3.is_true(model.eval(v[a]))]
  results.append(res);print(res if status!='sat' else {x:y for x,y in res.items() if x!='family'},flush=True)
  with open('workspace/agent4_t5_search.json','w') as out:json.dump(results,out)
with open('workspace/agent4_t5_search.py','w') as out:out.write(open(__file__).read())
