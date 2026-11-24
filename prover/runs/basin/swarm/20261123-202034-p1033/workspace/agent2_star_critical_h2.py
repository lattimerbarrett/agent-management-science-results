import itertools,z3,random,json,time
from pathlib import Path
h=2;n=2*h*h;t=h**3;r=n-h-1
G=[(b*2*h+a,b*2*h+h+c) for b in range(h) for a in range(h) for c in range(h)]
E=list(itertools.combinations(range(n),2));idx={e:i for i,e in enumerate(E)}
stars=[{idx[tuple(sorted((a,b)))] for b in range(n) if a!=b} for a in range(n)]
F=[]
for i,(a,b) in enumerate(G):
 for center in (a,b):
  for pt in itertools.combinations(sorted(stars[center]-{idx[(a,b)]}),r):F.append((i,center,pt))
m=len(E);y=[z3.Bool('p'+str(j)) for j in range(m+t)];act=[z3.Bool('a'+str(j)) for j in range(len(F))]
s=z3.Solver();s.set(timeout=10000);s.add(z3.PbLe([(v,1) for v in y],t-1))
for a,(i,c,P) in enumerate(F):s.add(z3.Implies(act[a],z3.Or([y[m+i]]+[y[j] for j in P])))
assert s.check(act)==z3.unsat
order=list(range(len(F)));random.Random(13).shuffle(order);current=set(order);witness={};start=time.time()
for a in order:
 status=s.check([act[b] for b in current-{a}]+[z3.Not(act[a])])
 assert status!=z3.unknown
 if status==z3.unsat:current.remove(a)
 else:
  model=s.model();C=[j for j,v in enumerate(y) if z3.is_true(model[v])];witness[a]=C
for a in current:
 C=set(witness[a]);i,c,P=F[a]
 assert not(C&({m+i}|set(P)))
 assert all(C&({m+F[b][0]}|set(F[b][2])) for b in current-{a})
result={'h':h,'t':t,'r':r,'initial_base_edges':len(F),'critical_base_edges':len(current),'class_sizes':[sum(F[a][0]==i for a in current) for i in range(t)],'witness_actual_counts':[sum(j<m for j in witness[a]) for a in sorted(current)],'critical_petals':[{'class':F[a][0],'center':F[a][1],'petal':F[a][2],'witness':witness[a]} for a in sorted(current)],'seconds':time.time()-start}
Path('workspace/agent2_star_critical_h2.json').write_text(json.dumps(result,indent=2));Path('workspace/agent2_star_critical_h2.py').write_text(Path('scratchpad.py').read_text())
print({k:v for k,v in result.items() if k!='critical_petals'})
