import z3,time,json,itertools,pathlib
z3.set_param('memory_max_size',2800)
start=time.time();n=14;N=1<<n;r=7
s=z3.With(z3.Tactic('sat'),anf=True,**{'anf.exlin':True,'cardinality.solver':True}).solver();s.set(timeout=210000)
f=[z3.Bool('f_%d'%i) for i in range(N)];a=f[:]
for j in range(n):
 bit=1<<j
 for x in range(N):
  if x&bit:
   t=z3.Bool('a_%d_%d'%(j,x));s.add(t==z3.Xor(a[x],a[x^bit]));a[x]=t
for x in range(N):
 if x.bit_count()>7:s.add(z3.Not(a[x]))
s.add(a[127])
for j in range(7):
 mask=127^(1<<j);s.add(a[mask])
 for b in range(7):s.add(z3.Not(a[mask|(1<<(7+b))]))
for b in [0,1,2,3,4,8,16]:
 s.add(f[b<<7])
 for y in range(1,128):s.add(z3.Not(f[(b<<7)|y]))
s.add(z3.PbGe([(v,1) for v in f],322),z3.PbLe([(v,1) for v in f],334))
lo=z3.BoolVal(False);hi=z3.BoolVal(False)
for i,v in enumerate(f):
 nl=z3.Bool('lo_'+str(i));nh=z3.Bool('hi_'+str(i));s.add(nl==z3.Xor(lo,v),nh==z3.Xor(hi,z3.And(lo,v)));lo,hi=nl,nh
s.add(z3.Not(lo),hi)
print('anf+weight built',time.time()-start,flush=True)
for d in range(1,128):
 terms=[(z3.And(f[(b<<7)|y],f[(b<<7)|(y^d)]),1) for b in range(128) for y in range(128) if y<(y^d)]
 s.add(z3.PbLe(terms,7))
 if d%16==0:print('directions',d,'seconds',time.time()-start,flush=True)
print('built',time.time()-start,flush=True)
res=s.check();out={'result':str(res),'seconds':time.time()-start,'meaning':'normalized RM7,14 target weights with p<=7 on all127 fiber directions only'}
if res==z3.unknown:out['reason']=s.reason_unknown()
if res==z3.sat:
 m=s.model();supp=[i for i,v in enumerate(f) if z3.is_true(m.eval(v))];out['support']=supp
 S=set(supp);assert len(S) in [322,326,330,334]
 vals=[int(i in S) for i in range(N)]
 for j in range(n):
  for x in range(N):
   if x>>j&1:vals[x]^=vals[x^(1<<j)]
 assert max(i.bit_count() for i,v in enumerate(vals) if v)<=7
 for d in range(1,128):assert sum(1 for p in S if p<(p^d) and p^d in S)<=7
print(out,flush=True)
pathlib.Path('workspace/agent1_maxpair_normalized_status.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent1_maxpair_normalized_sat.py').write_text(pathlib.Path(__file__).read_text())
