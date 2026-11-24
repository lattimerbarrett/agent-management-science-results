from itertools import combinations
import z3,time,json

def search(n,seconds=120):
 fs=list(combinations(range(n),4));ts=list(combinations(range(n),3));F={f:z3.Bool('f'+str(f)) for f in fs};T={t:z3.Bool('t'+str(t)) for t in ts}
 s=z3.Solver();s.set(timeout=seconds*1000)
 for t in ts:
  cnt=z3.Sum([z3.If(F[f],1,0) for f in fs if set(t)<=set(f)])
  s.add(z3.Or(cnt==0,cnt==2),T[t]==(cnt==2))
 for f in fs:
  s.add(z3.Or(F[f],z3.Sum([z3.If(T[t],1,0) for t in combinations(f,3)])<=2))
  if 0 in f and 1 in f:s.add(z3.Not(F[f]))
 for v in range(n):s.add(z3.Sum([z3.If(F[f],1,0) for f in fs if v in f])==(2*n-8 if v<2 else 2*n-6))
 for a,b in combinations(range(n),2):
  if (a,b)==(0,1):continue
  s.add(z3.Or([F[f] for f in fs if a in f and b in f]))
 for a,b in combinations(range(2,n),2):s.add(z3.Not(z3.And(T[(0,a,b)],T[(1,a,b)])))
 s.add(F[(0,2,3,4)],F[(0,2,3,5)])
 tm=time.time();ans=s.check();print('onemissing',n,ans,time.time()-tm,flush=True)
 if ans==z3.sat:
  m=s.model();fac=[f for f in fs if z3.is_true(m.eval(F[f]))]
  json.dump(fac,open('workspace/agent1_onemissing'+str(n)+'.json','w'));print('facets',len(fac),flush=True)
  from sage.all import SimplicialComplex
  K=SimplicialComplex(fac);print('HOMOLOGY',K.homology(),flush=True)
 return ans
if __name__=='__main__':
 for n in [13,14,15]:search(n)
