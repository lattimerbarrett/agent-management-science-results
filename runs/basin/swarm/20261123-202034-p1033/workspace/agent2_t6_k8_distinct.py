import itertools,z3,time,json
from pathlib import Path
start=time.time();t=6;k=8;d=2;c=k-d;n=t*c
cores=[frozenset(range(c*i,c*(i+1))) for i in range(t)]
F=[];owner=[];R=[];index={}
for i in range(t):
 for r in itertools.combinations(sorted(set(range(n))-cores[i]),d):
  index[i,r]=len(F);R.append(r);F.append(cores[i]|frozenset(r));owner.append(i)
M=[sum(1<<x for x in f) for f in F]
v=[z3.Bool('v'+str(a)) for a in range(len(F))]
s=z3.Solver();s.set(timeout=120000)
conf_count=0
for a in range(len(F)):
 for b in range(a):
  if owner[a]!=owner[b] and not M[a]&M[b]:
   s.add(z3.Or(z3.Not(v[a]),z3.Not(v[b])));conf_count+=1
print('conflicts',conf_count,'elapsed',time.time()-start,flush=True)
pattern=(c,2*c);s.add(v[index[0,pattern]])
count=0
V=set(range(n))
for Ct in itertools.combinations(range(n),t-1):
 hit={x//c for x in Ct};C=set(Ct);inds=[]
 for i in set(range(t))-hit:
  avail=sorted(V-cores[i]-C)
  inds.extend(index[i,r] for r in itertools.combinations(avail,2))
 s.add(z3.Or([v[a] for a in inds]));count+=1
 if count%50000==0:print('covers',count,'elapsed',time.time()-start,flush=True)
print('built all covers',count,'elapsed',time.time()-start,flush=True)
status=str(s.check());print('RESULT',status,'elapsed',time.time()-start,flush=True)
result={'t':t,'k':k,'core_size':c,'n':n,'status':status,'elapsed':time.time()-start,'pattern':pattern,'variables':len(F),'cover_clauses':count,'conflict_clauses':conf_count}
if status=='sat':
 model=s.model();fam=[sorted(f) for a,f in enumerate(F) if z3.is_true(model.eval(v[a]))]
 assert all(set(a)&set(b) for a,b in itertools.combinations(fam,2))
 assert all(any(not set(C)&set(f) for f in fam) for C in itertools.combinations(range(n),t-1))
 result['family']=fam
Path('workspace/agent2_t6_k8_distinct.json').write_text(json.dumps(result,indent=2))
Path('workspace/agent2_t6_k8_distinct.py').write_text(Path('scratchpad.py').read_text())
