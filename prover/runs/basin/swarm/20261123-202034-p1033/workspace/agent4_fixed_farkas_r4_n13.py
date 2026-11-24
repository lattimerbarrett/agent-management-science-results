import itertools,z3,time,json
start=time.time();r=4;n=13;weights=[-10]*5+[1]*4+[10]*4
edges=[e for e in itertools.combinations(range(n),r) if sum(weights[x] for x in e)>=0];masks=[sum(1<<x for x in e) for e in edges];vs=[z3.Bool('e%d'%i) for i in range(len(edges))];s=z3.Solver();s.set(timeout=60000)
# Symmetry within weight orbits: the edge covering {0,1} must use two heavy vertices, can anchor {0,1,9,10}.
s.add(vs[edges.index((0,1,9,10))])
conflicts=0
for i,e in enumerate(masks):
 for j in range(i):
  if not e&masks[j]:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])));conflicts+=1
for C in itertools.combinations(range(n),r-1):
 cm=sum(1<<x for x in C);s.add(z3.Or([vs[i] for i,e in enumerate(masks) if not e&cm]))
for x,y in itertools.combinations(range(n),2):s.add(z3.Or([vs[i] for i,e in enumerate(edges) if x in e and y in e]))
print('built',len(edges),'edges',conflicts,'conflicts',time.time()-start,flush=True)
status=s.check();out=dict(r=r,n=n,weights=weights,status=str(status),runtime=time.time()-start)
if status==z3.sat:
 model=s.model();fam=[e for i,e in enumerate(edges) if z3.is_true(model.eval(vs[i]))]
 assert all(set(a)&set(b) for a in fam for b in fam)
 assert all(any(not set(c)&set(e) for e in fam) for c in itertools.combinations(range(n),3))
 assert all(any(set(c)<=set(e) for e in fam) for c in itertools.combinations(range(n),2))
 assert all(sum(weights[x] for x in e)>=0 for e in fam) and sum(weights)<0
 out['family']=fam
print(out,flush=True)
with open('workspace/agent4_fixed_farkas_r4_n13.json','w') as f:json.dump(out,f,indent=2)
with open('workspace/agent4_fixed_farkas_r4_n13.py','w') as f:f.write(open(__file__).read())
