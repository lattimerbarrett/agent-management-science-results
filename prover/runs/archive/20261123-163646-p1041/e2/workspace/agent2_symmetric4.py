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
 points=list(itertools.product(*[range(n+1) for n in ns]));f={a:z3.Bool('f'+'_'.join(map(str,a))) for a in points};s=z3.Tactic('sat').solver();s.set(timeout=15000);s.set(anf=True);s.set('anf.exlin',True);s.set('anf.delay',0)
 for a in points:
  if sum(a)>8:
   subs=itertools.product(*[[b for b in range(x+1) if b&x==b] for x in a]);s.add(z3.Not(xors([f[b] for b in subs])))
 weighted=[(f[a],math.prod(math.comb(n,b) for n,b in zip(ns,a))) for a in points]
 for var,w in weighted:
  if w>334:s.add(z3.Not(var))
 s.add(z3.Or(*[z3.PbEq(weighted,w) for w in (322,326,330,334)]))
 tt=time.time();res=s.check();results.append((ns,str(res),time.time()-tt));print(results[-1],flush=True)
 if res==z3.sat:
  model=s.model();active={a for a in points if z3.is_true(model.eval(f[a]))};support=[]
  for x in range(1<<15):
   a=[];off=0
   for n in ns:a.append(((x>>off)&((1<<n)-1)).bit_count());off+=n
   if tuple(a) in active:support.append(x)
  assert len(support) in (322,326,330,334)
  table=[int(x in set(support)) for x in range(1<<15)]
  for i in range(15):
   for x in range(1<<15):
    if x>>i&1:table[x]^=table[x^(1<<i)]
  assert max(x.bit_count() for x,v in enumerate(table) if v)<=8
  json.dump({'partition':ns,'support':support},open('workspace/agent2_symmetric4_HIT.json','w'));print('VERIFIED HIT',len(support),flush=True);break
json.dump(results,open('workspace/agent2_symmetric4_results.json','w'));print('seconds',time.time()-t0)
Path('workspace/agent2_symmetric4.py').write_text(Path(__file__).read_text())
