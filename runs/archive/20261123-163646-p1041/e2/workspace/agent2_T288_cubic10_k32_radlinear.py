import json,sys,pathlib,collections,time,itertools
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
D=json.load(open('workspace/agent2_Q6_quadsmall.json'));Q=D['Q'];BB={int(k):tuple(v) for k,v in D['cubic_extension'].items()};EE=[]
for i in range(35):
 z=(1<<i)|(1<<35);f=0
 while z:
  k=z.bit_length()-1;z^=BB[k][0];f^=BB[k][1]
 EE.append(f)
def ext(z):
 f=0;z &= (1<<35)-1
 while z:
  b=z&-z;f^=EE[b.bit_length()-1];z^=b
 return f
q=lambda x: ((x&1)*(x>>1&1))^((x>>2&1)*(x>>3&1))^((x>>4&1)*(x>>5&1))
qfull=sum(q(x)<<x for x in range(64));v3=veronese(8,3);hist=collections.Counter();hits=[];count=0;t=time.time()
for ai,a in enumerate(D['small']):
 inds=[i for i in range(36) if a['Qmask']>>i&1];inside=[]
 for b in range(1<<len(inds)):
  if b.bit_count()%2 == (1 if a['weight']==6 else 0):inside.append(sum(1<<p for j,p in enumerate(inds) if b>>j&1))
 outside=[1<<i for i in range(36) if not a['Qmask']>>i&1] if a['weight']==6 else [0]
 for out in outside:
  for inn in inside:
   hf=ext(out|inn);af=a['full'];sf=hf|((hf^qfull)<<64)|((hf^af)<<128)|((hf^af^qfull)<<192);S=[]
   while sf:
    b=sf&-sf;S.append(b.bit_length()-1);sf^=b
   assert len(S)==72
   K=kernel(S,v3);odd=sum((x&y).bit_count()%2 for ix,x in enumerate(K) for y in K[ix+1:]);hist[a['weight'],len(K),bool(odd)]+=1;count+=1
   if odd:
    hits.append({'a':ai,'hQ':out|inn,'hfull':hf,'support':S,'K3':len(K),'odd':odd});print('HIT',hits[-1],flush=True)
 if (ai+1)%100==0:print('progress',ai+1,count,'sec',time.time()-t,flush=True)
print('DONE',count,hist,'hits',len(hits),'sec',time.time()-t)
json.dump({'count':count,'hist':{str(k):v for k,v in hist.items()},'hits':hits},open('workspace/agent2_T288_cubic10_k32_radlinear.json','w'));pathlib.Path('workspace/agent2_T288_cubic10_k32_radlinear.py').write_text(pathlib.Path(__file__).read_text())
