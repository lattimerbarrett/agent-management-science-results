import itertools,z3,time,json
from pathlib import Path
start=time.time();results=[]; ds=(1,2,2,2,2);t=5
Path('workspace/agent1_k_search.py').write_text(Path(__file__).read_text())
for k in [7,8]:
 for extras in [0,2]:
  pos=0;cores=[]
  for d in ds: cores.append(frozenset(range(pos,pos+k-d)));pos+=k-d
  n=pos+extras;F=[];owner=[]
  for i,d in enumerate(ds):
   for r in itertools.combinations(set(range(n))-cores[i],d): F.append(cores[i]|frozenset(r));owner.append(i)
  M=[sum(1<<x for x in f) for f in F];v=[z3.Bool('v%d'%a) for a in range(len(F))]
  s=z3.Solver();s.set(timeout=60000)
  for a in range(len(F)):
   for b in range(a):
    if owner[a]!=owner[b] and not M[a]&M[b]:s.add(z3.Or(z3.Not(v[a]),z3.Not(v[b])))
  for C in itertools.combinations(range(n),t-1):
   cm=sum(1<<x for x in C)
   s.add(z3.Or([v[a] for a,m in enumerate(M) if not m&cm]))
  status=str(s.check());res=dict(ds=ds,n=n,k=k,status=status,variables=len(F),elapsed=time.time()-start)
  if status=='sat':
   model=s.model();fam=[f for a,f in enumerate(F) if z3.is_true(model.eval(v[a]))]
   assert all(a&b for a in fam for b in fam)
   assert all(any(not(set(c)&f) for f in fam) for c in itertools.combinations(range(n),t-1))
   res['family']=[sorted(f) for f in fam]
  results.append(res);print({a:b for a,b in res.items() if a!='family'},flush=True)
  Path('workspace/agent1_k_search.json').write_text(json.dumps(results))