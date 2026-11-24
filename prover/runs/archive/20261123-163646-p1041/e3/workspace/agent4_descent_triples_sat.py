import z3,numpy as np,itertools,time,pathlib,json
pathlib.Path('workspace/agent4_descent_triples_sat.py').write_text(pathlib.Path(__file__).read_text())
src=pathlib.Path('workspace/agent4_descent_smallsearch.py').read_text();exec(src[src.index('start=time.time()'):src.index('rng=np.random')])
s=z3.With(z3.Tactic('sat'),anf=True,**{'anf.exlin':True,'cardinality.solver':True}).solver();s.set(timeout=30000)
def xor(v):
 a=z3.BoolVal(False)
 for b in v:a=z3.Xor(a,b)
 return a
def less(a,b):
 return z3.Or([z3.And(z3.Not(a[i]),b[i],*[a[j]==b[j] for j in range(i+1,4)]) for i in range(4)])
AA=[[z3.Bool('a%d_%d'%(b,i)) for i in range(4)] for b in range(16)]
BB=[[z3.Bool('b%d_%d'%(b,i)) for i in range(4)] for b in range(16)]
CC=[[z3.Xor(a,b) for a,b in zip(aa,bb)] for aa,bb in zip(AA,BB)]
active=[];f=[]
for b in range(16):
 aa,bb,cc=AA[b],BB[b],CC[b];t=z3.Bool('t%d'%b);s.add(t==z3.Or(aa));active.append(t)
 s.add(z3.Or(z3.And(*[z3.Not(v) for v in aa+bb]),z3.And(z3.Or(aa),less(aa,bb),less(bb,cc))))
 for z in range(16):
  terms=[z3.And(*[v if z&(1<<i) else z3.Not(v) for i,v in enumerate(row)]) for row in [aa,bb,cc]]
  q=z3.Bool('f%d'%((b<<4)|z));s.add(q==xor(terms));f.append(q)
for b,va,vb in [(0,1,2),(1,4,8)]:
 for i in range(4):s.add(AA[b][i]==z3.BoolVal(bool(va&(1<<i))),BB[b][i]==z3.BoolVal(bool(vb&(1<<i))))
s.add(z3.PbLe([(t,1) for t in active],11),z3.PbGe([(t,1) for t in active],8))
for J in itertools.combinations(range(4),2):
 M=[xor([z3.And(*[row[i] for i in J]) for row in [AA[b],BB[b],CC[b]]]) for b in range(16)]
 s.add(z3.Not(xor(M)))
 for k in range(4):s.add(z3.Not(xor([M[b] for b in range(16) if b&(1<<k)])))
for J in itertools.combinations(range(4),3):s.add(z3.Not(xor([z3.And(*[row[i] for i in J]) for b in range(16) for row in [AA[b],BB[b],CC[b]]])))
cuts=set()
def cut(points):
 key=tuple(sorted(map(int,points)))
 if key in cuts:return
 cuts.add(key);s.add(z3.PbLe([(f[x],1) for x in key],8))
for free in itertools.combinations(range(8),4):
 fixed=[i for i in range(8) if i not in free];vv=[sum(((v>>j)&1)<<free[j] for j in range(4)) for v in range(16)]
 for b in range(16):
  base=sum(((b>>j)&1)<<fixed[j] for j in range(4));cut([base^v for v in vv])
print('built',len(cuts),time.time()-start,flush=True);hist=[];result='budget';witness=None
for iteration in range(10000):
 if time.time()-start>180:break
 r=s.check()
 if r!=z3.sat:result=str(r);break
 model=s.model();S=np.array([int(z3.is_true(model.eval(v))) for v in f],dtype=np.int16);w=int(S.sum());arr=S.copy()
 for j in range(8):
  for x in range(256):
   if x&(1<<j):arr[x]^=arr[x^(1<<j)]
 assert max(x.bit_count() for x in range(256) if arr[x])<=4
 wal=fwht(S);hits=fwht(wal[spaces]);assert np.all(hits%16==0);hits//=16;viol=np.flatnonzero(hits>8);mx=int(hits.max());hist.append([w,mx,len(viol)])
 if not len(viol):result='SAT_counterexample';witness=np.flatnonzero(S).tolist();break
 if len(viol)>2000:
  vals=hits.ravel()[viol];viol=viol[np.argpartition(vals,-2000)[-2000:]]
 for v in viol:
  row,k=divmod(int(v),16);char=np.array([(k>>j)&1 for j in range(4)],dtype=np.uint8);mask=np.all(parity[np.bitwise_and(basis[row,:,None],xs[None,:])]==char[:,None],axis=0)
  pts=np.flatnonzero(mask);assert len(pts)==16 and int(S[pts].sum())>8;cut(pts)
 if iteration%10==0:print(iteration,w,mx,len(cuts),time.time()-start,flush=True)
res={'result':result,'iterations':iteration+1,'cuts':len(cuts),'seconds':time.time()-start,'hist':hist,'counterexample':witness,'meaning':'canonical-triple oddfiber RM4,8 wt<=38 localmin withtwo disjointfiberplanes'}
pathlib.Path('workspace/agent4_descent_triples_sat.json').write_text(json.dumps(res,indent=2));print(res)
if result=='unsat':pathlib.Path('workspace/agent4_descent_triples_sat_cuts.json').write_text(json.dumps(sorted(cuts)))
