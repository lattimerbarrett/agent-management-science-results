import z3,numpy as np,itertools,time,pathlib,json
pathlib.Path('workspace/agent4_descent_lazy_sat.py').write_text(pathlib.Path(__file__).read_text())
src=pathlib.Path('workspace/agent4_descent_smallsearch.py').read_text();exec(src[src.index('start=time.time()'):src.index('rng=np.random')])
s=z3.With(z3.Tactic('sat'),anf=True,**{'anf.exlin':True,'cardinality.solver':True}).solver();s.set(timeout=30000)
f=[z3.Bool('f%d'%i) for i in range(256)];a=f[:]
for j in range(8):
 for x in range(256):
  if x&(1<<j):
   v=z3.Bool('a%d_%d'%(j,x));s.add(v==z3.Xor(a[x],a[x^(1<<j)]));a[x]=v
for x in range(256):
 if x.bit_count()>4:s.add(z3.Not(a[x]))
s.add(a[15])
for j in range(4):
 mask=15^(1<<j);s.add(a[mask])
 for b in range(4):s.add(z3.Not(a[mask|(1<<(4+b))]))
for ell in range(1,16):s.add(z3.Or([f[(b<<4)|z] for b in range(16) for z in range(1,16) if (ell&z).bit_count()%2]))
s.add(z3.PbLe([(v,1) for v in f],38));s.add(z3.PbLe([(f[b<<4],1) for b in range(16)],8))
cuts=set()
def cut(points):
 key=tuple(sorted(map(int,points)))
 if key in cuts:return
 cuts.add(key);s.add(z3.PbLe([(f[x],1) for x in key],8))
for free in itertools.combinations(range(8),4):
 fixed=[i for i in range(8) if i not in free]
 vv=[sum(((v>>j)&1)<<free[j] for j in range(4)) for v in range(16)]
 for b in range(16):
  base=sum(((b>>j)&1)<<fixed[j] for j in range(4));cut([base^v for v in vv])
print('builtSAT',len(cuts),time.time()-start,flush=True);hist=[];result='budget';witness=None
for iteration in range(100000):
 if time.time()-start>240:break
 r=s.check()
 if r!=z3.sat:result=str(r);break
 model=s.model();S=np.array([int(z3.is_true(model.eval(v))) for v in f],dtype=np.int16);w=int(S.sum());wal=fwht(S);hits=fwht(wal[spaces]);assert np.all(hits%16==0);hits//=16
 viol=np.flatnonzero(hits>8);mx=int(hits.max());hist.append([w,mx,len(viol)])
 if not len(viol):result='SAT_counterexample';witness=np.flatnonzero(S).tolist();break
 # strongest 2000 cuts, all exact valid minflat inequalities
 if len(viol)>2000:
  vals=hits.ravel()[viol];viol=viol[np.argpartition(vals,-2000)[-2000:]]
 for v in viol:
  row,k=divmod(int(v),16);char=np.array([(k>>j)&1 for j in range(4)],dtype=np.uint8)
  mask=np.all(parity[np.bitwise_and(basis[row,:,None],xs[None,:])]==char[:,None],axis=0)
  pts=np.flatnonzero(mask);assert len(pts)==16 and int(S[pts].sum())>8;cut(pts)
 if iteration%10==0:print(iteration,w,mx,len(cuts),time.time()-start,flush=True)
res={'result':result,'iterations':iteration+1,'cuts':len(cuts),'seconds':time.time()-start,'hist':hist,'counterexample':witness,'meaning':'fullspan RM4,8 weight<=38 localmin normalized oddfibers'}
pathlib.Path('workspace/agent4_descent_lazy_sat.json').write_text(json.dumps(res,indent=2));print(res)
if result=='unsat':pathlib.Path('workspace/agent4_descent_lazy_sat_cuts.json').write_text(json.dumps(sorted(cuts)))
