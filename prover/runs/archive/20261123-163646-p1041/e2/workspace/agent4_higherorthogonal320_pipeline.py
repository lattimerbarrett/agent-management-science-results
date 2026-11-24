import json,time,random,collections,itertools
from pathlib import Path
rng=random.Random(8040160320);st=time.time()
def echelon(rows):
 B={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;break
 return B
def reduce(B,v):
 while v:
  k=v.bit_length()-1
  if k not in B:return v
  v^=B[k]
 return 0
def orth(rows,N):
 B=echelon(rows);out=[]
 for j in range(N):
  if j in B:continue
  v=1<<j
  for p in sorted(B):
   if (B[p]&v).bit_count()%2:v^=1<<p
  out.append(v)
 return out
def randomspan(B):
 m=rng.getrandbits(len(B));v=0
 for j,b in enumerate(B):
  if m>>j&1:v^=b
 return v
def products(C,r):
 out={C[0]}
 for k in range(1,min(r,len(C)-1)+1):
  for cc in itertools.combinations(C[1:],k):
   v=C[0]
   for c in cc:v&=c
   if v:out.add(v)
 return out
def extend(C,target,N,r):
 BB=echelon(C)
 while len(C)<target:
  V=orth(products(C,r-1),N)
  if len(V)<=len(C):return None
  for _ in range(20):
   v=randomspan(V)
   if reduce(BB,v):break
  else:return None
  C.append(v);BB=echelon(C)
 return C
def points(C,N):return [sum(((v>>j)&1)<<i for i,v in enumerate(C[1:])) for j in range(N)]
def periods(S):
 SS=set(S);p=S[0];return [p^q for q in S if all(x^p^q in SS for x in S)]
D=json.loads(Path('workspace/agent4_triorthogonal40_walk.json').read_text());core=D['aperiodic'][0]['support'];out=[]
for co in [5,6,7]:
 n=co+6;N=len(core)*2;full=(1<<N)-1;S=[x|(rr<<(n-1)) for x in core for rr in range(2)];target=n+1;C=[full]+[sum(((x>>j)&1)<<i for i,x in enumerate(S)) for j in range(n)];r=co-1
 assert len(echelon(C))==target
 hist=collections.Counter();accepted=0;found=[];proposals=0;start=time.time();bestdim=0
 for k in range(1000000):
  proposals+=1;drop=rng.choice([2,3,3,4,4,5]);keep=[full]+rng.sample(C[1:],target-1-drop);cand=extend(keep,target,N,r)
  if cand is None:hist['dead']+=1;continue
  pts=points(cand,N)
  if len(set(pts))<N:hist['duplicate']+=1;continue
  C=cand;accepted+=1;PV=periods(pts);pd=len(PV).bit_length()-1;hist['pd'+str(pd)]+=1
  if pd==0:
   # K_(co-2) is annihilator of products of coordinate rows up to co-2.
   K=orth(products(C,co-2),N);kd=len(K);bestdim=max(bestdim,kd);gram=sum((a&b).bit_count()%2 for a in K for b in K)
   kkfull=N-len(echelon(products(C,co-1)));assert kkfull>=1
   found.append({'support':sorted(pts),'C':C,'Klow':kd,'Kfull':kkfull,'Gram':gram})
   print('APERIODIC',co,'Klow',kd,'Kfull',kkfull,'Gram',gram,'accepted',accepted,'proposal',proposals,'seconds',time.time()-start,flush=True)
   if gram or len(found)>=20:break
  if time.time()-start>100:break
 print('STAGE',co,'FINISHED',accepted,proposals,hist,'found',len(found),'seconds',time.time()-start,flush=True)
 rr={'co':co,'N':N,'accepted':accepted,'proposals':proposals,'hist':dict(hist),'found':found,'seconds':time.time()-start};out.append(rr);Path('workspace/agent4_higherorthogonal320_pipeline.json').write_text(json.dumps(out))
 if not found:break
 candidates=[f for f in found if f['Kfull']==1]
 if not candidates:candidates=found
 core=max(candidates,key=lambda f:(f['Gram']>0,f['Klow']))['support']
Path('workspace/agent4_higherorthogonal320_pipeline.py').write_text(Path('scratchpad.py').read_text().split('