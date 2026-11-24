import sys,json,pathlib,itertools,collections,time,random,numpy as np
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese

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
D=json.load(open('workspace/agent2_T28810_K14_seed.json'));T=D['T'];B={};A=[sum(1<<i for i,p in enumerate(T) if j==-1 or p>>j&1) for j in range(-1,10)]
for a in A:assert ins(B,a)
E=[]
for x in D['K']:
 z=ins(B,x)
 if z:E.append(z)
assert len(E)==3
es=[0]
for e in E:es +=[x^e for x in es]
afs=[0]
for a in A:afs +=[x^a for x in afs]
wts=np.array([[(e^a).bit_count() for a in afs] for e in es],dtype=np.int16);idx=np.arange(2048);xor=idx[:,None]^idx[None,:];v5=veronese(12,5);hist=collections.Counter();paircounts=[];hits=[];seen=set();rng=np.random.default_rng(1415);t=time.time()
for e in range(1,8):
 for f in range(e+1,8):
  space=tuple(sorted((e,f,e^f)))
  if space in seen:continue
  seen.add(space);inter=(wts[e,:,None]+wts[f,None,:]-wts[e^f][xor])//2
  for I in [16,18,20,22]:
   inds=np.flatnonzero(inter==I);paircounts.append({'space':space,'I':I,'count':len(inds)})
   if not len(inds):continue
   sample=rng.choice(inds,size=min(128,len(inds)),replace=False)
   for ind in sample:
    a=int(ind)//2048;b=int(ind)%2048;h=es[e]^afs[a];k=es[f]^afs[b];S=[]
    for j,p in enumerate(T):
     hb=h>>j&1;kb=k>>j&1
     if hb:S.append(p|1024)
     if kb:S.append(p|2048)
     if 1^hb^kb:S.append(p|3072)
    assert len(S)==288+2*I
    K=kernel(S,v5);hist[I,len(K)]+=1
    if len(K)>=15:hits.append({'space':space,'a':a,'b':b,'I':I,'support':S,'K':K});print('HIT',I,len(K),space,a,b,flush=True)
  print('space',space,'hist',hist,'sec',time.time()-t,flush=True)
json.dump({'hist':{str(k):v for k,v in hist.items()},'paircounts':paircounts,'hits':hits},open('workspace/agent2_T28810_quadratic320.json','w'));pathlib.Path('workspace/agent2_T28810_quadratic320.py').write_text(pathlib.Path(__file__).read_text());print('DONE',hist,'hits',len(hits))
