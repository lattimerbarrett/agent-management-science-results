import json,random,sys,time,pathlib,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
random.seed(80114);V=veronese(10,4)
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
 while len(bs)<5:
  v0=random.randrange(1,1024);v=v0
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;bs.append(v0);break
 P=[random.randrange(1024)]
 for b in bs:P +=[p^b for p in P]
 return P

def mask(P):
 z=0
 for p in P:z|=1<<p
 return z
halves={(l,e):[i for i in range(32) if ((i&l).bit_count()%2)==e] for l in range(1,32) for e in [0,1]}
start=time.time();hist=collections.Counter();hits=[];moves=0;checks=0;maxK=0
for restart in range(40):
 while True:
  comps=[flat() for j in range(3)];z=mask(comps[0])^mask(comps[1])^mask(comps[2])
  if z.bit_count()==80:break
 for it in range(10000):
  P=random.choice(comps);idx=halves[random.randrange(1,32),random.randrange(2)];U=[P[i] for i in idx];u=mask(U)
  if u&z!=u:continue
  v=random.randrange(1,1024);W=[p^v for p in U];w=mask(W)
  if w&z:continue
  z^=u^w;moves+=1;comps.append(U+W)
  if len(comps)>64:comps.pop(0)
  if moves%10:continue
  S=[];a=z
  while a:t=a&-a;S.append(t.bit_length()-1);a^=t
  K=kernel(S);hist[len(K)]+=1;checks+=1
  if len(K)>maxK:maxK=len(K);print('maxK',maxK,'checks',checks,'time',time.time()-start,flush=True)
  if any((a&b).bit_count()%2 for a in K for b in K):
   ans={'support':S,'Kdim':len(K)};hits.append(ans);json.dump(hits,open('workspace/agent1_S80_switch_nonself.json','w'));print('HIT',len(K),restart,it,flush=True);raise SystemExit
 if restart%10==0:print(restart,'moves',moves,'checks',checks,'hist',dict(hist),time.time()-start,flush=True)
json.dump({'moves':moves,'checks':checks,'K4hist':dict(hist),'hits':hits},open('workspace/agent1_S80_switch_results.json','w'));pathlib.Path('workspace/agent1_S80_switch.py').write_text(pathlib.Path(__file__).read_text());print('DONE',moves,checks,dict(hist),time.time()-start)
