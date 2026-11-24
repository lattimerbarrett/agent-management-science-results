import itertools,time,json
from pathlib import Path
import z3
# Restricted finite search: t6, k6, six disjoint cores size4, residuals size2.
t=6;s=4;n=t*s
cores=[set(range(s*i,s*i+s)) for i in range(t)]
res=[]; edges=[]; groups=[]
for i in range(t):
 g=[]
 for R in itertools.combinations(set(range(n))-cores[i],2):
  g.append(len(edges));res.append(set(R));edges.append(cores[i]|set(R))
 groups.append(g)
B=[z3.Bool('e%d'%i) for i in range(len(edges))]
sol=z3.Solver();sol.set(timeout=90000)
for g in groups:sol.add(z3.Or([B[j] for j in g]))
for i in range(t):
 for j in range(i):
  for a in groups[i]:
   for b in groups[j]:
    if edges[a].isdisjoint(edges[b]):sol.add(z3.Or(z3.Not(B[a]),z3.Not(B[b])))
print('vars',len(B),'initial constraints',len(sol.assertions()),flush=True)
# Add all covers selecting one point in five distinct core blocks.
# These are the obvious t-1 covers and enforce genuinely all six classes.
for omitted in range(t):
 for C in itertools.product(*[sorted(cores[i]) for i in range(t) if i!=omitted]):
  CC=set(C)
  sol.add(z3.Or([B[a] for a in groups[omitted] if edges[a].isdisjoint(CC)]))
print('after rainbow cover cuts',len(sol.assertions()),flush=True)
# Every set of size <=5 extends to size5, so these constraints are exhaustive.
for ii,C in enumerate(itertools.combinations(range(n),t-1)):
 CC=set(C)
 if len({v//s for v in C})==t-1: continue
 sol.add(z3.Or([B[a] for a,F in enumerate(edges) if F.isdisjoint(CC)]))
print('all cover cuts',len(sol.assertions()),flush=True)
Path('workspace/agent2_original_sat.py').write_text(Path('scratchpad.py').read_text())
start=time.time()
for iteration in range(500):
 if iteration == 0:
  a0 = next(a for a in groups[0] if res[a] == {4,5})
  a1 = next(a for a in groups[0] if res[a] == {4,8})
  rr=sol.check(B[a1])
  print('symmetry branch', sorted(res[a1]), rr, flush=True)
  if rr==z3.unsat:
   # By all core/point symmetries, no selected residual can touch two blocks.
   sol.add(*[z3.Not(B[a]) for a,R in enumerate(res) if len({v//s for v in R})==2])
  rr=sol.check(B[a0])
  print('symmetry branch', sorted(res[a0]), rr, flush=True)
  r=rr
 else: r=sol.check()
 if r!=z3.sat:
  print('RESULT',r,'iteration',iteration,'secs',time.time()-start,flush=True);break
 model=sol.model();chosen=[a for a,b in enumerate(B) if z3.is_true(model.eval(b,model_completion=True))]
 h=z3.Solver();h.set(timeout=15000)
 V=[z3.Bool('v%d'%i) for i in range(n)]
 h.add(z3.PbLe([(v,1) for v in V],t-1))
 for a in chosen:h.add(z3.Or([V[v] for v in edges[a]]))
 hr=h.check()
 if hr==z3.unsat:
  data={'t':t,'k':6,'cores':[sorted(x) for x in cores],'edges':[sorted(edges[a]) for a in chosen]}
  Path('workspace/agent2_original_sat_witness.json').write_text(json.dumps(data))
  print('FOUND',len(chosen),data,flush=True);break
 if hr!=z3.sat:print('cover oracle unknown',flush=True);break
 hm=h.model();C={i for i,v in enumerate(V) if z3.is_true(hm.eval(v,model_completion=True))}
 sol.add(z3.Or([B[a] for a,F in enumerate(edges) if F.isdisjoint(C)]))
 if iteration%10==0:print(iteration,'chosen',len(chosen),'cut',sorted(C),'elapsed',time.time()-start,flush=True)
Path('workspace/agent2_original_sat.py').write_text(Path('scratchpad.py').read_text())
