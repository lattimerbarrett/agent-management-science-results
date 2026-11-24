import itertools,time,json
import z3
from pathlib import Path
n=9; d=3
Fs=[frozenset(c) for c in itertools.combinations(range(n),d+1)]
M=len(Fs); s=z3.Solver(); s.set(timeout=240000)
x=[z3.Bool('x%d'%i) for i in range(M)]
s.add(x[0],z3.Or(*[z3.Not(q) for q in x]))
tri={T:z3.Bool('t'+''.join(map(str,sorted(T)))) for T in set(F-{v} for F in Fs for v in F)}
for T,b in tri.items():s.add(b==z3.Or(*[x[j] for j,G in enumerate(Fs) if T<=G]))
for i,F in enumerate(Fs):s.add(z3.Implies(z3.Not(x[i]),z3.PbLe([(tri[F-{v}],1) for v in F],2)))
for e in itertools.combinations(range(n),2):s.add(z3.Or(*[x[i] for i,F in enumerate(Fs) if set(e)<=F]))
for size in (0,1,2):
 for tau in itertools.combinations(range(n),size):
    T=set(tau);inds=[i for i,F in enumerate(Fs) if T<=F]
    D={i:z3.Int('d'+str(tau)+'_'+str(i)) for i in inds}
    for pos,i in enumerate(inds):
        s.add(D[i]>=0,D[i]<len(inds))
        root=z3.And(*[z3.Not(x[j]) for j in inds[:pos]])
        nb=[j for j in inds if j!=i and len(Fs[i]&Fs[j])==3]
        s.add(z3.Implies(x[i],z3.Or(root,*[z3.And(x[j],D[j]<D[i]) for j in nb])))
print('built',M,'solving',flush=True)
t=time.time();res=s.check();print(res,time.time()-t,flush=True)
if res==z3.sat:
    m=s.model();ans=[sorted(F) for i,F in enumerate(Fs) if z3.is_true(m.eval(x[i]))]
    print(ans)
    Path('workspace/agent1_strong_candidate.json').write_text(json.dumps(ans))
Path('workspace/agent1_strong_search.py').write_text(Path('scratchpad.py').read_text())
