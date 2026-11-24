import itertools,z3,time,json
start=time.time();r=4;n=14
edges=list(itertools.combinations(range(n),r));masks=[sum(1<<x for x in e) for e in edges];vs=[z3.Bool('e%d'%i) for i in range(len(edges))];s=z3.Solver();s.set(timeout=180000)
# Symmetry: one edge 0,1,2,3 belongs.
s.add(vs[0])
conflicts=0
for i,e in enumerate(masks):
 for j in range(i):
  if not e&masks[j]:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])));conflicts+=1
for C in itertools.combinations(range(n),r-1):
 cm=sum(1<<x for x in C);s.add(z3.Or([vs[i] for i,e in enumerate(masks) if not e&cm]))
for x,y in itertools.combinations(range(n),2):s.add(z3.Or([vs[i] for i,e in enumerate(edges) if x in e and y in e]))
print('built',len(edges),'edges',conflicts,'conflicts',time.time()-start,flush=True)
status=s.check();out=dict(r=r,n=n,status=str(status),runtime=time.time()-start)
if status==z3.sat:
 model=s.model();fam=[e for i,e in enumerate(edges) if z3.is_true(model.eval(vs[i]))]
 assert all(set(a)&set(b) for a in fam for b in fam)
 assert all(any(not set(c)&set(e) for e in fam) for c in itertools.combinations(range(n),3))
 assert all(any(set(c)<=set(e) for e in fam) for c in itertools.combinations(range(n),2))
 out['family']=fam
print(out,flush=True)
with open('workspace/agent4_pairshadow_r4_n14.json','w') as f:json.dump(out,f,indent=2)
with open('workspace/agent4_pairshadow_r4_n14.py','w') as f:f.write(open(__file__).read())
