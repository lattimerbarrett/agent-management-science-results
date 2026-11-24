import itertools,json,os
# Save reproducible source alongside machine-check results.
with open('workspace/agent4_checks.py','w') as _out:
 _out.write(open(__file__).read())

def check(t):
 k=2*t
 cores=[]; pos=0
 for i in range(t):
  d=t-1-i
  cores.append(tuple(range(pos,pos+k-d)));pos+=k-d
 classes=[]
 for i in range(t):
  cls=[]
  for petal in itertools.product(*cores[i+1:]):
   F=frozenset(cores[i]+petal)
   assert len(F)==k
   cls.append(F)
  classes.append(cls)
 fam=sum(classes,[])
 assert len(set(fam))==len(fam)
 assert all(F&G for x,F in enumerate(fam) for G in fam[x:])
 assert all(all(set(cores[i])<=F for F in classes[i]) for i in range(t))
 # Any smaller cover extends to t-1, so exhaustive checking this level suffices.
 for C in itertools.combinations(range(pos),t-1):
  S=set(C)
  assert any(not(S&F) for F in fam)
 C={c[0] for c in cores}
 assert all(C&F for F in fam)
 return dict(t=t,k=k,n=pos,m=len(fam),b=sum(k-len(c) for c in cores),tau=t,checked_noncovers=__import__('math').comb(pos,t-1))
results=[check(t) for t in range(2,5)]
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent4_tournament_checks.json','w') as f:json.dump(results,f,indent=2)
print(results)
# Search for counterexamples to quadratic construction at t=4, bounded universe.
import z3
search=[]
for ds in [(0,1,1,3),(0,1,2,2),(1,1,1,2)]:
 for extras in [0,2]:
  t=4;k=4;pos=0;cores=[]
  for d in ds:
   cores.append(frozenset(range(pos,pos+k-d)));pos+=k-d
  n=pos+extras
  candidates=[]; owners=[]
  for i,d in enumerate(ds):
   for R in itertools.combinations(set(range(n))-cores[i],d):
    candidates.append(cores[i]|frozenset(R));owners.append(i)
  vs=[z3.Bool('v%d'%j) for j in range(len(candidates))]
  sol=z3.Solver();sol.set(timeout=10000)
  for i in range(t):sol.add(z3.Or([v for v,o in zip(vs,owners) if o==i]))
  for a,F in enumerate(candidates):
   for b in range(a):
    if owners[a]!=owners[b] and not F&candidates[b]:sol.add(z3.Or(z3.Not(vs[a]),z3.Not(vs[b])))
  for C in itertools.combinations(range(n),t-1):
   C=set(C);sol.add(z3.Or([v for v,F in zip(vs,candidates) if not C&F]))
  status=str(sol.check());search.append(dict(ds=ds,k=k,n=n,status=status,candidates=len(vs)))
print(search)
with open('workspace/agent4_sat_search.json','w') as f:json.dump(search,f,indent=2)
