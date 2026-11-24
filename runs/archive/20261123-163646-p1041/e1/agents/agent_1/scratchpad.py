import pickle,json,itertools,time,random,collections,numpy as np,z3
random.seed(4147);cols=pickle.load(open('workspace/a1_cols14_degree6.pkl','rb'));seeds=json.load(open('workspace/agent4_flat_seeds.json'));start=time.time();N=16384

def span(B):
 p=[0]
 for b in B:p +=[x^b for x in p]
 return p
def pts(b):
 p=[]
 while b:t=b&-b;p.append(t.bit_length()-1);b^=t
 return p
def nullrelations(vs):
 piv={};K=[]
 for k,v in enumerate(vs):
  r=1<<k
  while v:
   h=v.bit_length()-1
   if h not in piv:piv[h]=(v,r);break
   a,b=piv[h];v^=a;r^=b
  if not v:K.append(r)
 return K
def xor(xs):
 if not xs:return z3.BoolVal(False)
 while len(xs)>1:xs=[z3.Xor(xs[k],xs[k+1]) if k+1<len(xs) else xs[k] for k in range(0,len(xs),2)]
 return xs[0]
def cnpoint(x,i,j):return x^(((x>>j)&1)<<i)
def rank(B):
 pp={}
 for b in B:
  while b:
   h=b.bit_length()-1
   if h not in pp:pp[h]=b;break
   b^=pp[h]
 return len(pp)
found={};cases=[('336',0,7),('340',2,6),('340',2,12),('346',5,12),('346',0,1),('354',1,8),('358',3,13),('370',1,12),('382',0,1)]
for ci,(ww,i,j) in enumerate(cases):
 w=int(ww);S=set()
 for m in seeds[ww]:S.symmetric_difference_update(span([1<<i for i in range(14) if m>>i&1]))
 ab=[0,1<<i,1<<j,(1<<i)^(1<<j)];U=sorted({x^a for x in S for a in ab});umap={x:k for k,x in enumerate(U)}
 if rank([x^U[0] for x in U])<14:print('SKIPhull',ww,i,j,flush=True);continue
 K=nullrelations([cols[x] for x in U]);fibers={z:([umap[z^a] for a in ab],sum((z^a)in S for a in ab)) for z in U if not(z>>i&1 or z>>j&1)};fibs=list(fibers.values());full=[k for inds,t in fibs if t==4 for k in inds];cons=[]
 for r in K:
  v=sum(((r>>k)&1)<<q for q,k in enumerate(full))
  for q,(inds,t) in enumerate(fibs):v|=(sum((r>>k)&1 for k in inds)%2)<<(len(full)+q)
  cons.append(v)
 KK=[]
 for rel in nullrelations(cons):
  r=0
  for k in pts(rel):r^=K[k]
  KK.append(r)
 K=KK;bs=[z3.Bool('b%d_%d'%(ci,k)) for k in range(len(K))];pbits=[[] for _ in U]
 for k,r in enumerate(K):
  for p in pts(r):pbits[p].append(bs[k])
 pbits=[xor(a) for a in pbits];fbits=[z3.Not(pbits[k]) if x in S else pbits[k] for k,x in enumerate(U)];solver=z3.SolverFor('QF_FD');solver.set(timeout=3000)
 for inds,t in fibs:
  pp=[fbits[k] for k in inds]
  if t==1:solver.add(z3.AtMost(*pp,1))
  elif t==3:solver.add(z3.AtMost(*[z3.Not(p) for p in pp],1))
  elif t==2:solver.add(z3.Or(*pp),z3.Or(*[z3.Not(p) for p in pp]))
 hlist=[]
 for m in seeds[ww]:
  H=span([1<<k for k in range(14) if m>>k&1]);hlist.append(H)
  for _ in range(4):
   HH=H.copy()
   for _ in range(random.choice([1,2,3])):
    a,b=random.sample(range(14),2);HH=[cnpoint(x,a,b) for x in HH]
   hlist.append(HH)
 print('MODEL',ww,(i,j),'U',len(U),'Kclean',len(K),'fibers',len(fibs),'Hcases',len(hlist),'time',time.time()-start,flush=True)
 for hi,H in enumerate(hlist):
  pp=[fbits[umap[x]] for x in H if x in umap]
  if len(pp)<(w+128-334)//2:continue
  solver.push();solver.add(z3.Or(*[z3.PbEq([(p,1) for p in pp],(w+128-t)//2) for t in [322,326,330,334] if t not in found]));res=solver.check()
  if res==z3.sat:
   model=solver.model();r=0
   for k,b in enumerate(bs):
    if z3.is_true(model.eval(b,model_completion=True)):r^=K[k]
   FF=0
   for k,x in enumerate(U):
    if (x in S)^bool(r>>k&1):FF|=1<<x
   assert FF.bit_count()==w
   TT=FF^sum(1<<x for x in H);t=TT.bit_count();assert t in [322,326,330,334]
   anf=np.unpackbits(np.frombuffer(TT.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for d in range(14):anf.reshape(-1,2,1<<d)[:,1,:]^=anf.reshape(-1,2,1<<d)[:,0,:]
   assert all(not b or x.bit_count()<=7 for x,b in enumerate(anf));found[t]={'truth_hex':hex(TT),'fiber_word_hex':hex(FF),'H_points':H,'base_masks':seeds[ww],'pair':[i,j]};json.dump(found,open('workspace/a1_fullfiber_SAT_found.json','w'));print('FOUND',t,flush=True)
  solver.pop();print('CASE',ww,(i,j),hi,str(res),'time',time.time()-start,flush=True)
  if len(found)==4:raise SystemExit
print('DONE',list(found),'time',time.time()-start)
