import itertools,z3,time,json
start=time.time();cores=[set(range(3)),{3,4},{5,6},{7,8}];n=9;t=4
res=[]
for k in (4,5):
 d=[k-len(X) for X in cores]
 fam=[];owners=[]
 for i,X in enumerate(cores):
  for size in range(max(t,len(X)),k+1):
   for P in itertools.combinations(set(range(n))-X,size-len(X)):
    E=X|set(P)
    if not any(E==F for F in fam):fam.append(E);owners.append(i)
 vs=[z3.Bool('x%d'%i) for i in range(len(fam))];s=z3.Solver();s.set(timeout=60000)
 C={0,1,3,5}
 for i,E in enumerate(fam):
  if not E&C:s.add(z3.Not(vs[i]))
  disjoint=[j for j,F in enumerate(fam) if not E&F]
  s.add(z3.Or(vs[i],*[vs[j] for j in disjoint]))
  for j in disjoint:
   if j<i:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
 for c in itertools.combinations(range(n),t-1):s.add(z3.Or([vs[i] for i,E in enumerate(fam) if not E&set(c)]))
 # All classes must occur, assigning an edge containing multiple cores to first eligible owner does not suffice; here disjoint cores total>=5 for every pair except cores2+2=4.
 for X in cores:s.add(z3.Or([vs[i] for i,E in enumerate(fam) if X<=E]))
 status=s.check();item=dict(k=k,n=n,cores=[sorted(X) for X in cores],cover=sorted(C),candidate_count=len(fam),status=str(status))
 if status==z3.sat:
  m=s.model();H=[E for i,E in enumerate(fam) if z3.is_true(m.eval(vs[i]))]
  assert all(E&F for E in H for F in H)
  assert all(any(not E&set(c) for E in H) for c in itertools.combinations(range(n),3))
  assert all(E&C for E in H)
  assert all(any(not E&F for E in H) or F in H for F in fam)
  item['family']=[sorted(E) for E in H]
 res.append(item);print(item,flush=True)
with open('workspace/agent4_partial_cover_saturation.json','w') as f:json.dump(res,f,indent=2)
with open('workspace/agent4_partial_cover_saturation.py','w') as f:f.write(open(__file__).read())
print('runtime',time.time()-start)
