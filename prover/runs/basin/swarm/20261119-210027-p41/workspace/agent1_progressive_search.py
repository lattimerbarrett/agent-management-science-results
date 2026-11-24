import itertools,time,json
import z3
from pathlib import Path
n=9; d=3
Fs=[frozenset(c) for c in itertools.combinations(range(n),d+1)]
M=len(Fs); s=z3.Solver(); s.set(timeout=240000)
x=[z3.Bool('x%d'%i) for i in range(M)]
s.add(x[Fs.index(frozenset((0,1,3,4)))],z3.Or(*[z3.Not(q) for q in x]))
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

s.add(z3.Not(tri[frozenset((0,1,2))]))
pairs=list(itertools.combinations(range(1,n),2));pi={p:i for i,p in enumerate(pairs)}
vec={T:sum(1<<pi[p] for p in itertools.combinations(sorted(T),2) if p[0]!=0) for T in tri}

def force_fill(target):
 coeff={T:z3.Bool(f'c{target}_{"".join(map(str,sorted(T)))}') for T in tri}
 for T,c in coeff.items():s.add(z3.Implies(c,tri[T]))
 for coord in range(len(pairs)):
  terms=[c for T,c in coeff.items() if vec[T]>>coord&1]
  parity=terms[0]
  for q in terms[1:]:parity=z3.Xor(parity,q)
  s.add(parity==(target==coord))
def cocycles(ys):
 basis={}
 for T in ys:
  row=vec[T]
  while row:
   j=row.bit_length()-1
   if j not in basis:basis[j]=row;break
   row^=basis[j]
 out=[]
 for f in range(len(pairs)):
  if f in basis:continue
  w=1<<f
  for j,row in sorted(basis.items()):
   if (row&w).bit_count()%2:w^=1<<j
  out.append(w)
 return out
start=time.time();targets={pi[(1,2)]};force_fill(pi[(1,2)])
for it in range(len(pairs)):
 s.set(timeout=60000)
 res=s.check();print(it,'targets',sorted(targets),res,'time',time.time()-start,flush=True)
 if res!=z3.sat:break
 m=s.model();ys=[T for T,b in tri.items() if z3.is_true(m.eval(b))]
 cc=cocycles(ys)
 if not cc:
  ans=[sorted(F) for i,F in enumerate(Fs) if z3.is_true(m.eval(x[i]))]
  print('H1ZERO',ans,flush=True);Path('workspace/agent1_h1zero_candidate.json').write_text(json.dumps(ans));break
 w=cc[0]
 for j in range(len(pairs)):
  if w>>j&1 and j not in targets:targets.add(j);force_fill(j);break
 if time.time()-start>240:break
Path('workspace/agent1_progressive_search.py').write_text(Path('scratchpad.py').read_text())
