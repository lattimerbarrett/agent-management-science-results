import sys,itertools,json,time,collections,pathlib
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

def extra(S,m,K):
 B={}
 for j in range(-1,m):insert(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
 out=[]
 for v in K:
  z=insert(B,v)
  if z:out.append(z)
 return out
D=json.load(open('workspace/agent4_T288_quadgraph_P16.json'));v10=veronese(10,5);v115=veronese(11,5);v125=veronese(12,5);v123=veronese(12,3)
stats=collections.Counter();out=[];count=0;t0=time.time()
for res in D['results']:
 a=res['a'];T=[]
 for x in range(256):
  q1=(x&1)*(x>>1&1);q2=((x&1)*(x>>2&1))^((x>>1&1)*(x>>3&1) if a==4 else 0);T.append(x|(q1<<8)|(q2<<9))
 ext=extra(T,10,kernel(T,v10));labs=[0]
 for u in ext:labs += [v^u for v in labs]
 for sid,seed in enumerate(res['seeds']):
  for lid,u in enumerate(labs):
   S=set(seed['support'])
   for i,p in enumerate(T):
    if u>>i&1:S.symmetric_difference_update([p,p|1024])
   S=sorted(S);K=kernel(S,v115)
   if len(K)!=14:continue
   ex=extra(S,11,K);assert len(ex)==2
   for wid,w in enumerate([ex[0],ex[1],ex[0]^ex[1]]):
    U=[p|(((w>>i)&1)<<11) for i,p in enumerate(S)];KU=kernel(U,v125);cl,rk=closure(set(U),v123);stats[a,len(KU),len(cl)]+=1;count+=1
    if cl:
     out.append({'a':a,'seed':sid,'hlabel':lid,'graphlabel':wid,'support':U,'K5':len(KU),'cl3extra':[p for p,c in cl]})
    if len(KU)>13:print('NONTERMINAL',a,sid,lid,wid,len(KU),len(cl),flush=True)
 print('pencil done',a,'count',count,'stats',stats,'sec',time.time()-t0,flush=True)
json.dump({'count':count,'stats':{str(k):v for k,v in stats.items()},'leaves':out},open('workspace/agent2_T288_quad_ALLh_lifts.json','w'))
pathlib.Path('workspace/agent2_T288_quad_ALLh_lifts.py').write_text(pathlib.Path(__file__).read_text());print('DONE',len(out),'with cl3extras',time.time()-t0)
