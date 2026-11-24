import sys,itertools,json,pathlib,time,collections,numpy as np,random
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

def ins(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0
D=json.load(open('workspace/agent4_T288_quadgraph_P16.json'));seed=next(s for r in D['results'] for s in r['seeds'] if s['K5']==14);S=sorted(seed['support']);K=kernel(S,veronese(11,5));B={};AB=[]
for j in range(-1,11):
 u=ins(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
 if u:AB.append(u)
assert len(AB)==12
E=[]
for u in K:
 r=ins(B,u)
 if r:E.append(r)
assert len(E)==2
A=[0]
for u in AB:A +=[v^u for v in A]
NA=[u^E[0] for u in A];NB=[u^E[1] for u in A];NC=[u^E[0]^E[1] for u in A];wa=np.array([u.bit_count() for u in NA]);wn=np.array([u.bit_count() for u in NB]);wx=np.array([u.bit_count() for u in NC]);J=np.arange(4096);hits=[];count=0;mins=1000
for i in range(4096):
 ints=(wa[i]+wn-wx[i^J])//2;mins=min(mins,int(ints.min()));jj=np.where(ints==16)[0];count+=len(jj)
 for j in jj:hits.append((i,int(j)))
print('PAIRCOUNT',count,'min',mins,flush=True)
random.seed(3115);random.shuffle(hits);start=time.time();hist=collections.Counter();results=[]
for ii,(i,j) in enumerate(hits[:1000]):
 h=NA[i];k=NB[j];G=[]
 for q,p in enumerate(S):
  hh=(h>>q)&1;kk=(k>>q)&1
  if hh:G.append(p|2048)
  if kk:G.append(p|4096)
  if 1^hh^kk:G.append(p|6144)
 assert len(G)==320;G.sort();KK=kernel(G,veronese(13,5));nz=sum((u&v).bit_count()%2 for u in KK for v in KK);hist[(len(KK),bool(nz))]+=1
 if nz:
  cl,r=closure(set(G),veronese(13,5));ans={'source':S,'hidx':i,'kidx':j,'support':G,'K5':len(KK),'Gram_nonzero':nz,'cl5extra':len(cl)};results.append(ans);print('NONSELF320',ii,len(KK),len(cl),flush=True)
  json.dump(results,open('workspace/agent1_new320_quadratic_K14_hits.json','w'))
 if ii%100==0:print('progress',ii,dict(hist),time.time()-start,flush=True)
json.dump({'paircount':count,'minintersection':mins,'sampled':min(1000,len(hits)),'Kgram_hist':{str(k):v for k,v in hist.items()},'results':results},open('workspace/agent1_new320_quadratic_K14_results.json','w'))
