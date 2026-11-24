from itertools import combinations
import z3,time,json
from pathlib import Path
n=12;d=3
Fs=tuple(frozenset(F) for F in combinations(range(n),4));M=len(Fs)
s=z3.SolverFor('QF_FD');s.set(timeout=600000)
width=(4*M).bit_length()
r=[z3.BitVec('r%d'%i,width) for i in range(M)];x=[r[i]<M for i in range(M)]
for i in range(M):s.add(z3.Or(z3.And(r[i]>=0,r[i]<M),r[i]==M+i))
s.add(z3.Distinct(r))
s.add(r[Fs.index(frozenset((0,1,2,3)))]==0,r[Fs.index(frozenset((0,1,2,4)))]==1)
for i,F in enumerate(Fs):
 if F not in (frozenset((0,1,2,3)),frozenset((0,1,2,4))):s.add(r[i]!=0,r[i]!=1)
b={frozenset(T):z3.BitVec('b'+'_'.join(map(str,T)),width) for size in (1,2,3) for T in combinations(range(n),size)}
for T,v in b.items():
 inc=[z3.If(x[i],r[i],M) for i,F in enumerate(Fs) if T<=F]
 s.add(v>=0,v<=M,z3.Or(*[v==q for q in inc]))
 s.add(*[v<=q for q in inc])
 if len(T)==1:s.add(v<M)
s.add(z3.Or(*[z3.Not(q) for q in x]))
count=sum([z3.If(q,z3.BitVecVal(1,width),z3.BitVecVal(0,width)) for q in x])
s.add(count==60)
for i in range(M):s.add(z3.Implies(x[i],r[i]<60))
for v in range(5,n-1):s.add(b[frozenset((v,))]<=b[frozenset((v+1,))])
for i,F in enumerate(Fs):
 ridges={v:b[F-{v}] for v in F}
 condition=z3.And(x[i],r[i]>0)
 for size in range(4):
  for tau in combinations(sorted(F),size):
   T=frozenset(tau);old=z3.BoolVal(True) if not T else b[T]<r[i]
   s.add(z3.Implies(z3.And(condition,old),z3.Or(*[ridges[v]<r[i] for v in F-T])))
 y={v:ridges[v]<M for v in F}
 s.add(z3.Implies(z3.Not(x[i]),z3.PbLe([(q,1) for q in y.values()],2)))
 for u,v in combinations(sorted(F),2):
  s.add(z3.Implies(z3.And(z3.Not(x[i]),y[u],y[v]),b[frozenset((u,v))]<M))
print('BUILT',n,M,len(s.assertions()),flush=True)
t=time.time();res=s.check();print(res,time.time()-t,flush=True)
if res==z3.unknown:print(s.reason_unknown(),flush=True)
if res==z3.sat:
 m=s.model();out=sorted((m.eval(r[i]).as_long(),sorted(F)) for i,F in enumerate(Fs) if z3.is_true(m.eval(x[i])))
 print(out,flush=True)
 Path('workspace/agent1_birth_candidate.json').write_text(json.dumps(out))
Path('workspace/agent1_birth_search.py').write_text(Path('scratchpad.py').read_text())
