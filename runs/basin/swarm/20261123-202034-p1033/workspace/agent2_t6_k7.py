import itertools,z3,time,json,os
start=time.time();t=6;k=7;d=2;c=k-d;n=t*c
cores=[frozenset(range(c*i,c*(i+1))) for i in range(t)]
F=[];owner=[];R=[];index={}
for i in range(t):
 for r in itertools.combinations(sorted(set(range(n))-cores[i]),d):
  index[i,r]=len(F);R.append(r);F.append(cores[i]|frozenset(r));owner.append(i)
M=[sum(1<<x for x in f) for f in F]
v=[z3.Bool('v'+str(a)) for a in range(len(F))]
conf=[]
for a in range(len(F)):
 for b in range(a):
  if owner[a]!=owner[b] and not M[a]&M[b]:conf.append(z3.Or(z3.Not(v[a]),z3.Not(v[b])))
print('conflicts',len(conf),'elapsed',time.time()-start,flush=True)
clauses=[]
for C in itertools.combinations(range(n),t-1):
 hit={x//c for x in C};C=set(C);inds=[]
 for i in set(range(t))-hit:
  avail=sorted(set(range(n))-cores[i]-C)
  inds.extend(index[i,r] for r in itertools.combinations(avail,2))
 clauses.append(z3.Or([v[a] for a in inds]))
print('covers',len(clauses),'elapsed',time.time()-start,flush=True)
results=[]
for pattern in [(c,c+1),(c,2*c)]:
 s=z3.Solver();s.set(timeout=90000);s.add(conf);s.add(clauses)
 s.add(v[index[0,pattern]])
 status=str(s.check());print(pattern,status,'elapsed',time.time()-start,flush=True)
 result={'t':t,'k':k,'core_size':c,'status':status,'elapsed':time.time()-start,'pattern':pattern}
 if status=='sat':
  model=s.model();fam=[sorted(f) for a,f in enumerate(F) if z3.is_true(model.eval(v[a]))]
  assert all(set(a)&set(b) for a,b in itertools.combinations(fam,2))
  assert all(any(not set(C)&set(f) for f in fam) for C in itertools.combinations(range(n),t-1))
  result['family']=fam
 results.append(result)
 with open('workspace/agent2_t6_k7.json','w') as out:json.dump(results,out)
with open('workspace/agent2_t6_k7.py','w') as out:out.write(open('scratchpad.py').read())
