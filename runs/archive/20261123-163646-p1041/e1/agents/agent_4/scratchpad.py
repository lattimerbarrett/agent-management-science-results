import numpy as np,itertools,time,json,pickle,random,collections
start=time.time();random.seed(4430);N=16384;cols=pickle.load(open('workspace/a1_cols14_degree6.pkl','rb'));masks=[3868,13894,5737];F=0
for m in masks:
 ps=[0]
 for j in range(14):
  if m>>j&1:ps +=[x^(1<<j) for x in ps]
 for x in ps:F^=1<<x
assert F.bit_count()==336
FB=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little');cells={}
for i in range(14):
 mem=sum(1<<j for j,m in enumerate(masks) if m>>i&1)
 if mem:cells.setdefault(mem,1<<i)
vs=list(cells.values());W=[0]
for b in vs:W +=[x^b for x in W]
assert len(W)==128
v=128;S0=set(np.flatnonzero(FB).tolist());seen={hash(F)};sigs=set();out=[];stats=collections.Counter();X=[sum(1<<j for j in range(N) if j>>i&1) for i in range(14)];ALL=(1<<N)-1
def mob(f):
 for i in range(14):f^=(f&(ALL^X[i]))<<(1<<i)
 return f
def signature(f):
 a=1-2*np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').astype(np.int32)
 for h in [1<<i for i in range(14)]:
  b=a.reshape(-1,2*h);u=b[:,:h].copy();q=b[:,h:].copy();b[:,:h]=u+q;b[:,h:]=u-q
 return tuple(zip(*np.unique(np.abs(a),return_counts=True)))
def fullhull(f):
 ss=np.flatnonzero(np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little'));bas={};s0=int(ss[0])
 for x in ss:
  z=int(x)^s0
  while z and z.bit_length()-1 in bas:z^=bas[z.bit_length()-1]
  if z:bas[z.bit_length()-1]=z
  if len(bas)==14:return True
 return False
sigs.add(signature(F))
for wi,w in enumerate(W[1:]):
 p=(w&-w).bit_length()-1;R=[r for r in range(N) if not r&v and not r&(1<<p)];P=np.array([[r,r^w,r^v,r^w^v] for r in R],dtype=np.int64);patterns=FB[P];perms=[]
 for comb in itertools.combinations(range(4),3):
  for cyc in [comb,(comb[0],comb[2],comb[1])]:
   perm=list(range(4))
   for a,b in zip(cyc,cyc[1:]+cyc[:1]):perm[b]=a
   delta=patterns^patterns[:,perm];inds=np.flatnonzero(np.any(delta,axis=1));pairs=[]
   for j in inds:
    pts=P[j,np.flatnonzero(delta[j])];assert len(pts)==2;pairs.append(tuple(map(int,pts)))
   bas={};K=[]
   for j,(a,b) in enumerate(pairs):
    vv=cols[a]^cols[b];rel=1<<j
    while vv:
     pp=vv.bit_length()-1
     if pp not in bas:bas[pp]=(vv,rel);break
     aa,bb=bas[pp];vv^=aa;rel^=bb
    if not vv:K.append(rel)
   stats[len(K)]+=1;KG=[]
   for rr in K:
    gg=0
    while rr:
     lo=rr&-rr;j=lo.bit_length()-1;aa,bb=pairs[j];gg^=(1<<aa)|(1<<bb);rr^=lo
    KG.append(gg)
   g=F;prevgray=0
   for sample in range(1<<len(KG)):
    gray=sample^(sample>>1)
    if sample:g^=KG[(gray^prevgray).bit_length()-1]
    prevgray=gray
    hh=hash(g)
    if hh in seen:continue
    seen.add(hh)
    if not fullhull(g):continue
    sig=signature(g)
    if sig in sigs:continue
    sigs.add(sig);aa=mob(g);assert g.bit_count()==336 and max(j.bit_count() for j in range(N) if aa>>j&1)<=7
    out.append({'weight':336,'truth_hex':hex(g),'anf_hex':hex(aa),'outside_direction':v,'inside_direction':w,'cycle':cyc});print('NEW fullhull',len(out),'wi',wi,'w',w,'K',len(K),'sec',time.time()-start,flush=True);json.dump(out,open('workspace/agent4_generalplane_3cycle336_sources.json','w'))
 if wi%20==0:print('wi',wi,'tested',len(seen),'new',len(out),'stats',stats,'sec',time.time()-start,flush=True)
print('DONE',len(out),stats,'sec',time.time()-start)
open('workspace/agent4_generalplane_3cycle336_search.py','w').write(open(__file__).read())
