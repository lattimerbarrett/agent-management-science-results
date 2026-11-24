import json,sys,pathlib,collections,time
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese,closure

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out
v123=veronese(12,3);v125=veronese(12,5);v134=veronese(13,4);v135=veronese(13,5);P6hist=collections.Counter();P6bad=[];F296hist=collections.Counter();processed=0

def process(F):
 global processed
 E,r=closure(set(F),v123);E=[p for p,c in E];assert len(E)==12
 KK=kernel(F+E,v125);BB={}
 for c in KK:
  z=c>>296
  while z:
   j=z.bit_length()-1
   if j in BB:z^=BB[j][0];c^=BB[j][1]
   else:BB[j]=(z,c);break
 C=[0]
 for z,c in BB.values():C +=[x^c for x in C]
 enum=collections.Counter((c>>296).bit_count() for c in C);assert enum=={0:1,4:3,6:24,8:3,12:1}
 F296hist[len(E),tuple(sorted(enum.items()))]+=1
 for c in C:
  if (c>>296).bit_count()!=6:continue
  P={p for i,p in enumerate(E) if c>>(296+i)&1};SS=set(F);p0=min(P)
  periods=[v for v in [p0^p for p in P if p!=p0] if all(p^v in P for p in P)]
  assert len(periods)==1
  v=periods[0];common=all(p^v in SS for p in SS);P6hist[common]+=1
  if not common:P6bad.append({'support':F,'P':list(P),'v':v})
 processed+=1
 if processed%2000==0:print('processed',processed,'hist',P6hist,'sec',time.time()-t,flush=True)
D=json.load(open('workspace/agent2_T288_E_ALLgraph_cl3.json'))['hits'];P=json.load(open('workspace/agent2_T288_E_cl3_relative.json'))['small'];v=veronese(11,5);u=veronese(12,5);u4=veronese(12,4);u6=veronese(12,6);hist=collections.Counter();leaves=[];t=time.time();old=-1
for ix,r in enumerate(P):
 si=r['source'];S=D[si]['support']
 if si!=old:
  B={}
  for i,p in enumerate(S):
   z=v[p];c=1<<i
   while z:
    k=z.bit_length()-1
    if k not in B:B[k]=(z,c);break
    z^=B[k][0];c^=B[k][1]
  old=si
 z=0
 for p in r['subset']:z^=v[p]
 c=0
 while z:
  k=z.bit_length()-1;assert k in B;z^=B[k][0];c^=B[k][1]
 H=set(r['subset'])|{p for i,p in enumerate(S) if c>>i&1};F=sorted(H|{p|2048 for p in set(S)^H});assert len(F)==296
 syn=0
 for p in F:syn^=u6[p]
 assert syn==0
 process(F)
print('DONE',processed,'P6hist',P6hist,'bad',len(P6bad),'sec',time.time()-t)
json.dump({'F296hist':{str(k):v for k,v in F296hist.items()},'P6hist':{str(k):v for k,v in P6hist.items()},'bad':P6bad},open('workspace/agent2_T308_E296_P6_periods.json','w'))
