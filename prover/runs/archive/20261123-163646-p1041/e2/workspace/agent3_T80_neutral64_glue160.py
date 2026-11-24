import itertools,collections,json,pathlib,time,random,sys,numpy as np
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
raw=json.load(open('workspace/agent4_higherorthogonal320_pipeline.json'))[0]['found'];rng=random.Random(322333)
def bas(B):
 D={}
 for x in B:
  z=x
  while z:
   k=z.bit_length()-1
   if k in D:z^=D[k]
   else:D[k]=z;break
 return D
AA=np.arange(1024,dtype=np.uint16);A=np.array([np.zeros(1024,dtype=np.uint16),AA&31,AA>>5,(AA&31)^(AA>>5)])
start=time.time();hist=collections.Counter();hits=[];trials=0
for si,ob in enumerate(raw):
 S=set(ob['support']);ls=sorted(S);pairs=collections.defaultdict(list)
 for i,a in enumerate(ls):
  for b in ls[i+1:]:pairs[a^b].append((a,b))
 ds=[v for v,ps in pairs.items() if len(ps)>=2]
 for trial in range(100):
  v=rng.choice(ds);p,q=rng.sample(pairs[v],2);o=p[0];B=[v,p[0]^q[0]]
  while len(B)<11:
   z=rng.randrange(1,2048)
   if len(bas(B+[z]))>len(B):B.append(z)
  pts=[0]
  for b in B:pts += [x^b for x in pts]
  inv={x:i for i,x in enumerate(pts)};hh=np.zeros((16,32),dtype=np.uint8)
  for p in S:
   y=inv[p^o];hh[(y>>2)&15,y>>6]+=1
  score=np.zeros((1024,1024),dtype=np.uint8)
  for vv in range(16):score += hh[vv,A[vv&3,:,None]^A[vv>>2,None,:]]
  mx=int(score.max());hist[mx]+=1;trials+=1
  wh=np.argwhere(score==32)
  for ia,ib in wh[:4]:
   cols=[int(ia&31),int(ia>>5),int(ib&31),int(ib>>5)];H=set()
   for x in range(64):
    yy=0
    for j,c in enumerate(cols):
     if x>>(2+j)&1:yy^=c
    H.add(pts[x+(yy<<6)]^o)
   assert len(H)==64 and len(H&S)==32
   T=S^H;assert len(T)==80
   translates=[v for v in [next(iter(T))^s for s in S] if {s^v for s in S}==T]
   if translates:continue
   Z=S|{s+2048 for s in T};K=kernel(sorted(Z),veronese(12,5))
   hit={'source':si,'trial':trial,'g':sorted(S),'h':sorted(T),'H':sorted(H),'support':sorted(Z),'K5':len(K),'basis':B,'offset':o,'cols':cols}
   hits.append(hit);print('HIT',si,trial,'K5',len(K),'elapsed',time.time()-start,flush=True)
   if len(K)==1:break
  if hits and hits[-1]['K5']==1:break
  if time.time()-start>160:break
 if hits and hits[-1]['K5']==1:break
 if time.time()-start>160:break
 print('source',si,'hist',dict(hist),'hits',len(hits),'elapsed',time.time()-start,flush=True)
out={'trials':trials,'hist':dict(hist),'hits':hits,'elapsed':time.time()-start}
pathlib.Path('workspace/agent3_T80_neutral64_glue160.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_T80_neutral64_glue160.py').write_text(pathlib.Path('scratchpad.py').read_text())
