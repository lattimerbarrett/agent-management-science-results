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
for nb in (2,3,4):
 for ns in partitions(14,nb):
  points=list(itertools.product(*[range(n+1) for n in ns]));index={a:i for i,a in enumerate(points)};weights=[math.prod(math.comb(n,b) for n,b in zip(ns,a)) for a in points];N=len(points)
  rows=[]
  for a in points:
   if sum(a)>8:
    subs=itertools.product(*[[b for b in range(x+1) if b&x==b] for x in a]);rows.append((sum(1<<index[b] for b in subs),0))
  rows += [(1<<i,0) for i,w in enumerate(weights) if w>156]
  rows.append((1<<index[(0,)*nb],1))
  for i in range(nb):
   a=[0]*nb;a[i]=1;rows.append((1<<index[tuple(a)],1))
  basis={};inconsistent=False
  for row,rhs in rows:
   while row:
    p=row.bit_length()-1
    if p in basis:b,rr=basis[p];row^=b;rhs^=rr
    else:basis[p]=(row,rhs);break
   if not row and rhs:inconsistent=True;break
  if inconsistent:results.append((ns,0,'linear_unsat',0));print(results[-1],flush=True);continue
  free=[i for i in range(N) if i not in basis];D=len(free);expr={i:1<<j for j,i in enumerate(free)}
  for p in sorted(basis):
   row,rhs=basis[p];row^=1<<p;v=rhs<<D
   while row:
    low=row&-row;i=low.bit_length()-1;v^=expr[i];row^=low
   expr[p]=v
  s=z3.Solver();s.set(timeout=10000);bs=[z3.Bool('b%d'%i) for i in range(D)]
  f=[xors([b for j,b in enumerate(bs) if expr[i]>>j&1]+([z3.BoolVal(True)] if expr[i]>>D&1 else [])) for i in range(N)]
  s.add(z3.Or(*[z3.PbEq(list(zip(f,weights)),w) for w in (152,154,156)]))
  tt=time.time();res=s.check();results.append((ns,D,str(res),time.time()-tt));print(results[-1],flush=True)
  if res==z3.sat:
   model=s.model();active={a for a in points if z3.is_true(model.eval(f[index[a]]))};support=[]
   for x in range(1<<14):
    a=[];off=0
    for n in ns:a.append(((x>>off)&((1<<n)-1)).bit_count());off+=n
    if tuple(a) in active:support.append(x)
   assert len(support) in (152,154,156)
   assert 0 in support and all(1<<i in support for i in range(14))
   S=set(support);table=[int(x in S) for x in range(1<<14)]
   for i in range(14):
    for x in range(1<<14):
     if x>>i&1:table[x]^=table[x^(1<<i)]
   assert max(x.bit_count() for x,v in enumerate(table) if v)<=8
   json.dump({'partition':ns,'support':support},open('workspace/agent2_co6sym_rank_HIT.json','w'));print('VERIFIED FULLRANK14HIT',len(support),flush=True);raise SystemExit
json.dump(results,open('workspace/agent2_co6sym_rank_results.json','w'));print('seconds',time.time()-t0)
Path('workspace/agent2_co6sym_rank.py').write_text(Path(__file__).read_text())
