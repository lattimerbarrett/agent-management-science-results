import itertools,z3,time,json
from pathlib import Path
st=time.time();t=5;n=15;k=5; cores=[sum(1<<a for a in range(3*i,3*i+3)) for i in range(t)]
Es=[]; colors=[]; by=[[] for _ in range(t)]; lookup={}
for i,c in enumerate(cores):
 for P in itertools.combinations([a for a in range(n) if not(c>>a&1)],2):
  p=sum(1<<a for a in P);lookup[i,p]=len(Es);by[i].append(len(Es));Es.append(c|p);colors.append(i)
x=[z3.Bool('x%d'%j) for j in range(len(Es))];nx=[z3.Not(y) for y in x];s=z3.Solver();s.set(timeout=90000)
for cl in by:s.add(z3.Or([x[j] for j in cl]))
for a,E in enumerate(Es):
 for b in range(a):
  if colors[a]!=colors[b] and not E&Es[b]:s.add(z3.Or(nx[a],nx[b]))
for C in itertools.combinations(range(n),t-1):
 mask=sum(1<<a for a in C);s.add(z3.Or([x[j] for j,E in enumerate(Es) if not E&mask]))
pairs=list(itertools.combinations(range(t),2));perms=[list(itertools.permutations(range(3*i,3*i+3),2)) for i in range(t)]; clauses=[];nt=0
for bits in range(1<<len(pairs)):
 incoming=[[] for _ in range(t)];outgoing=[[] for _ in range(t)]
 for a,(i,j) in enumerate(pairs):
  if bits>>a&1:i,j=j,i
  incoming[j].append(i);outgoing[i].append(j)
 if any(len(cl)!=2 for cl in incoming):continue
 nt+=1
 for choices in itertools.product(*perms):
  pet=[0]*t
  for j in range(t):
   for ind,i in enumerate(incoming[j]):pet[i]|=1<<choices[j][ind]
  inds=[lookup[i,pet[i]] for i in range(t)]
  assert all((Es[a]&Es[b]) and ((Es[a]&Es[b])&~cores[colors[a]]==0 or (Es[a]&Es[b])&~cores[colors[b]]==0) for a,b in itertools.combinations(inds,2))
  clauses.append(z3.Or([nx[j] for j in inds]))
assert nt==24 and len(clauses)==186624
s.add(clauses); print('built',time.time()-st,flush=True);out={'t':t,'n':n,'tournaments':nt,'forbidden_tuples':len(clauses),'build_seconds':time.time()-st,'results':[]}
for pet in [(1<<3)|(1<<4),(1<<3)|(1<<6)]:
 s.push();s.add(x[lookup[0,pet]]);a=time.time();res=s.check();d={'anchor_petal':pet,'result':str(res),'seconds':time.time()-a}
 if res==z3.sat:
  mod=s.model();d['selected']=[{'color':colors[j],'edge':[a for a in range(n) if E>>a&1]} for j,E in enumerate(Es) if z3.is_true(mod[x[j]])]
 out['results'].append(d);print(d,flush=True);s.pop()
out['seconds']=time.time()-st
Path('workspace/agent1_t5_arc_full.py').write_text(Path(__file__).read_text());Path('workspace/agent1_t5_arc_full.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))