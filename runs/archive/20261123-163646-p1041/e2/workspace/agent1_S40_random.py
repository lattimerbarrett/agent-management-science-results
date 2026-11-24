import json,random,sys,time,pathlib,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
random.seed(75041)
V=veronese(7,2)
def kernel(S):
 B={};out=[]
 for i,p in enumerate(S):
  v=V[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out

def flat():
 B={};bs=[]
 while len(bs)<4:
  v0=random.randrange(1,128);v=v0
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;bs.append(v0);break
 P=[random.randrange(128)]
 for b in bs:P +=[p^b for p in P]
 z=0
 for p in P:z|=1<<p
 return z

start=time.time();ct=0;hist=collections.Counter();seen=set();hits=[]
for it in range(200000):
 z=0
 for j in range(random.randint(3,7)):z^=flat()
 if z.bit_count()!=40 or z in seen:continue
 seen.add(z);S=[p for p in range(128) if z>>p&1];K=kernel(S);hist[len(K)]+=1
 if any((a&b).bit_count()%2 for a in K for b in K):
  print('NONSELF',len(K),it,'time',time.time()-start,flush=True);hits.append({'support':S,'Kdim':len(K)})
  json.dump(hits,open('workspace/agent1_S40_nonselforth.json','w'))
  if len(hits)>=20:break
 if len(seen)%1000==0:print(it,len(seen),dict(hist),time.time()-start,flush=True)
print('DONE',len(seen),dict(hist),'hits',len(hits),'time',time.time()-start)
json.dump({'distinctS40':len(seen),'K2hist':dict(hist),'hits':hits},open('workspace/agent1_S40_random_result.json','w'));pathlib.Path('workspace/agent1_S40_random.py').write_text(pathlib.Path(__file__).read_text())
