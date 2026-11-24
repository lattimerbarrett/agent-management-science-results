import itertools,z3,time,json
start=time.time();sizes=[3,2,2,2];cores=[];base=0
for c in sizes:cores.append(set(range(base,base+c)));base+=c
n=base;t=4;d=[t-c for c in sizes]
families=[]
for i,X in enumerate(cores):families.append([X|set(P) for P in itertools.combinations(set(range(n))-X,d[i])])
vs=[[z3.Bool('e%d_%d'%(i,j)) for j in range(len(fam))] for i,fam in enumerate(families)]
s=z3.Solver();s.set(timeout=120000)
for v in vs:s.add(z3.Or(v))
# valid first-edge symmetry
s.add(vs[0][next(j for j,E in enumerate(families[0]) if E==cores[0]|{3})])
good={};conf=0
for i in range(t):
 for j in range(i):
  for a,E in enumerate(families[i]):
   for b,F in enumerate(families[j]):
    meet=E&F
    good[i,a,j,b]=bool(meet) and (meet<=cores[i] or meet<=cores[j])
    if not meet:s.add(z3.Or(z3.Not(vs[i][a]),z3.Not(vs[j][b])));conf+=1
for C in itertools.combinations(range(n),t-1):s.add(z3.Or([vs[i][a] for i in range(t) for a,E in enumerate(families[i]) if not set(C)&E]))
forbidden=0
for choices in itertools.product(*[range(len(fam)) for fam in families]):
 if any(not families[i][choices[i]]&families[j][choices[j]] for i in range(t) for j in range(i)):continue
 score=sum(good[i,choices[i],j,choices[j]] for i in range(t) for j in range(i))
 if score>=5:s.add(z3.Or([z3.Not(vs[i][a]) for i,a in enumerate(choices)]));forbidden+=1
print('built',list(map(len,families)),'conf',conf,'forbidden',forbidden,'time',time.time()-start,flush=True)
status=s.check();out=dict(status=str(status),sizes=sizes,counts=list(map(len,families)),conflicts=conf,forbidden=forbidden,runtime=time.time()-start)
if status==z3.sat:
 model=s.model();selected=[[a for a,x in enumerate(v) if z3.is_true(model.eval(x))] for v in vs]
 H=[E for i,fam in enumerate(families) for a,E in enumerate(fam) if a in selected[i]]
 assert all(E&F for E in H for F in H)
 assert all(any(not E&set(C) for E in H) for C in itertools.combinations(range(n),3))
 maxscore=max(sum(good[i,c[i],j,c[j]] for i in range(t) for j in range(i)) for c in itertools.product(*selected));assert maxscore<5
 out.update(selected=[[sorted(families[i][a]) for a in A] for i,A in enumerate(selected)],maxscore=maxscore)
print(out,flush=True)
with open('workspace/agent4_rank4_arc_check.json','w') as f:json.dump(out,f,indent=2)
with open('workspace/agent4_rank4_arc_check.py','w') as f:f.write(open(__file__).read())
