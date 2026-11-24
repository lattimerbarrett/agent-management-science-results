from itertools import combinations
from pathlib import Path
import z3,time,sys,json
sys.path.insert(0,'workspace');from a3_fastkd import kd
n=8;q=4
F=[sum(1<<x for x in c) for c in combinations(range(n),q)];m=len(F)
s=z3.Solver();s.set(timeout=20000)
t=[z3.Int('t%d'%i) for i in range(m)];P=[x<=m for x in t]
s.add(*[z3.And(x>=1,x<=m+1) for x in t]);s.add(t[0]==1,t[1]==2)
for i in range(m):
 for j in range(i):s.add(z3.Or(z3.Not(P[i]),z3.Not(P[j]),t[i]!=t[j]))
s.add(z3.Or(*[z3.Not(p) for p in P]))
R={};B={}
for i,f in enumerate(F):
 vs=[v for v in range(n) if f>>v&1]
 for v in vs:
  r=R[i,v]=z3.Bool('r%d_%d'%(i,v));b=B[i,v]=z3.Bool('b%d_%d'%(i,v))
  ridge=f^(1<<v);nn=[j for j,g in enumerate(F) if j!=i and g&ridge==ridge]
  s.add(b==z3.Or(*[P[j] for j in nn]))
  if i:s.add(z3.Implies(z3.And(P[i],r),z3.Or(*[t[j]<t[i] for j in nn])))
 if i:s.add(z3.Implies(P[i],z3.Or(*[R[i,v] for v in vs])))
 for j,g in enumerate(F):
  if i!=j and i:s.add(z3.Implies(z3.And(P[i],t[j]<t[i]),z3.Or(*[R[i,v] for v in vs if not(g>>v&1)])))
 blocked=z3.Or(*[z3.And(P[j],*[z3.Not(B[i,v]) for v in vs if not(g>>v&1)]) for j,g in enumerate(F) if i!=j])
 s.add(z3.Implies(z3.Not(P[i]),z3.Or(blocked,z3.PbEq([(B[i,v],1) for v in vs],3))))
for v in range(n):s.add(z3.Or(*[P[i] for i,f in enumerate(F) if f>>v&1]))
print('encoded',flush=True);start=time.time()
for it in range(100):
 res=s.check()
 if res!=z3.sat:print('RESULT',res,s.reason_unknown(),flush=True);break
 model=s.model();present=[i for i in range(m) if z3.is_true(model.eval(P[i]))];fs=tuple(F[i] for i in present)
 print('model',it,'facets',len(fs),'time',time.time()-start,flush=True)
 iskd=kd(fs,1);print('edge-decomp?',iskd,flush=True)
 if iskd:
  good=[]
  for i in range(m):
   if i not in present and kd(tuple(sorted(fs+(F[i],))),1):good.append(i)
  print('outgoing',len(good),flush=True)
  if not good:
   print('FOUND',fs,flush=True);Path('workspace/a4_edge_obstruction.json').write_text(json.dumps(fs));break
 s.add(z3.Or(*[z3.Not(P[i]) if i in present else P[i] for i in range(m)]))
 if time.time()-start>100:break
Path('workspace/agent4_edge_sat.py').write_text(Path(__file__).read_text())
