import networkx as nx,numpy as np,json,itertools,time
F=nx.node_link_graph(json.load(open('workspace/agent2_b_vs_clique_counter_min.json')));vs=sorted(F);n=len(vs);ix={v:i for i,v in enumerate(vs)};root=ix[29];nm=[sum(1<<ix[w] for w in F[v]) for v in vs];FULL=(1<<n)-1;pop=np.array([i.bit_count() for i in range(256)],dtype=np.uint8)
profiles={};totalvalid=0;totalcandidates=0;t0=time.time()
def comps(mask):
 out=[]
 while mask:
  bit=mask&-mask;cc=bit;front=bit
  while front:
   j=(front&-front).bit_length()-1;front &=front-1;new=nm[j]&mask&~cc;cc|=new;front|=new
  mask &=~cc;out.append(cc)
 return out
for lo in range(0,1<<n,1<<18):
 a=np.arange(lo,min(lo+(1<<18),1<<n),dtype=np.uint32);valid=np.ones(len(a),dtype=bool)
 for v in range(n):
  q=a&np.uint32(nm[v]);bad=((a>>v)&1)!=0;bad &= (q&(q-np.uint32(1)))!=0;valid &=~bad
 a=a[valid];totalvalid+=len(a)
 if not len(a):continue
 b=np.uint32(FULL)^a;active=np.zeros(len(a),dtype=np.uint32)
 for v in range(n):active |= np.where((((b>>v)&1)!=0)&((b&np.uint32(nm[v]))!=0),np.uint32(1<<v),np.uint32(0))
 pc=pop[active.view(np.uint8).reshape(-1,4)].sum(axis=1);a=a[pc<=6];totalcandidates+=len(a)
 for aa in a:
  aa=int(aa);bb=FULL^aa;cs=comps(bb);big=[c.bit_count() for c in cs if c.bit_count()>=3];ne=sum(c.bit_count()==2 for c in cs)
  if sum(big)+2*max(0,ne-1)>4:continue
  if aa>>root&1:p=('A',(aa&nm[root]).bit_count(),0,tuple(sorted(big)),ne)
  else:
   rc=next(c for c in cs if c>>root&1);sz=rc.bit_count();obig=big.copy();one=ne
   if sz>=3:obig.remove(sz)
   elif sz==2:one-=1
   p=('B',0,sz,tuple(sorted(obig)),one)
  profiles[p]=profiles.get(p,0)+1
 if lo%(1<<22)==0:print('lo',lo,'profiles',len(profiles),'t',time.time()-t0,flush=True)
print('TOTALS',n,totalvalid,totalcandidates,'profiles',len(profiles),'sec',time.time()-t0,flush=True)
for p,c in sorted(profiles.items()):print(p,c)
feasible=[]
for p,q in itertools.product(profiles,repeat=2):
 if p[0]!=q[0]:continue
 if p[0]=='A':
  if p[1]+q[1]>1:continue
  big=list(p[3]+q[3]);ne=p[4]+q[4]
 else:
  rc=p[2]+q[2]-1;big=list(p[3]+q[3]);ne=p[4]+q[4]
  if rc>=3:big.append(rc)
  elif rc==2:ne+=1
 if sum(big)+2*max(0,ne-1)<=4:feasible.append((p,q))
print('FEASIBLE GLUED T',feasible)
assert not feasible
json.dump({'n':n,'valid_matching_A':totalvalid,'candidates_Bactive6':totalcandidates,'profiles':[(list(p),c) for p,c in profiles.items()]},open('workspace/agent2_T_exhaustive_certificate.json','w'))
