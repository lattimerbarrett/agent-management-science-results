import itertools,z3,time,json
start=time.time();r=4;n=13;weights=[-10]*5+[1]*4+[10]*4
E=list(itertools.combinations(range(n),r));idx={e:i for i,e in enumerate(E)};vs=[z3.Bool('e%d'%i) for i in range(len(E))];bs=[z3.Bool('b%d'%i) for i in range(len(E))];s=z3.Solver();s.set(timeout=120000)
# EveryHedgeisalsoamincover(sinceintersectingrankrτr); henceHedgeweightsnonnegativeaswell.
for i,e in enumerate(E):
 complement=[v for v in range(n) if v not in e];disj=[idx[F] for F in itertools.combinations(complement,r)]
 s.add(bs[i]==z3.And([z3.Not(vs[j]) for j in disj]))
 if sum(weights[v] for v in e)<0:s.add(z3.Not(bs[i]),z3.Not(vs[i]))
 for j in disj:
  if j<i:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
for C in itertools.combinations(range(n),r-1):
 cc=set(C);s.add(z3.Or([vs[idx[F]] for F in itertools.combinations([v for v in range(n) if v not in cc],r)]))
for a,b in itertools.combinations(range(n),2):s.add(z3.Or([bs[i] for i,e in enumerate(E) if a in e and b in e]))
print('built',len(E),'time',time.time()-start,flush=True)
status=s.check();out=dict(r=r,n=n,weights=weights,status=str(status),runtime=time.time()-start)
if status==z3.sat:
 model=s.model();H=[e for i,e in enumerate(E) if z3.is_true(model.eval(vs[i]))];B=[e for i,e in enumerate(E) if z3.is_true(model.eval(bs[i]))]
 assert all(set(e)&set(f) for e in H for f in H)
 assert all(any(not set(c)&set(e) for e in H) for c in itertools.combinations(range(n),r-1))
 assert all(any(set(p)<=set(c) for c in B) for p in itertools.combinations(range(n),2))
 assert all(all(set(c)&set(e) for e in H) for c in B)
 assert all(sum(weights[v] for v in c)>=0 for c in B) and sum(weights)<0
 out.update(H=H,B=B)
print({k:v for k,v in out.items() if k not in ('H','B')},flush=True)
with open('workspace/agent4_polar_fixed_farkas.json','w') as f:json.dump(out,f,indent=2)
with open('workspace/agent4_polar_fixed_farkas.py','w') as f:f.write(open(__file__).read())
