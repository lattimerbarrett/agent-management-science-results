import itertools,random,json,time
D=json.load(open('workspace/agent4_flat_seeds.json'));basew=342;oldflats=D[str(basew)];targets={t:(basew+128-t)//2 for t in [322,326,330,334]};found={};start=time.time()
def ptsflat(free):
 s=free;p=[]
 while True:
  p.append(s)
  if not s:return p
  s=(s-1)&free
S=set();ANF=set();flatpoints=[]
for free in oldflats:
 pts=ptsflat(free);S^=set(pts);flatpoints.append(pts);fixed=16383^free
 for t in ptsflat(fixed):
  if t in ANF:ANF.remove(t)
  else:ANF.add(t)
for i in range(7):
 ib=1<<i;others=[j for j in range(14) if j!=i];monomials=[0]+[1<<j for j in others]+[(1<<j)|(1<<k) for j,k in itertools.combinations(others,2)];M=len(monomials)
 deriv=[s^ib for s in ANF if s&ib and s.bit_count()==7];highs={};cols=[]
 for mon in monomials:
  col=0
  for d in deriv:
   union=d|mon
   if union.bit_count()>7:
    if union not in highs:highs[union]=len(highs)
    col^=1<<highs[union]
  cols.append(col)
 piv={};qbasis=[]
 for j,c in enumerate(cols):
  rel=1<<j
  while c:
   k=c.bit_length()-1
   if k in piv:c^=piv[k][0];rel^=piv[k][1]
   else:piv[k]=(c,rel);break
  if not c:qbasis.append(rel)
 print('direction',i,'kernel',len(qbasis),flush=True)
 for trial in range(500):
  fi=random.randrange(len(oldflats));free=oldflats[fi];pp=flatpoints[fi]
  eq=random.randrange(1,16384)&free
  if not eq:continue
  H=[x for x in pp if (x&eq).bit_count()%2==0]
  if len(H)!=64:continue
  while True:
   ext=random.randrange(16384)
   if ext&~free:break
  shift=0 if random.randrange(2) else next(x for x in pp if(x&eq).bit_count()%2)
  F=[x^shift for x in H]+[x^shift^ext for x in H]
  base=sum((x in S)<<k for k,x in enumerate(F));dm=sum(((x in S)^((x^ib)in S))<<k for k,x in enumerate(F))
  lm={j:sum(((x>>j)&1)<<k for k,x in enumerate(F)) for j in others}
  em=[(1<<128)-1]+[lm[j] for j in others]+[lm[j]&lm[k] for j,k in itertools.combinations(others,2)]
  ev=[]
  for qb in qbasis:
   v=0
   for j,e in enumerate(em):
    if qb>>j&1:v^=e
   ev.append(v&dm)
  # image RREF, retainrelationq
  image={}
  for v,q in zip(ev,qbasis):
   while v:
    k=v.bit_length()-1
    if k in image:v^=image[k][0];q^=image[k][1]
    else:image[k]=(v,q);break
  B=list(image.values())
  if all(v.bit_count()%2==0 for v,q in B) and all((z-base.bit_count())%2 for z in targets.values()):continue
  val=base;q=0
  for sample in range(1<<len(B)):
   if sample:
    bit=(sample&-sample).bit_length()-1;val^=B[bit][0];q^=B[bit][1]
   I=val.bit_count()
   ts=[t for t,z in targets.items() if I==z]
   for t in ts:
    found[t]={'flats':oldflats,'direction':i,'qmonomials':[monomials[j] for j in range(M) if q>>j&1],'added_points':F,'intersection':I}
    del targets[t];print('FOUND',t,found[t],flush=True);json.dump(found,open('workspace/agent2_directshear_seeds.json','w'))
   if not targets:break
  if not targets:break
 if not targets:break
 print('progress',i,time.time()-start,flush=True)
print('remain',targets,time.time()-start)
open('workspace/agent2_directshear_search.py','w').write(open(__file__).read())
