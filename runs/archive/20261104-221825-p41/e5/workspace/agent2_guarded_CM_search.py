from itertools import combinations
from pathlib import Path
import z3,time,sys,json
sys.path.insert(0,'workspace')
from a3_modular_homology import witness

def faces(fs):
 C={0}
 for f in fs:
  g=f
  while g:C.add(g);g=(g-1)&f
 return C

def run(n=9,seconds=100,primes=(2,3,5)):
 F=[sum(1<<v for v in c) for c in combinations(range(n),4)]
 fv={g:z3.Bool('f%d'%g) for g in F}
 var={g:z3.Bool('a%d'%g) for q in [2,3] for c in combinations(range(n),q) for g in [sum(1<<v for v in c)]}
 s=z3.Solver();s.set(timeout=10000,random_seed=178)
 for g,v in var.items():s.add(v==z3.Or([fv[f] for f in F if f&g==g]))
 for f in F:
  vs=[v for v in range(n) if f>>v&1];b=[var[f^(1<<v)] for v in vs]
  # Missing facet with >=3 boundarytriangles is legal; exactly2 is legal iff oppositeedge absent.
  s.add(z3.Or(fv[f],z3.PbLe([(v,1) for v in b],2)))
  for a,c in combinations(range(4),2):s.add(z3.Or(fv[f],z3.Not(b[a]),z3.Not(b[c]),var[(1<<vs[a])|(1<<vs[c])]))
 for v in range(n):s.add(z3.Or([fv[f] for f in F if f>>v&1]))
 s.add(z3.Not(z3.And(list(fv.values()))));s.add(fv[F[0]])
 def present(g):return z3.BoolVal(True) if g.bit_count()<=1 else var[g]
 start=time.time();cuts=set();iterations=0;candidates=[];last='time'
 while time.time()-start<seconds:
  result=s.check();last=str(result)
  if result!=z3.sat:print('RESULT',result,s.reason_unknown(),flush=True);break
  model=s.model();fs=tuple(f for f in F if z3.is_true(model[fv[f]]));C=faces(fs);newcuts=[]
  for tau in C:
   if tau.bit_count()>2:continue
   L={g^tau for g in C if g&tau==tau}
   for i in range(3-tau.bit_count()):
    for p in primes:
     answer=witness(L,i,p)
     if answer is None:continue
     z,u=answer
     guard=tuple(sorted(tau|g for g in z))
     possible=[]
     for f in F:
      if f&tau!=tau:continue
      vv=[v for v in range(n) if (f^tau)>>v&1];odd=False
      for cc in combinations(vv,i+2):
       h=sum(1<<v for v in cc)
       pairing=sum((-1)**j*u.get(h^(1<<v),0) for j,v in enumerate(cc))%p
       if pairing:odd=True;break
      if odd:possible.append(f)
     positive=tuple(possible)
     assert positive and not set(positive)&set(fs)
     key=(guard,positive)
     if key not in cuts:cuts.add(key);newcuts.append(key)
  if not newcuts:
   # No generated obstruction may also mean all extant witnesses alreadycut: impossible for aSATmodel.
   candidates.append(fs);print('CM_ALL_TESTED_PRIMES',len(fs),'iteration',iterations,flush=True)
   Path('workspace/agent2_CM_candidate_n%d_%d.json'%(n,len(candidates))).write_text(json.dumps(fs))
   s.add(z3.Or([z3.Not(fv[f]) if f in fs else fv[f] for f in F]))
  for guard,positive in newcuts:
   s.add(z3.Or([z3.Not(present(g)) for g in guard]+[fv[f] for f in positive]))
  iterations+=1
  if iterations%20==0:print('it',iterations,'cuts',len(cuts),'sec',time.time()-start,flush=True)
 report=dict(n=n,primes=primes,iterations=iterations,cuts=len(cuts),candidates=len(candidates),last=last,seconds=time.time()-start)
 Path('workspace/agent2_guarded_CM_n%d_report.json'%n).write_text(json.dumps(report));print(report,flush=True)
 return report
if __name__=='__main__':run()
