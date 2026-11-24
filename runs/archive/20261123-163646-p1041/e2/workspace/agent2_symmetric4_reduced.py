import z3,itertools,math,time,json
from pathlib import Path

def partitions(n,k,lo=1):
 if k==0:
  if n==0:yield ()
  return
 for a in range(lo,n//k+1):
  for b in partitions(n-a,k-1,a):yield (a,)+b

def xors(xs):
 if not xs:return z3.BoolVal(False)
 while len(xs)>1:xs=[z3.Xor(xs[i],xs[i+1]) if i+1<len(xs) else xs[i] for i in range(0,len(xs),2)]
 return xs[0]
results=[];t0=time.time()
for ns in partitions(15,4):
 points=list(itertools.product(*[range(n+1) for n in ns]));index={a:i for i,a in enumerate(points)};weights=[math.prod(math.comb(n,b) for n,b in zip(ns,a)) for a in points];N=len(points)
 rows=[]
 for a in points:
  if sum(a)>8:
   subs=itertools.product(*[[b for b in range(x+1) if b&x==b] for x in a]);rows.append(sum(1<<index[b] for b in subs))
 rows += [1<<i for i,w in enumerate(weights) if w>334]
 basis={}
 for row in rows:
  while row:
   p=row.bit_length()-1
   if p in basis:row^=basis[p]
   else:basis[p]=row;break
 free=[i for i in range(N) if i not in basis];expr={i:1<<j for j,i in enumerate(free)}
 for p in sorted(basis):
  row=basis[p]^(1<<p);v=0
  while row:
   low=row&-row;i=low.bit_length()-1;v^=expr[i];row^=low
  expr[p]=v
 s=z3.Solver();s.set(timeout=10000);bs=[z3.Bool('b%d'%i) for i in range(len(free))]
 f=[xors([b for j,b in enumerate(bs) if expr[i]>>j&1]) for i in range(N)]
 s.add(z3.Or(*[z3.PbEq(list(zip(f,weights)),w) for w in (322,326,330,334)]))
 # Full divided-square syndrome: one condition per coordinate block suffices.
 for i,n in enumerate(ns):
  terms=[]
  for a in itertools.product(*[range(nn+(j!=i)) for j,nn in enumerate(ns)]):
   if not all((aa & (nn-(j==i)))==aa for j,(nn,aa) in enumerate(zip(ns,a))):continue
   b=list(a);b[i]+=1;terms.append(z3.And(f[index[a]],f[index[tuple(b)]]))
  s.add(xors(terms))
 tt=time.time();res=s.check();results.append((ns,len(free),str(res),time.time()-tt));print(results[-1],flush=True)
 if res==z3.sat:
  model=s.model();active={a for a in points if z3.is_true(model.eval(f[index[a]]))};support=[]
  for x in range(1<<15):
   a=[];off=0
   for n in ns:a.append(((x>>off)&((1<<n)-1)).bit_count());off+=n
   if tuple(a) in active:support.append(x)
  assert len(support) in (322,326,330,334)
  S=set(support);table=[int(x in S) for x in range(1<<15)]
  for i in range(15):
   for x in range(1<<15):
    if x>>i&1:table[x]^=table[x^(1<<i)]
  assert max(x.bit_count() for x,v in enumerate(table) if v)<=8
  json.dump({'partition':ns,'support':support},open('workspace/agent2_symmetric4_reduced_HIT.json','w'));print('VERIFIED HIT',len(support),flush=True);break
json.dump(results,open('workspace/agent2_symmetric4_reduced_results.json','w'));print('seconds',time.time()-t0)
Path('workspace/agent2_symmetric4_reduced.py').write_text(Path(__file__).read_text())
