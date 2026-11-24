import sys,itertools,json,pathlib,time,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

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

def insert(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0
D=json.load(open('workspace/agent4_T288_quadgraph_P16.json'));v10=veronese(10,5);v114=veronese(11,3);v115=veronese(11,5);start=time.time();stats=[];hits=[]
for res in D['results']:
 a=res['a'];T=[]
 for x in range(256):
  q1=(x&1)*(x>>1&1);q2=((x&1)*(x>>2&1))^((x>>1&1)*(x>>3&1) if a==4 else 0);T.append(x|(q1<<8)|(q2<<9))
 K=kernel(T,v10);B={}
 for j in range(-1,10):insert(B,sum(1<<i for i,p in enumerate(T) if j==-1 or p>>j&1))
 extra=[]
 for u in K:
  r=insert(B,u)
  if r:extra.append(r)
 assert len(extra)==(6 if a==3 else 2)
 labels=[0]
 for u in extra:labels +=[z^u for z in labels]
 hist=collections.Counter();ct=0
 for seedid,seed in enumerate(res['seeds']):
  S0=set(seed['support'])
  for labid,u in enumerate(labels):
   S=set(S0)
   for i,p in enumerate(T):
    if u>>i&1:S.symmetric_difference_update([p,p|1024])
   S=sorted(S);assert len(S)==288
   K4=kernel(S,v114);K5=kernel(S,v115);nz=sum((x&y).bit_count()%2 for x in K4 for y in K5)
   X,rr=closure(set(S),v114);assert not X
   hist[(len(K4),len(K5),bool(nz))]+=1;ct+=1
   if nz:
    hits.append({'a':a,'seed':seedid,'label':labid,'support':S,'K4':len(K4),'K5':len(K5),'cross_nonzero':nz})
    print('CROSSHIT',a,seedid,labid,len(K4),len(K5),nz,flush=True)
 stats.append({'a':a,'extraK':len(extra),'Pcases':len(res['seeds']),'hclasses':len(labels),'total':ct,'hist':{str(k):v for k,v in hist.items()}});print(stats[-1],time.time()-start,flush=True)
json.dump({'stats':stats,'hits':hits},open('workspace/agent1_T288_quadgraph_ALLh_K3.json','w'))
