import itertools,time,json
import z3
from pathlib import Path
n=9; d=3
Fs=[frozenset(c) for c in itertools.combinations(range(n),d+1)]
M=len(Fs); s=z3.Solver(); s.set(timeout=240000)
r=[z3.Int('r%d'%i) for i in range(M)]
x=[v>=0 for v in r]
for i in range(M):s.add(z3.Or(r[i]==-i-1,z3.And(r[i]>=0,r[i]<M)))
s.add(r[0]==0)
s.add(z3.Or(*[z3.Not(q) for q in x]))
tri={T:z3.Bool('t'+''.join(map(str,sorted(T)))) for T in set(F-{v} for F in Fs for v in F)}
for T,b in tri.items():s.add(b==z3.Or(*[x[j] for j,G in enumerate(Fs) if T<=G]))
for i,F in enumerate(Fs):s.add(z3.Implies(z3.Not(x[i]),z3.PbLe([(tri[F-{v}],1) for v in F],2)))
for e in itertools.combinations(range(n),2):s.add(z3.Or(*[x[i] for i,F in enumerate(Fs) if set(e)<=F]))
# Search without shellability first.
print('built',M,'variables facets; solving',flush=True)
t=time.time();res=s.check();print(res,time.time()-t,flush=True)
if res==z3.sat:
    m=s.model();ans=sorted((m.eval(r[i]).as_long(),sorted(F)) for i,F in enumerate(Fs) if z3.is_true(m.eval(x[i])))
    print(ans)
    Path('workspace/agent1_candidate.json').write_text(json.dumps(ans))
Path('workspace/agent1_localflag_search.py').write_text(Path('scratchpad.py').read_text())
