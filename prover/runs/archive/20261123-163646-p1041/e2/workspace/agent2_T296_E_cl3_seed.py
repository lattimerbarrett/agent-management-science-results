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
 ex,rk=closure(set(F),veronese(12,3));print('cl3extras',len(ex));json.dump({'support':F,'cl3extra':[p for p,c in ex]},open('workspace/agent2_T296_E_cl3_seed.json','w'));break
